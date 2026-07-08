# Practice Guide: Chapter 19 (Volume 4)

## Objective
To use `strace` to launch a simple command, observe the raw system calls it makes to the kernel, and force a "Permission Denied" error to see how the kernel responds.

## Assignment 1: Basic System Call Tracing
We all know the `cat` command prints a file to the screen. But what does it *actually* do behind the scenes?

1. Ensure `strace` is installed (it usually is on Ubuntu/RHEL):
   `sudo apt install strace` or `sudo dnf install strace`
2. Run the `cat` command through `strace` to read a harmless file like `/etc/hostname`:
   `strace cat /etc/hostname`
3. **Observation:** You will see about 30 lines of output before it actually prints the hostname! Don't panic, let's break it down.
   * The first 20 lines are `execve()`, `mmap()`, and `openat()`. This is the Linux kernel loading the `cat` binary into memory and loading all the required C libraries.
   * Look near the bottom. You will see `openat(AT_FDCWD, "/etc/hostname", O_RDONLY) = 3`. The kernel successfully opened the file and assigned it File Descriptor number 3.
   * On the very next line, you will see `read(3, "your-hostname\n", 131072)`. The `cat` program asked the kernel to read the contents of File Descriptor 3!
   * Finally, you will see `write(1, "your-hostname\n", ...`. The `cat` program asked the kernel to write the string to File Descriptor 1 (Standard Output / Your Screen).

## Assignment 2: Tracing Errors
Now let's see what it looks like when something goes wrong.

1. Create a secret file:
   `echo "My Secret Data" > secret.txt`
2. Change the permissions so that absolutely nobody has access to it:
   `chmod 000 secret.txt`
3. Attempt to `cat` the file through `strace`, but we will filter it to ONLY show `openat` syscalls so the output is cleaner:
   `strace -e trace=openat cat secret.txt`
4. **Analysis:** The output will be very short. Look at the final line:
   `openat(AT_FDCWD, "secret.txt", O_RDONLY) = -1 EACCES (Permission denied)`
5. This is the absolute truth of the failure. The `cat` binary asked the kernel to open the file, and the Linux kernel definitively replied `-1` (Error) and `EACCES` (Permission Denied). 

## Success Criteria
You have successfully completed this practice if you ran a basic command through `strace`, identified the `openat()`, `read()`, and `write()` system calls, and successfully reproduced a kernel-level `EACCES` error!
