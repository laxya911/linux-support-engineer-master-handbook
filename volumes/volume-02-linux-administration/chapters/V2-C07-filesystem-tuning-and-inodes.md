---
volume: 2
chapter: 7
part: 2
id: V2-C07
title: Filesystem Tuning and Inodes
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Advanced
estimated_time: 1.5 Hours
reading_time: 30 Minutes
labs: 1
interview_questions: 3
prerequisites: V2-C06
last_updated: 2026-07
status: In Progress
---

# Chapter 7 — Filesystem Tuning and Inodes

* **Difficulty:** Advanced
* **Estimated Time:** 1.5 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

By the end of this chapter, you will be able to:
* Define what an Inode is and how the Linux Kernel uses it.
* Differentiate between `df -h` (Disk Space) and `df -i` (Inode Space).
* Troubleshoot "No space left on device" errors caused by Inode exhaustion.
* Understand the `ext4` reserved block percentage.

## Visual Architecture: The Library Card Catalog

Think of a hard drive like a physical library. The physical books take up space (Disk Space). But to find the books, the librarian uses a card catalog. Every single book needs exactly one index card. The index card holds the metadata (the title, the author, where the book is located on the shelf). 
In Linux, the index card is called an **Inode**.

```mermaid
flowchart LR
    A["User types: \n cat /var/log/syslog"] --> B{"Kernel asks Filesystem: \n 'Where is syslog?'"}
    
    B -->|Checks Inode Table| C["Inode #12345 \n Owner: root \n Permissions: 640 \n Block Location: Sector 9"]
    
    C -->|Reads physical disk| D[("Hard Drive \n (Sector 9)")]
    
    D -->|Returns text| A
    
    style A fill:#0984e3,stroke:#74b9ff,color:#fff
    style B fill:#f39c12,stroke:#f1c40f,color:#000
    style C fill:#00b894,stroke:#55efc4,color:#000
    style D fill:#2d3436,stroke:#b2bec3,color:#fff
```

## Theory & Concepts

### 1. The Anatomy of an Inode
An Inode (Index Node) is a data structure on a filesystem that stores all the information *about* a file, except for its name and its actual data. 
It stores:
* The file's size
* The file's owner (UID) and group (GID)
* The read/write/execute permissions (`chmod`)
* The exact physical location on the hard drive where the data begins.

### 2. The Hard Limit
When you format a hard drive with the `ext4` filesystem, Linux calculates the size of the drive and creates a fixed, permanent number of Inodes. 
* 1 File = 1 Inode. 
* 1 Directory = 1 Inode.
If a partition is given 10,000,000 Inodes, you can only ever create 10 million files on that drive, regardless of how small they are.

### 3. Reserved Blocks
By default, `ext4` reserves 5% of all disk space exclusively for the `root` user. If a regular user fills the drive to 100%, `root` can still log in and use that hidden 5% to delete files and save the server.

## Scenario-Based Troubleshooting

### Scenario A: The Inode Exhaustion
**The Incident:** A customer's e-commerce website goes offline. The web browser shows a fatal PHP error: `Warning: session_write_close(): write failed: No space left on device (28)`. 
The customer panics and buys a larger hard drive. They contact Support and say, "My server says it is out of space, but when I run `df -h`, it says my hard drive is only 40% full! Your servers are broken!"

**The Investigation & Fix:**
1. The Support Engineer logs in. They run `df -h`. The customer is correct; the drive has 60% free physical space.
2. The engineer knows the secret. They run the Inode command:
   `df -i`
3. The output shows `IUse%: 100%`. 
4. The engineer understands the problem: The physical hard drive has plenty of room, but the filesystem has run out of index cards. 
5. What causes this? It is always caused by an application creating millions of tiny, 1-kilobyte files. The files don't consume much physical gigabyte space, but each file consumes exactly 1 Inode.
6. The engineer hunts for the directory holding the most files using a specialized command:
   `find / -xdev -type d -size +100k` *(or a similar script to count files per directory)*.
7. They discover that `/var/lib/php/sessions/` contains 4.5 million old, abandoned session files. A cron job meant to delete old sessions had failed a year ago.
8. The engineer deletes the millions of tiny files (`find /var/lib/php/sessions -type f -delete`).
9. The engineer runs `df -i` again. Inode usage drops to 5%. The website instantly comes back online.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 7 Practice Guide](../practice-files/V2-C07-practice.md) to inspect your own VM's Inode limits.

## Interview Questions

### Question 1: An application crashes with a "No space left on device" error. You check `df -h` and verify there is over 100GB of free space. What is the next command you should run?
* **Target Answer**: "I would run `df -i`. The error indicates that the filesystem cannot write new data. If physical block space is available, the filesystem has likely exhausted its supply of Inodes. Every file requires one Inode, so a runaway script generating millions of tiny files will exhaust the Inode pool before it exhausts the physical disk capacity."

### Question 2: What information is stored inside an Inode?
* **Target Answer**: "An Inode stores the metadata of a file. This includes the file's owner, group, access permissions, timestamps, file size, and the pointers to the physical blocks on the hard drive where the actual data resides. Notably, the Inode does *not* store the file's name (which is stored in the directory table) or the actual file content."

### Question 3: By default, the `ext4` filesystem reserves 5% of the disk space. What is the purpose of this reserved space?
* **Target Answer**: "The reserved space is held exclusively for the `root` user and critical system processes. If a runaway application or user fills the hard drive to 100%, the system will not crash. The `root` user can still log in, utilize the reserved 5% to execute commands, and delete files to resolve the emergency."

## Chapter Summary

The `df -h` command only tells you half the story. The physical size of the files matters, but the *quantity* of the files matters just as much. If you ever see "No space left on device," run `df -h`, and then immediately run `df -i`. 

## Completion Checklist

- [ ] I can define what an Inode is.
- [ ] I know the command to check Inode usage (`df -i`).
- [ ] I understand how millions of tiny files can crash a server.

---

## Navigation

⬅ Previous:
[Chapter 6 – Network Attached Storage](V2-C06-network-attached-storage.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 8 – Static IP Configuration *[Coming Soon]*](#)
