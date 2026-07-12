---
volume: 2
chapter: 18
part: 5
id: V2-C18
title: System Backup & Restoration (rsync)
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Intermediate
estimated_time: 1.5 Hours
reading_time: 30 Minutes
labs: 1
interview_questions: 3
prerequisites: V2-C17
last_updated: 2026-07
status: In Progress
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 18 — System Backup & Restoration (rsync)


## Learning Objectives

By the end of this chapter, you will be able to:
* Explain the 3-2-1 Backup Rule.
* Understand why `rsync` is vastly superior to `cp` or `tar` for network backups.
* Execute an `rsync` command over SSH to push or pull data.
* Recover deleted files from a remote backup server.


> [!IMPORTANT]
> **ServiceNow Ticket: INC-88267**
> **Priority:** High
> **Reported By:** Enterprise Application Team
> **Issue:** We are experiencing a critical failure related to System Backup & Restoration (rsync). Please investigate immediately.
> 
> **Support Engineer Objective:** Use operational thinking to collect evidence, identify the root cause, and restore service without causing further disruption.

## Visual Architecture: The Delta Transfer

If you have a 100GB database file and you change a single 5MB table, the `cp` command will copy the entire 100GB file again. This is impossible to scale. 
`rsync` is brilliant. It compares the cryptographic hashes of the files on both servers, calculates exactly which blocks changed (the "delta"), and only transmits those modified blocks over the network.

```mermaid
flowchart LR
    A["Production Server \n (100GB File)"] -->|"Calculates Hashes"| B{"rsync"}
    
    C["Backup Server \n (100GB File)"] -->|"Calculates Hashes"| B
    
    B -->|"Only 5MB differs!"| D["Transmits 5MB Delta over SSH"]
    
    style A fill:#0984e3,stroke:#74b9ff,color:#fff
    style B fill:#f39c12,stroke:#f1c40f,color:#000
    style C fill:#00b894,stroke:#55efc4,color:#000
    style D fill:#d63031,stroke:#ff7675,color:#fff
```

## Theory & Concepts

### 1. The 3-2-1 Rule
Every Support Engineer must memorize the golden rule of backups:
* **3** Copies of your data.
* **2** Different physical media (e.g., SSD and Tape, or AWS and Azure).
* **1** Copy stored completely offsite.
If you do not follow this rule, you do not actually have a backup; you just have an illusion of safety.

### 2. The `rsync` Command
`rsync` is the industry standard for synchronizing files between servers. 
The standard flags are `-avz`:
* `-a` (Archive): Preserves all permissions, owners, and symlinks.
* `-v` (Verbose): Prints what it is doing to the screen.
* `-z` (Compress): Compresses the data during network transit.

**To push data to a backup server:**
`rsync -avz /var/www/html/ backupuser@10.0.0.50:/backups/website/`

**To pull data from a backup server:**
`rsync -avz backupuser@10.0.0.50:/backups/website/ /var/www/html/`

## Scenario-Based Troubleshooting

### Scenario A: The Accidental Deletion
**The Incident:** A junior engineer is tasked with cleaning up some old temporary files in the `/etc/nginx/conf.d/` directory. They type `rm -rf *` to delete the files, but they don't realize they are actually sitting in the main `/etc/nginx/` folder. 
They accidentally delete the entire Nginx configuration for the company's production website. The website goes down immediately. Panic ensues.

**The Investigation & Fix:**

1. The Support Engineer receives the frantic phone call. "I deleted the web config!"
2. The engineer stays calm. "We follow the 3-2-1 rule," they say. "A cronjob runs `rsync` every 15 minutes to our backup server."
3. The engineer logs into the production web server. They do not use `cp` or `tar`. They need the files restored exactly as they were, with the exact same `root` permissions and SELinux contexts.
4. The engineer runs a targeted `rsync` pull command:
   `rsync -avz root@backup-server:/backups/nginx/ /etc/nginx/`
5. `rsync` connects over SSH. It sees that `/etc/nginx/` on the production server is completely empty, so it safely transmits all the missing files.
6. Because the engineer used the `-a` (archive) flag, all file permissions are perfectly restored. 
7. The engineer runs `systemctl restart nginx`. The website is back online in less than 2 minutes.


## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 18 Practice Guide](../practice-files/V2-C18-practice.md) to practice synchronizing a local directory and witnessing the magic of Delta transfers!

## Interview Questions

### Question 1: What makes `rsync` fundamentally better than `scp` or `cp` for daily automated backups?
* **Target Answer**: "`scp` and `cp` are dumb copying tools; they will copy the entire file every single time they are run. `rsync` uses a delta-transfer algorithm. It compares the source and destination, and only transmits the specific blocks of data that have changed. This reduces network bandwidth and backup time from hours to seconds."

### Question 2: Explain the 3-2-1 Backup Rule.
* **Target Answer**: "The 3-2-1 rule states that you must maintain 3 copies of your data, stored on 2 different types of storage media, with at least 1 copy located physically offsite (like a separate cloud provider or geographical region) to protect against site-wide disasters."

### Question 3: In the command `rsync -avz`, what does the `-a` flag do, and why is it critical for Linux system backups?
* **Target Answer**: "The `-a` flag stands for 'Archive' mode. It is actually a combination of several flags that tell `rsync` to recursively copy directories while strictly preserving all symlinks, file permissions, ownership (UID/GID), and modification times. This is critical for system backups because restoring an application with incorrect file permissions will usually cause the application to crash."

## Chapter Summary

Accidents happen. Hard drives fail. Hackers deploy ransomware. The only thing standing between a company and total bankruptcy is a tested, reliable backup strategy. Master `rsync`, schedule it in `cron`, and sleep soundly knowing your data is safe.

## Completion Checklist

- [ ] I can recite the 3-2-1 Backup Rule.
- [ ] I understand how the `rsync` Delta algorithm saves bandwidth.
- [ ] I can write an `rsync` command to push data to a remote server.

---

## Navigation

← Previous: [Chapter 17 — Cron & Task Scheduling](V2-C17-cron-and-task-scheduling.md)

↑ Volume Contents: [Table of Contents](TOC.md)

→ Next: [Chapter 19 — Incident Response Methodology](V2-C19-incident-response.md)
