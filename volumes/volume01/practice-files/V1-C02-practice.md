# Practice Guide: Chapter 2

## Objective
To explore the four layers of the Linux architecture (User Space, Libraries, Kernel, Hardware) and observe processes generating system calls.

## Assignment 1: Basic Architecture Discovery
Boot up the Virtual Machine you created in Chapter 1 and log in. Run the following commands and record your observations:
1. `uname -a` (What information is returned?)
2. `hostnamectl` (Which OS version and Kernel are running?)
3. `cat /etc/os-release` (What is the exact name and version of the distribution?)

## Assignment 2: Process and Memory Inspection
1. Run `top`.
   * Identify the process consuming the most CPU.
   * Identify the total amount of RAM and Swap space.
   * Press `q` to exit `top`.
2. Run `free -m`.
   * How does this output differ from what you saw in `top`?
3. Run `ps -ef`.
   * Find the process with PID `1`. What is the name of this process?

## Assignment 3: System Call Tracing
1. Run `strace ls`.
   * You will see a massive wall of text. Scroll up.
   * Look for the `openat()` or `read()` system calls. 
   * Even though `ls` is a very simple command in User Space, observe how much communication it requires with the Kernel to actually read the disk.

## Success Criteria
You have successfully completed this practice if you understand that typing a command in User Space relies entirely on the Kernel (via System Calls) to access Hardware.
