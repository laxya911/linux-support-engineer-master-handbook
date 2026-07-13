# Chapter 3: Flame Graphs

You now know how to trace system calls and disk I/O using eBPF and BCC tools. But what if the bottleneck isn't the disk, the network, or the system calls? What if the bottleneck is the application's own code? 

If a Java application is consuming 100% CPU purely executing logic (like parsing massive JSON blobs or computing hashes), `strace` or `execsnoop` will tell you absolutely nothing. The application isn't talking to the kernel; it's just spinning the CPU. 

To visualize where CPU cycles are being spent inside an application, we use **Flame Graphs**.

## What is a Flame Graph?

Invented by Brendan Gregg, a Flame Graph is a brilliant visualization of profiled software, allowing you to identify the most frequent code paths quickly and accurately. 

Instead of reading through thousands of lines of raw text output from a profiler, a Flame Graph turns the call stack into an interactive, color-coded SVG image.

### Reading a Flame Graph

When you look at a Flame Graph, it looks like a literal wall of flames. Here is how to interpret it:

1. **The Y-Axis (Height):** Represents the stack depth (the lineage of function calls). The bottom box is the parent function (e.g., `main()`). The box above it is the function that `main()` called. The higher you go, the deeper into the code you are.
2. **The X-Axis (Width):** Represents the *population* of samples, not the passage of time. If a function box is very wide, it means the CPU spent a massive percentage of its total time executing that specific function. 
3. **The Colors:** By default, colors are chosen randomly just to differentiate the boxes. Warmer colors (reds and oranges) are used purely for aesthetics. (However, some advanced flame graphs use color to represent other metrics, like memory allocations).

**The Golden Rule of Flame Graphs:** Look for the widest boxes at the top of the flames. The top boxes are the functions currently executing on the CPU. The wider they are, the more CPU time they are burning. 

## How to Generate a Flame Graph

Generating a Flame Graph is a two-step process: Profiling, and then Rendering.

### Step 1: Profiling with `perf`

`perf` is the official performance analyzing tool built into the Linux kernel. It works by "sampling" the CPU at a specific frequency (e.g., 99 times a second) and recording exactly which function the CPU was executing at that exact microsecond.

To profile a specific process (PID 1234) for 60 seconds at 99 Hertz:
```bash
$ sudo perf record -F 99 -p 1234 -g -- sleep 60
```
This generates a binary file named `perf.data` containing all the raw stack traces.

### Step 2: Rendering the Graph

To turn the `perf.data` file into an SVG image, you use Brendan Gregg's open-source `FlameGraph` Perl scripts:

```bash
$ sudo perf script | ./FlameGraph/stackcollapse-perf.pl | ./FlameGraph/flamegraph.pl > cpu_profile.svg
```
You can then open `cpu_profile.svg` in any web browser. It is fully interactive—you can click on boxes to zoom in and search for specific function names.

---

## Scenario-Based Troubleshooting

### Scenario A: The CPU Hog

> [!IMPORTANT]  
> **Incident Report: The CPU Hog**  
> **Reporter:** Infrastructure Team  
> **SOP execution:**
> 
> 1. **11:00 AM — Incident Receipt:** An alert fires indicating that a critical Python microservice is consuming 100% of a CPU core, causing message processing to lag behind.
> 
> 2. **11:02 AM — Triage & Containment:** The engineer runs `top` and confirms the Python process is pinned at 100% CPU. Restarting the service temporarily fixes it, but the CPU climbs back to 100% within 5 minutes.
> 
> 3. **11:05 AM — Investigation:** The engineer uses `perf` to record the CPU's stack traces for 30 seconds:
>    `sudo perf record -F 99 -p <PID> -g -- sleep 30`
>    They then generate a Flame Graph SVG and open it in their browser.
> 
> 4. **11:10 AM — Root Cause:** Looking at the Flame Graph, the engineer immediately spots a massive, flat box at the top of the graph taking up 85% of the total width. The box is labeled `re.compile()` (the Python regular expression compiler). The developer had placed a regex compilation step *inside* a `for` loop that iterates millions of times, forcing the CPU to recompile the regex on every single loop iteration.
> 
> 5. **11:15 AM — Resolution:** The engineer contacts the developer. They move the `re.compile()` statement outside of the loop so it only compiles once. The code is redeployed.
> 
> 6. **11:30 AM — Verification:** The engineer generates a second Flame Graph. The massive `re.compile()` plateau is completely gone. Overall CPU usage drops from 100% to 12%.
> 
> 7. **Post-Mortem:** Discuss the importance of moving expensive computations outside of loops during code review.
> 
> 8. **Documentation:** Add the before-and-after Flame Graphs to the incident ticket to visualize the massive performance win.

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Sampling at 100 Hz instead of 99 Hz. Always use odd frequencies like 99 Hertz (`-F 99`) for sampling. If you sample at exactly 100 Hz, your samples might perfectly align with system timers or background tasks that execute exactly every 10 milliseconds. This causes "lockstep" sampling, where your data is skewed and misrepresents reality.

> [!TIP] Pro-Tip
> When analyzing applications written in Java, Node.js, or Python, standard `perf` will only show you the C-level functions of the JVM or the Python Interpreter, not your actual Java or Python function names. To fix this, you must run your application with specific flags (like `--perf-basic-prof` in Node.js) or use specialized eBPF profilers designed for JIT languages.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 3 Practice Guide](../practice-files/V5-C03-practice.md) to generate your very first Flame Graph using a simulated CPU load!

## Interview Questions

### Question 1: How do you interpret the X and Y axes of a Flame Graph?
* **Target Answer**: "The Y-axis represents stack depth; it shows the lineage of function calls from the parent at the bottom to the child at the top. The X-axis represents the percentage of total CPU time. It does *not* represent time sequentially left-to-right. Therefore, the widest boxes at the top of the graph are the functions burning the most CPU cycles."

### Question 2: Why do we use a sampling profiler like `perf` instead of an instrumentation profiler?
* **Target Answer**: "Instrumentation profilers modify the code to inject timing logs at the start and end of every single function. This causes massive performance overhead, heavily skewing the results (the Observer Effect). A sampling profiler like `perf` simply interrupts the CPU 99 times a second to take a quick snapshot of what is running. This creates an incredibly accurate statistical picture of performance with almost zero overhead, making it safe for production."

### Question 3: Why should you sample at 99 Hertz instead of 100 Hertz?
* **Target Answer**: "To avoid lockstep sampling. If you sample exactly in sync with the system's clock ticks or timer-based interrupts, you might repeatedly sample the exact same background maintenance task, incorrectly concluding that the task is taking up 100% of the CPU. An odd frequency ensures random, statistically sound samples."

---

## Navigation

⬅ Previous:
[Chapter 2 – Tracing with eBPF and BCC](V5-C02-ebpf-and-bcc.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 4 – Memory Leaks and Analysis](V5-C04-memory-leaks.md)
