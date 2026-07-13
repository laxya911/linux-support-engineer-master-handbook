# Chapter 4: Memory Leaks and Analysis

When a CPU bottlenecks, the system slows down. When a network bottlenecks, the system slows down. But when memory runs out, the system panics and starts violently executing processes to survive.

A slow system is frustrating. A system actively terminating its own critical infrastructure is a Sev1 incident.

In this chapter, we will learn how to identify memory leaks, understand the Linux Out Of Memory (OOM) Killer, and trace precisely where memory is being consumed.

## The Anatomy of Memory

To diagnose memory issues, you must first understand how Linux views memory. 

When you run `free -m`, you see several columns:
* **Total:** Physical RAM installed.
* **Used:** Memory currently assigned to applications.
* **Free:** Memory completely unused. (In a healthy Linux server, this should be close to zero!).
* **Buff/Cache:** Memory the kernel is using to cache disk data for faster access. *This is technically free memory*, as the kernel will instantly dump the cache if an application needs it.
* **Available:** The actual amount of memory applications can safely ask for right now without forcing the system to swap. **This is the most important metric.**

### The Swap Space

When physical RAM is completely exhausted, the kernel uses "Swap"—a dedicated partition on the physical hard drive. It moves the least-used pages of memory from fast, expensive RAM to slow, cheap Disk. 

If a system is actively swapping pages in and out (`si` and `so` in `vmstat`), performance will degrade by orders of magnitude because disk access is millions of times slower than RAM access.

## The OOM Killer

If memory is exhausted, and Swap is exhausted, the Linux kernel has no choice but to invoke the **Out Of Memory (OOM) Killer**. 

The OOM Killer's job is to sacrifice a child to save the village. It calculates an `oom_score` for every process on the system based on memory consumption and priority. It then ruthlessly sends a `SIGKILL` (Signal 9) to the process with the highest score.

If your database suddenly disappears without a trace, and there is nothing in the database logs, always check the kernel logs for the OOM Killer's signature:
```bash
$ dmesg -T | grep -i oom
```
You will see a message like: `Out of memory: Killed process 1234 (mysqld)`.

## Diagnosing Memory Leaks

A memory leak occurs when an application allocates memory but forgets to free it when it's done. Over hours or days, the application slowly consumes all available RAM until the OOM Killer strikes.

If you suspect an application is leaking memory, do not just restart it. You destroy the evidence.

### Tool 1: Valgrind
`Valgrind` is the industry-standard tool for profiling memory. It runs your application in a highly monitored sandbox. When the application exits, Valgrind prints a summary of exactly how many bytes were leaked and exactly which lines of code failed to call `free()`.

*Warning:* Valgrind introduces massive overhead (slowing the application by 20x to 50x) and should never be run in production.

### Tool 2: BCC `memleak`
Because Valgrind is too heavy for production, we return to our eBPF superpower. The BCC tool `memleak-bpfcc` attaches eBPF probes to the C standard library's `malloc()` (memory allocate) and `free()` functions.

If it sees an application call `malloc()` 1,000 times, but only call `free()` 900 times, it captures the stack trace of the 100 missing calls and prints them to your screen, allowing you to find memory leaks in production with minimal overhead.

---

## Scenario-Based Troubleshooting

### Scenario A: The Midnight Crash

> [!IMPORTANT]  
> **Incident Report: The Midnight Crash**  
> **Reporter:** Automated Monitoring  
> **SOP execution:**
> 
> 1. **02:00 AM — Incident Receipt:** PagerDuty alerts that the primary staging Redis cache has crashed and restarted.
> 
> 2. **02:05 AM — Triage & Containment:** The engineer logs in. Redis is back online (systemd restarted it), but the cache is completely empty. The engineer checks the Redis application logs, but they end abruptly with no error messages.
> 
> 3. **02:10 AM — Investigation:** Recognizing the symptom of an abrupt, unlogged termination, the engineer suspects the kernel intervened. They run `dmesg -T | grep -i "Out of memory"`. The kernel ring buffer clearly shows: `Out of memory: Killed process 5678 (redis-server), total-vm:8450000kB`. 
>    The engineer reviews historical Grafana graphs and sees Redis memory consumption climbing steadily in a straight diagonal line for 48 hours until it hit the server's 8GB limit.
> 
> 4. **02:15 AM — Root Cause:** A new caching policy was deployed on Friday. It instructed the application to cache user sessions for 30 days but failed to set a `maxmemory` eviction policy in Redis. Redis blindly cached everything until it consumed all physical RAM and triggered the OOM Killer.
> 
> 5. **02:20 AM — Resolution:** The engineer edits `redis.conf` and sets `maxmemory 6gb` and `maxmemory-policy allkeys-lru` (Least Recently Used). They restart the Redis service.
> 
> 6. **02:25 AM — Verification:** The engineer monitors the memory usage. When it hits 6GB, Redis correctly evicts old keys instead of crashing. Memory usage plateaus.
> 
> 7. **Post-Mortem:** Discuss why staging environments must be sized appropriately to catch memory exhaustion before production.
> 8. **Documentation:** Update infrastructure-as-code to enforce `maxmemory` limits on all new Redis clusters.

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Panicking when `free` shows 0 under the "Free" column. This is normal! Linux philosophy states that "Free RAM is Wasted RAM." The kernel intentionally uses all free RAM to cache disk reads. Always look at the **Available** column to see how much RAM the system actually has left for your applications.

> [!TIP] Pro-Tip
> You can protect critical processes (like your SSH daemon) from the OOM Killer by adjusting their `oom_score_adj` value. Setting a process's adjustment score to `-1000` makes it completely immune to the OOM Killer, ensuring you never get locked out of a server during a memory crisis.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 4 Practice Guide](../practice-files/V5-C04-practice.md) to write a C program that deliberately leaks memory, and catch it using `valgrind`!

## Interview Questions

### Question 1: What is the difference between "Free" and "Available" memory in Linux?
* **Target Answer**: "Free memory is RAM that is completely untouched. Available memory is the amount of RAM that can be given to a new application without forcing the system to swap. Because Linux aggressively uses untouched RAM for disk caching (which it will instantly drop if an application needs it), the 'Free' column is often near zero, while the 'Available' column provides the true health of the system."

### Question 2: Why would a process disappear from a Linux server with absolutely nothing written to its application logs?
* **Target Answer**: "This is the hallmark of the Linux OOM (Out Of Memory) Killer. If the system exhausts all RAM and Swap, the kernel steps in and terminates the largest memory consumer using a `SIGKILL` (Signal 9). Because a `SIGKILL` cannot be intercepted by the application, the application has no opportunity to write an error to its logs before it dies. You must check the kernel logs (`dmesg`) to prove it."

### Question 3: How does the BCC `memleak` tool find leaks without the massive overhead of Valgrind?
* **Target Answer**: "It uses eBPF probes attached to memory allocation functions like `malloc()` and `free()`. Every time memory is allocated, eBPF records the stack trace. Every time memory is freed, it deletes that record. Anything left over when the tool stops is a leak. Because eBPF runs highly optimized, JIT-compiled code directly in the kernel, it can perform this tracking with minimal performance impact, making it safe for production analysis."



**Chapter Transition**
> Memory leaks are resolved, but the application is still slow. Is it the code, or is the network silently dropping packets?

---

## Navigation

⬅ Previous:
[Chapter 3: Flame Graphs](V5-C03-flame-graphs.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 5: Network Latency Profiling](V5-C05-network-latency-profiling.md)
