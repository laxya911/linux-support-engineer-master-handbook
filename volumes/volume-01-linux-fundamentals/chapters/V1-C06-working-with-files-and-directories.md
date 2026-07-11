---
volume: 1
chapter: 6
part: 1
id: V1-C06
title: Working with Files & Directories
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Beginner
estimated_time: 2 Hours
reading_time: 40 Minutes
labs: 1
interview_questions: 2
prerequisites: Chapter 5
last_updated: 2026-07
status: In Progress
---

# Chapter 6 — Working with Files & Directories

* **Difficulty:** Beginner
* **Estimated Time:** 2 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 2

## Learning Objectives

By the end of this chapter, you will be able to:
* Create, copy, move, and delete files and directories confidently.
* Differentiate between viewing static files (`cat`, `less`) and streaming live files (`tail -f`).
* Understand and create Symbolic Links (Soft Links) to alias files across the filesystem.

## Visual Architecture: Symbolic Links

A **Symbolic Link** (or symlink) is a special file that acts as a shortcut to another file. If you delete the symlink, the target file is safe. If you delete the target file, the symlink breaks.

```mermaid
flowchart LR
    A["Symlink File (e.g., /tmp/shortcut.conf)"] -.->|"Points to Path"| B["Target File (e.g., /etc/nginx/nginx.conf)"]
    B --> C["('Hard Drive Inode')"]
    
    style A fill:#0984e3,stroke:#74b9ff,color:#fff
    style B fill:#2d3436,stroke:#b2bec3,color:#fff
    style C fill:#d63031,stroke:#ff7675,color:#fff
```

## Theory & Concepts

### 1. Creation and Deletion
* `touch <file>`: Creates an empty file or updates its timestamp if it already exists.
* `mkdir <dir>`: Creates a directory. Use `-p` to create nested directories (e.g., `mkdir -p /app/logs/2026`).
* `rm <file>`: Deletes a file permanently. Linux has no Recycle Bin.
* `rm -r <dir>`: Deletes a directory and everything inside it. 

> [!CAUTION]
> **Senior Engineer Warning**
> Never run `rm -rf /` or `rm -rf *` blindly. Always verify your current directory using `pwd` before running a recursive delete.

### 2. Copying and Moving
* `cp <source> <destination>`: Copies a file. Use `cp -r` for directories.
* `mv <source> <destination>`: Moves a file. Interestingly, `mv` is also used to rename files. If you type `mv oldname.txt newname.txt`, the file is renamed instantly.

### 3. Viewing Files
As a Support Engineer, you will spend 80% of your time reading configuration and log files.
* `cat <file>`: Dumps the entire file to the screen. Good for short files.
* `less <file>`: Opens the file in an interactive pager. You can scroll up/down and search by typing `/keyword`. Press `q` to exit.
* `head <file>`: Shows the first 10 lines of a file.
* `tail <file>`: Shows the last 10 lines of a file.

**The Golden Command: `tail -f`**
When troubleshooting, you don't just want to see the end of a log file; you want to watch it update in real-time while a user tries to log in.
* `tail -f /var/log/syslog` will lock onto the file and stream new log entries live to your terminal. Press `Ctrl + C` to stop.

### 4. Linking
Sometimes a script expects a file to be in `/usr/local/bin`, but you installed it in `/opt`. Instead of copying the binary and wasting space, you create a link.
* **Symbolic Link (`ln -s <target> <link_name>`)**: Creates a shortcut. 
* **Hard Link (`ln <target> <link_name>`)**: Points directly to the data on the disk (the inode). Rarely used by beginners, but crucial to know they exist.

## Real-World Scenarios

**Customer:**
*"Our application is crashing when it starts up. The developer says we need to watch the application log while they trigger the script."*

How should a Linux Support Engineer investigate?
* **Action:** You SSH into the server and type `tail -f /var/log/myapp/error.log`. 
* **Observation:** As the developer triggers the script, you instantly see: `ERROR: Cannot write to /tmp/myapp.lock - Permission denied`.
* **The Fix:** Because you watched the log in real-time, you caught the exact error without having to dig through millions of lines of historical logs.

## Hands-on Lab

> [!NOTE]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 6 Practice Guide](../practice-files/V1-C06-practice.md) to practice linking files and watching log streams.

## Interview Questions

### Question 1: What is the difference between `cat` and `less`?
* **Target Answer**: "`cat` prints the entire contents of a file to standard output at once, which makes it terrible for reading large log files. `less` opens the file in a paginated view, allowing you to scroll, search, and consume the file without flooding your terminal."

### Question 2: What happens if you delete the target of a symbolic link?
* **Target Answer**: "The symbolic link becomes a 'broken link' or an 'orphan'. It will still exist in the filesystem, but attempting to read or execute it will result in a 'No such file or directory' error, because the path it points to no longer exists."

## Chapter Summary

The ability to swiftly manipulate the filesystem is the foundation of Linux administration. Creating, copying, moving, and deleting files are the nouns and verbs of your daily job. Furthermore, mastering `tail -f` will drastically reduce your time-to-resolution during live outages. 

## Completion Checklist

- [ ] I can create and safely delete directories.
- [ ] I understand the difference between renaming a file and moving it.
- [ ] I can use `tail -f` to monitor logs in real-time.

---

## Navigation

⬅ Previous:
[Chapter 5 – Linux Filesystem](V1-C05-linux-filesystem.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 7 – Text Editors (nano & vim)](V1-C07-text-editors.md)
