---
volume: 1
chapter: 2
part: 1
id: V1-C02
title: Linux Architecture & Distributions
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Beginner
estimated_time: 2 Hours
reading_time: 45 Minutes
labs: 1
interview_questions: 2
prerequisites: Chapter 1
last_updated: 2026-07
status: In Progress
---

# Chapter 2 — Linux Architecture & Distributions

* **Difficulty:** Beginner
* **Estimated Time:** 2 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 2

*"You cannot troubleshoot what you don't understand."*

## Learning Objectives

By the end of this chapter, you will be able to:
* Explain the architecture of a Linux operating system.
* Understand how users interact with the kernel.
* Describe what happens when a command is executed.
* Explain system calls.
* Understand why processes crash and how memory is allocated.
* Explain the Linux boot sequence at a high level.
* Understand where troubleshooting begins.

## Introduction: Why Linux Architecture Matters

Most beginners learn Linux like this: they memorize commands (`ls`, `cd`, `cp`, `mv`, `systemctl`, `journalctl`).

Professional engineers ask different questions.

When troubleshooting, you must first ask: **Where is the crash happening?**
* Application?
* Library?
* Kernel?
* Filesystem?
* Memory?
* CPU?
* Hardware?
* Network?

To answer those questions, you must understand Linux architecture.

## Linux Is Like a City

Imagine Linux as a modern city. Every request travels through these layers. Understanding those layers is the foundation of troubleshooting.

```text
                 USER
    Chrome, Firefox, SSH, Nginx, MySQL, Python, Docker, Bash
-----------------------------
        User Space
-----------------------------
      System Libraries
-----------------------------
      System Calls
-----------------------------
          Kernel
-----------------------------
      Hardware Drivers
-----------------------------
   CPU, RAM, SSD, NIC, GPU
```

## The Four Major Layers

Linux consists of four primary layers: **User → Applications → Kernel → Hardware**. Let's examine each one.

### Layer 1 — User Space

Everything you interact with lives here (e.g., Bash, Firefox, SSH client, Nginx, Docker). Applications cannot directly access hardware. They must request access from the kernel. This separation protects the operating system.

> [!NOTE]
> **Windows ↔ Linux Comparison**
> In Windows, the equivalent flow is: `Applications → Windows API → Windows Kernel → Hardware`. The concept is highly similar.

### Layer 2 — System Libraries

Applications rarely talk directly to the kernel. Instead, they use libraries (e.g., `glibc`, `OpenSSL`, `libpthread`, `zlib`). Think of a library as a translator. Instead of every program knowing how to communicate with the kernel, the library handles it.

**Real Example:** You type `cat test.txt`. The `cat` program doesn't know how to read a disk directly. Instead, the flow is:
`cat → glibc → System Call → Kernel → Disk`

### Layer 3 — System Calls

This is one of the most important concepts. A system call is simply a request from a program asking the kernel to perform a privileged operation.

Every application depends on them: reading a file, writing a file, creating a process, allocating memory, opening a network socket, mounting a disk.
*Common system calls include: `open()`, `read()`, `write()`, `close()`, `fork()`, `execve()`, `socket()`, `connect()`, `accept()`, `mmap()`, `clone()`.*

### Layer 4 — Kernel

The kernel is the heart of Linux. Everything depends on it. If the kernel stops, Linux stops.
Responsibilities include: CPU scheduling, memory management, process management, device drivers, networking, filesystems, security, and system calls.

> [!TIP]
> **The Kernel Is Like a Traffic Police Officer**
> Imagine thousands of applications, millions of operations, and only one CPU. The kernel decides which process runs, when, for how long, how much RAM it receives, which files it can access, and which network packets are allowed.

## Hardware Layer

Hardware includes the CPU, Memory, SSD/HDD, Network Interface Card (NIC), GPU, and USB devices. The kernel communicates with hardware through device drivers. Without the correct driver, the hardware may not function properly.

## How a Command Really Works

Let's follow a simple command: `ls`. What actually happens?

1. **Keyboard** input is sent.
2. **Shell** receives input.
3. **Shell searches PATH** and loads `/bin/ls`.
4. **Creates Process**.
5. **Kernel allocates memory**.
6. **Kernel schedules CPU**.
7. **ls requests directory contents**.
8. **Kernel reads filesystem**.
9. **Kernel returns data**.
10. **Terminal displays result**.

This entire process usually completes in milliseconds.

## Processes & Memory

Everything running on Linux is represented as a process (`bash`, `systemd`, `sshd`, `nginx`, `mysql`). Each process has a Process ID (PID), Parent Process ID (PPID), User, Memory allocation, and Open files.

