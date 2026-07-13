# Chapter 2: Tracing with eBPF and BCC

In the previous chapter, we used standard tools like `top` and `iostat` to measure Utilization and Saturation. But what happens when those tools aren't enough? What if `top` shows 90% CPU usage, but you need to know *exactly* which line of code inside the kernel is burning those cycles?

Historically, tracing the Linux kernel in production was dangerous. It often required modifying the kernel source code, loading custom kernel modules, or using tools that caused massive performance overhead (like `strace`).

Today, we have **eBPF**.

## What is eBPF?

eBPF (Extended Berkeley Packet Filter) is arguably the most important Linux technology developed in the last decade. 

It allows you to run sandboxed, highly efficient programs *directly inside the kernel* without changing kernel source code or loading kernel modules. 

Think of the kernel as a highly secure vault. User-space applications cannot enter the vault directly; they must slide requests (system calls) under the door. Historically, if you wanted to observe how the vault workers were handling requests, you had to stop the workers and ask them (which is slow), or modify the workers' DNA (which is dangerous).

eBPF allows you to dynamically place invisible cameras (probes) inside the vault. The cameras execute small, verified programs that collect data and send it back to user space asynchronously.

### The Superpowers of eBPF
1. **Safety:** The kernel validates every eBPF program before it runs to ensure it cannot crash the system or enter an infinite loop.
2. **Speed:** eBPF programs are JIT (Just-In-Time) compiled into native machine code, meaning the performance overhead is practically zero.
3. **Visibility:** You can attach eBPF probes to almost *anything*: network sockets, system calls, kernel functions, or even user-space application functions (like Java or Python methods).

## The BCC Toolkit

Writing raw eBPF code in C is extremely complex. Fortunately, the **BCC** (BPF Compiler Collection) provides a suite of pre-written, ready-to-use profiling scripts that harness the power of eBPF.

When you install the BCC tools (`sudo apt install bpfcc-tools`), you get over 100 specialized performance scripts.

### Essential BCC Tools

* `execsnoop-bpfcc`: Traces new processes. Unlike `top`, which polls every 3 seconds and misses short-lived processes, `execsnoop` attaches an eBPF probe directly to the `execve()` system call. It will catch a script that executes and dies in 1 millisecond.
* `opensnoop-bpfcc`: Traces file opens. If an application is failing because it's looking for a config file in the wrong directory, `opensnoop` will instantly show you the exact path the application *tried* to open, and the `ENOENT` (File not found) error it received.
* `biolatency-bpfcc`: Measures block I/O latency. Instead of just seeing average queue sizes in `iostat`, this tool generates a beautiful histogram showing exactly how many disk operations took 1ms, 10ms, or 100ms.
* `tcplife-bpfcc`: Traces TCP sessions. It prints a summary line for every TCP connection that opens and closes, including the total bytes transmitted and the duration, all without the massive overhead of `tcpdump`.

---

## Scenario-Based Troubleshooting

### Scenario A: The Phantom CPU Spikes

> [!IMPORTANT]  
> **Incident Report: The Phantom CPU Spikes**  
> **Reporter:** Automated Monitoring  
> **SOP execution:**
> 
> 1. **09:00 AM — Incident Receipt:** Datadog alerts that a critical worker node is experiencing intermittent 100% CPU spikes, causing API latency.
> 
> 2. **09:02 AM — Triage & Containment:** The engineer logs in and runs `top`. The CPU is currently sitting at 5%. The engineer watches `top` for 2 minutes, but catches nothing. The spikes are too brief.
> 
> 3. **09:05 AM — Investigation:** The engineer realizes `top` polls too slowly to catch short-lived processes. They run `sudo execsnoop-bpfcc`. 
>    * Suddenly, the screen floods with thousands of `curl` commands being executed in rapid succession. 
>    * The output reveals the Parent Process ID (PPID) spawning these `curl` commands.
> 
> 4. **09:08 AM — Root Cause:** The engineer tracks the PPID to a poorly written cron script (`/opt/scripts/healthcheck.sh`). The script was supposed to check a URL once a minute, but a missing `sleep` command inside a `while` loop caused it to execute thousands of times a second.
> 
> 5. **09:12 AM — Resolution:** The engineer kills the runaway script and corrects the logic.
> 
> 6. **09:15 AM — Verification:** `execsnoop` shows no more phantom processes. CPU utilization normalizes.
> 
> 7. **Post-Mortem:** Discuss why standard monitoring failed to catch the short-lived processes and train the team on eBPF tooling.
> 
> 8. **Documentation:** Add `execsnoop` to the standard troubleshooting playbook for unexplained CPU spikes.

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Running `strace` in production instead of `opensnoop` or `execsnoop`. `strace` pauses the application using `ptrace` for every single system call, which can grind a database or web server to a halt. Always reach for eBPF/BCC tools first in production environments for safe, zero-overhead tracing.

> [!TIP] Pro-Tip
> The BCC tools often require kernel headers to compile the eBPF code on the fly. If you run a BCC tool and it errors out complaining about missing headers, simply run `sudo apt install linux-headers-$(uname -r)` (or the equivalent for your distro) to install the map of the kernel so the BCC compiler knows where to place its probes.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 2 Practice Guide](../practice-files/V5-C02-practice.md) to use `opensnoop` to find a hidden configuration file!

## Interview Questions

### Question 1: What is the primary advantage of eBPF over legacy tracing tools like `strace`?
* **Target Answer**: "eBPF provides deep kernel visibility with near-zero performance overhead. Unlike `strace`, which forces the kernel to context-switch and pause the application for every single system call, eBPF runs JIT-compiled, verified programs directly in kernel space asynchronously. This makes eBPF safe to run on heavy production workloads."

### Question 2: Why would you use `execsnoop` instead of `top` or `ps`?
* **Target Answer**: "Tools like `top` and `ps` work by taking a snapshot of the `/proc` filesystem at regular intervals (e.g., every 1-3 seconds). If a malicious script or an inefficient loop spawns a process that only lives for a few milliseconds, it will disappear before `top` can capture it. `execsnoop` attaches an eBPF probe directly to the kernel's process execution mechanism, meaning it guarantees you will see every single command run on the system, no matter how brief."

### Question 3: How does the kernel guarantee that an eBPF program won't crash the server?
* **Target Answer**: "Before an eBPF program is allowed to load into the kernel, it must pass through the eBPF Verifier. The verifier mathematically analyzes the code to ensure it does not contain infinite loops, illegal memory accesses, or uninitialized variables. If the program cannot be proven safe, the kernel rejects it."

---

## Navigation

⬅ Previous:
[Chapter 1 – The USE Method & System Profiling](V5-C01-the-brendan-gregg-method.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 3 – Flame Graphs](V5-C03-flame-graphs.md)
