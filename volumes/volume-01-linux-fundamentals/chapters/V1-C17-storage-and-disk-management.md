---
volume: 1
chapter: 17
part: 1
id: V1-C17
title: Storage & Disk Management
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Intermediate
estimated_time: 2 Hours
reading_time: 45 Minutes
labs: 1
interview_questions: 3
prerequisites: Chapter 16
last_updated: 2026-07
status: In Progress
---

# Chapter 17 — Storage & Disk Management

* **Difficulty:** Intermediate
* **Estimated Time:** 2 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

By the end of this chapter, you will be able to:
* Map the physical and logical layout of disks using `lsblk`.
* Identify a 100% full hard drive using `df -h`.
* Hunt down massive files causing storage outages using `du -sh`.
* Understand the concept of Mount Points and `/etc/fstab`.

## Visual Architecture: The Anatomy of Storage

In Windows, you plug in a hard drive and it becomes the `D:\` drive. In Linux, there are no drive letters. A physical block device is partitioned, formatted, and then **mounted** to an arbitrary folder on the system.

```mermaid
flowchart TD
    A["Physical Block Device (/dev/sda)"] -->|Partitioned| B["Partition (/dev/sda1)"]
    B -->|Formatted| C["Filesystem (ext4 / xfs)"]
    C -->|Mounted via /etc/fstab| D["Mount Point (/)"]
    
    style A fill:#2d3436,stroke:#b2bec3,color:#fff
    style B fill:#0984e3,stroke:#74b9ff,color:#fff
    style C fill:#f39c12,stroke:#f1c40f,color:#000
    style D fill:#d63031,stroke:#ff7675,color:#fff
```

## Theory & Concepts

### 1. `lsblk` (List Block Devices)
A block device is a physical (or virtual) hard drive. 
Running `lsblk` shows you a hierarchical tree of all disks attached to the server. 
* `/dev/sda`: The first hard drive.
* `/dev/sda1`: The first partition on the first hard drive.
* `/dev/sdb`: The second hard drive.

### 2. `df` (Disk Free)
When a server starts crashing randomly, the very first thing a Support Engineer does is check if the hard drive is full.
* `df -h`: The `-h` flag stands for **Human-readable**. It prints the sizes in Megabytes (M) and Gigabytes (G) instead of raw bytes. 
* Look closely at the `Use%` column. If a partition says `100%`, the server is dead in the water.

### 3. `du` (Disk Usage)
If `df -h` tells you the disk is full, `du` is the weapon you use to hunt down *why* it is full.
* `du -sh *`: This is a mandatory troubleshooting command. 
  * `-s`: **Summarize** (only show the total size of each directory, don't list every single file inside).
  * `-h`: **Human-readable**.
  * `*`: Run this against everything in the current directory.

### 4. Mount Points and `/etc/fstab`
Because Linux has no drive letters, everything exists under the single Root directory (`/`). 
You can take a massive 10 Terabyte hard drive (`/dev/sdb1`) and mount it to the `/var/log` directory. Now, whenever the system writes a log file, it is transparently writing it to the second hard drive.
* `/etc/fstab` (File System Table): This configuration file tells the Linux Kernel which partitions belong to which mount points so they connect automatically on boot.

## Real-World Scenarios

**Customer:**
*"Our MySQL database suddenly crashed. When we try to restart it using `systemctl`, it says 'No space left on device'. Please help!"*

How should a Linux Support Engineer investigate?
* **Diagnosis:** The hard drive is 100% full. The database cannot write to the disk, so it crashed.
* **Investigation:** 
  1. The engineer runs `df -h` and confirms that the Root partition (`/`) is at `100%` usage.
  2. The engineer `cd`s into the root directory (`cd /`).
  3. They run `sudo du -sh *`. They see that the `/var` directory is 90GB.
  4. They `cd /var` and run `sudo du -sh *` again. They see `/var/log` is 85GB.
  5. They `cd /var/log` and find a single file named `error.log` that is 85GB in size.
* **The Fix:** The engineer deletes the runaway log file using `rm error.log`. They run `df -h` again and see usage drop to `15%`. They restart the database via `systemctl restart mysql`, and the service is restored.

## Hands-on Lab

> [!CAUTION]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 17 Practice Guide](../practice-files/V1-C17-practice.md). You will map your virtual machine's block devices and practice hunting for large directories.

## Interview Questions

### Question 1: A customer complains their server is slow. You run `df -h` and see `/dev/sda1` is at 100% usage. What command do you use to figure out which specific folder is consuming the most space?
* **Target Answer**: "I would navigate to the root directory and run `du -sh *`. This will summarize the total disk usage of every top-level folder in human-readable format. I would then identify the largest folder, `cd` into it, and repeat the command until I isolate the massive files."

### Question 2: What is the purpose of the `/etc/fstab` file?
* **Target Answer**: "The File System Table (`fstab`) is read by the system during the boot process. It maps physical block devices or partitions (like `/dev/sdb1`) to logical Mount Points (like `/data`), ensuring that extra hard drives are mounted automatically on startup."

### Question 3: Why should you always use the `-h` flag with commands like `df` and `du`?
* **Target Answer**: "The `-h` flag stands for 'Human-readable'. Without it, the commands output sizes in raw bytes or 1K-blocks, which are extremely difficult to read quickly when dealing with gigabytes or terabytes of data during an emergency."

## Chapter Summary

Running out of disk space is one of the most common causes of server outages. Remember the workflow: use `lsblk` to understand the physical layout, `df -h` to confirm the outage, and `du -sh *` to hunt down the files responsible.

## Completion Checklist

- [ ] I understand that Linux uses Mount Points instead of drive letters like `C:\`.
- [ ] I can check if my hard drive is 100% full using `df -h`.
- [ ] I know how to summarize folder sizes using `du -sh *`.

---

## Navigation

⬅ Previous:
[Chapter 16 – Archiving and Compression](V1-C16-archiving-and-compression.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 18 – Advanced Grep & Awk](V1-C18-advanced-grep-and-awk.md)