#### Process Lifecycle
`Created → Ready → Running → Sleeping → Waiting → Stopped → Terminated`

Support engineers often investigate processes that become stuck in one of these states. Every running process needs memory (Code, Data, Heap, Stack, Shared memory). When available memory becomes scarce, Linux may use swap space or invoke the Out-Of-Memory (OOM) Killer to terminate processes.

> [!IMPORTANT]
> **Senior Engineer Thinking**
> **Customer**: *"The server rebooted itself."*
> A beginner says: *"Hardware problem?"*
> A senior engineer considers: *Kernel panic? OOM Killer? Power issue? Hypervisor restart? Watchdog timer? Cloud maintenance event?* Multiple hypotheses are explored before conclusions are drawn.

## The Linux Boot Process

At a high level, Linux starts by loading the kernel through a bootloader before handing control to `systemd`. We'll examine every stage of this process in detail in **V1-C18 – Linux Boot Process**.

> [!CAUTION]
> **Common Beginner Mistakes**
> ❌ Rebooting before collecting evidence.
> ❌ Assuming every issue is application-related.
> ❌ Ignoring logs.
> ❌ Treating symptoms instead of identifying root causes.
> ❌ Restarting services without understanding why they failed.

## Real-World Scenarios

**Customer:**
*"My application freezes whenever it accesses a file."*

How should a Linux Support Engineer investigate?
* **Which logs?** Check `dmesg` or `journalctl` for I/O errors or filesystem corruption.
* **Which services?** Check if network storage mounts (NFS/CIFS) are hanging.
* **Which commands?** Use `strace` on the frozen application process, or `df -h` / `iostat` to check storage availability and latency.
* **Expected troubleshooting workflow:** Determine if the process is stuck in Uninterruptible Sleep (D state) waiting for the kernel/disk, then trace the storage path.

## Hands-on Lab

> [!NOTE]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 2 Practice Guide](../practice-files/V1-C02-practice.md) to explore the system architecture and observe system calls.

### Lab 2.1: Exploring the System Architecture

#### Objective
Familiarize yourself with the system's architecture, processes, and memory.

#### Step-by-Step Instructions

1. **Explore the Running System**
   ```bash
   $ uname -a
   $ hostnamectl
   $ cat /etc/os-release
   ```
   *Questions*: Which kernel version are you running? Which Ubuntu release is installed? What architecture (x86_64, ARM) is the system using?

2. **Inspect Processes**
   ```bash
   $ ps -ef
   $ top
   ```
   *Observe*: PID, PPID, User, CPU usage, and Memory usage.

3. **Explore Memory**
   ```bash
   $ free -h
   $ cat /proc/meminfo
   ```
   *Questions*: How much RAM is installed? How much is currently available? Is swap enabled?

4. **Observe System Calls (Preview)**
   ```bash
   $ strace ls
   ```
   Don't worry about understanding every line yet. Notice that even a simple command generates many system calls.

## Interview Questions

### Question 1: What happens when you execute ls?
**Scenario**: You are asked this during an interview to gauge your architectural depth.
* **Target Answer**: "The shell parses the command, searches the executable in the PATH, creates a new process, the kernel schedules it, the process requests directory information through system calls, the kernel retrieves the data from the filesystem, and the results are returned to the terminal."

### Question 2: Why can't user-space applications access hardware directly?
* **Target Answer**: For security and stability. User space is separated from the kernel to ensure that a crashing application or malicious code cannot directly manipulate hardware or memory belonging to other processes. Applications must request privileged operations via system calls.

## Chapter Summary

You learned that Linux is organized into layers: user space, libraries, system calls, kernel, and hardware. Applications rely on the kernel to access system resources, and every command creates one or more processes. Understanding where a failure occurs is the first step toward effective troubleshooting, transforming it from trial-and-error into logical investigation.

## Cheat Sheet

Remember this flow:
`User → Application → System Libraries → System Calls → Kernel → Device Drivers → Hardware`

When something fails, your first task is not to fix it. Your first task is to identify which layer is failing. That single habit will make your troubleshooting faster, more accurate, and more professional.

## Completion Checklist

- [ ] I can describe the 4 major layers of Linux architecture.
- [ ] I understand the role of System Calls.
- [ ] I know the difference between User Space and Kernel Space.
- [ ] I completed Lab 2.1 and reviewed the `strace` output.

---

## Navigation

⬅ Previous:
[Chapter 1 – Welcome to Linux Support Engineering](V1-C01-welcome-to-linux-support-engineering.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 3 – Provisioning Linux](V1-C03-provisioning-linux.md)
