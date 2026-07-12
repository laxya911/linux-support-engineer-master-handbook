---
volume: 1
chapter: 5
part: 1
id: V1-C05
title: Linux Filesystem
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Beginner
estimated_time: 2 Hours
reading_time: 45 Minutes
labs: 1
interview_questions: 3
prerequisites: Chapter 4
last_updated: 2026-07
status: In Progress
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 5 — Linux Filesystem

* **Difficulty:** Beginner
* **Estimated Time:** 2 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

In Linux, 'everything is a file.' But where are those files actually stored? Navigating the Filesystem Hierarchy Standard is like learning the map of a new city—once you know the layout, you'll never get lost.

By the end of this chapter, you will be able to:
* Explain the "Everything is a file" philosophy.
* Navigate the Filesystem Hierarchy Standard (FHS) intuitively.
* Identify exactly where configuration files, logs, and binaries are stored.
* Differentiate between persistent storage on disk and virtual filesystems in RAM.

## Visual Architecture: The Filesystem Hierarchy

```mermaid
flowchart TD
    ROOT["/ (Root)"] --> BIN["/bin & /sbin (Core Binaries)"]
    ROOT --> ETC["/etc (Configuration Files)"]
    ROOT --> VAR["/var (Variable Data & Logs)"]
    ROOT --> USR["/usr (Installed Software)"]
    ROOT --> HOME["/home (User Directories)"]
    ROOT --> OPT["/opt (Third-Party Software)"]
    ROOT --> TMP["/tmp (Temporary Files)"]
    ROOT --> DEV["/dev (Device Files)"]
    ROOT --> PROC["/proc & /sys (Virtual Filesystems)"]

    style ROOT fill:#2d3436,stroke:#b2bec3,color:#fff
    style ETC fill:#d63031,stroke:#ff7675,color:#fff
    style VAR fill:#00b894,stroke:#55efc4,color:#fff
    style DEV fill:#f39c12,stroke:#f1c40f,color:#fff
    style PROC fill:#9b59b6,stroke:#8e44ad,color:#fff
```

## Theory & Concepts

### 1. "Everything is a file"
In Linux, almost everything you interact with is represented as a file. A text document is a file. A directory is a file that contains a list of other files. Your hard drive is a file (e.g., `/dev/sda`). Even your network socket or a running process is represented as a file.

Because everything is a file, the same tools you use to read a text document (`cat`, `less`) can often be used to read hardware information.

### 2. The Filesystem Hierarchy Standard (FHS)
Unlike Windows, which assigns drive letters (C:\, D:\), Linux uses a single, unified tree structure starting at the **Root Directory (`/`)**. The FHS dictates exactly where certain types of files must live. If you memorize this, you will never have to guess where something is installed.

#### Core Binaries (`/bin` and `/sbin`)
* `/bin`: Contains essential user commands (like `ls`, `cat`, `echo`).
* `/sbin`: Contains essential system administration commands (like `fdisk`, `reboot`). These typically require `root` privileges.

#### Configuration (`/etc`)
If you need to change how a service behaves, you go here. **Nothing in `/etc` is an executable binary.** It contains purely text-based configuration files (e.g., `/etc/ssh/sshd_config` or `/etc/fstab`). 

#### Variable Data (`/var`)
This directory contains data that frequently changes while the system is running.
* `/var/log`: System and application log files.
* `/var/lib`: Databases (like MySQL or PostgreSQL data).
* `/var/spool`: Mail and print queues.

#### Installed Software (`/usr` and `/opt`)
* `/usr`: The secondary hierarchy for read-only user data. Most user-installed software and libraries live here (e.g., `/usr/bin/python`).
* `/opt`: Optional third-party software that doesn't follow standard Linux packaging conventions (e.g., proprietary enterprise agents or massive self-contained Java apps).

### 3. Virtual Filesystems (`/dev`, `/proc`, `/sys`)
Not everything in the tree exists on the hard drive. Some directories exist entirely in RAM and are generated dynamically by the Linux Kernel.

* `/dev`: Device nodes. When you plug in a USB drive, the kernel creates a file here (like `/dev/sdb`) so software can communicate with it.
* `/proc`: The process information pseudo-filesystem. It contains live data about the system's running processes and hardware state.
* `/sys`: Similar to `/proc`, it provides an interface to kernel data structures and hardware attributes.

## Real-World Scenarios

> [!IMPORTANT]
> **Incident Report & Roleplay**
>
> **👤 End User (Dave):**
> *""I just installed a proprietary monitoring agent, but when I type its command in the terminal, it says 'command not found'. Where did it install?""*
>
> **🧑‍💻 Tech Support (Charlie):**
> - **Mental Map:** You know it is third-party, proprietary software. It likely didn't install to the standard `/usr/bin`.
>
> **👨‍🔧 Junior Admin (Bob):**
> - **The Fix:** You check the `/opt` directory and find `/opt/custom-monitor/`. You run `/opt/custom-monitor/bin/start.sh` directly, and the agent works. You then explain to the customer how to add that directory to their `$PATH`.
>   
>
## Hands-on Lab

> [!NOTE]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 5 Practice Guide](../practice-files/V1-C05-practice.md) to practice navigating the hierarchy and reading live kernel data from the virtual filesystems.

## Interview Questions

### Question 1: What is the difference between `/bin` and `/sbin`?
* **Target Answer**: "Both contain executable binaries. However, `/bin` contains standard commands that any user can run, like `ls` or `mkdir`. `/sbin` contains system binaries intended specifically for the root user to perform administrative tasks, like `fdisk` or `iptables`."

### Question 2: If a web server fails to start, which directory do you check first?
* **Target Answer**: "I would immediately check `/var/log/` (specifically `/var/log/nginx` or `/var/log/httpd`) for error logs to understand why the service is crashing."

### Question 3: Is `/proc/cpuinfo` a file stored on the hard drive?
* **Target Answer**: "No. The `/proc` directory is a virtual, pseudo-filesystem created by the kernel in RAM. When you run `cat /proc/cpuinfo`, the kernel intercepts that read request and dynamically generates text output containing the live hardware specifications."

## Chapter Summary

The Linux Filesystem is highly organized. Configuration goes in `/etc`. Logs go in `/var/log`. Normal software goes in `/usr`, and weird proprietary software goes in `/opt`. The kernel exposes itself through `/proc` and `/sys`. Mastering this layout is the difference between blindly searching a server and surgically navigating it.

## Completion Checklist

- [ ] I can explain why `/etc` contains no executable files.
- [ ] I know exactly where to look for application log files.
- [ ] I understand that `/proc` exists only in memory, not on disk.

---

## Navigation

⬅ Previous:
[Chapter 4 – Linux Boot Process](V1-C04-linux-boot-process.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 6 – Working with Files & Directories](V1-C06-working-with-files-and-directories.md)
