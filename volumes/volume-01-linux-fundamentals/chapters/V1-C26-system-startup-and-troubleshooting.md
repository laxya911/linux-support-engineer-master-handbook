---
volume: 1
chapter: 26
part: 1
id: V1-C26
title: System Startup & Troubleshooting
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Advanced
estimated_time: 2 Hours
reading_time: 45 Minutes
labs: 1
interview_questions: 3
prerequisites: Chapter 25
last_updated: 2026-07
status: In Progress
---

# Chapter 26 — System Startup & Troubleshooting

* **Difficulty:** Advanced
* **Estimated Time:** 2 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

By the end of this chapter, you will be able to:
* Identify the 4 main stages of the Linux boot sequence.
* Query the boot logs using `journalctl -b`.
* Identify silent service failures using `systemctl --failed`.
* Troubleshoot and escape from the dreaded "Emergency Mode".

## Visual Architecture: The Boot Sequence

When you press the power button, Linux does not instantly appear. It hands control through four distinct software layers. If any layer fails, the server crashes.

```mermaid
flowchart TD
    A["1. BIOS / UEFI (Hardware)"] -->|"Loads Bootloader"| B["2. GRUB (Bootloader)"]
    
    B -->|"Loads Kernel into RAM"| C["3. The Linux Kernel"]
    
    C -->|"Starts the first process (PID 1)"| D["4. systemd (Init System)"]
    
    D -->|"Mounts drives & starts services"| E["Login Prompt"]
    
    style A fill:#2d3436,stroke:#b2bec3,color:#fff
    style B fill:#0984e3,stroke:#74b9ff,color:#fff
    style C fill:#f39c12,stroke:#f1c40f,color:#000
    style D fill:#00b894,stroke:#55efc4,color:#000
```

## Theory & Concepts

### 1. The 4 Stages of Boot
1. **BIOS / UEFI**: The motherboard wakes up, checks the RAM and CPU, and looks for a hard drive.
2. **GRUB**: The Grand Unified Bootloader. It presents a menu (if you have a monitor plugged in) asking which operating system you want to load.
3. **The Kernel**: The core of Linux wakes up, takes control of the CPU and RAM, and mounts the root filesystem as Read-Only.
4. **systemd**: The Kernel starts the very first program (Process ID 1), which is `systemd`. `systemd` remounts the hard drive as Read/Write, turns on the network, and starts all your services (like Nginx, SSH, and Cron).

### 2. Reading the Boot Log
When a server reboots, all the text that flies by on the screen is saved into the journal.
* `journalctl -b`: Prints the logs generated *only* during the most recent boot cycle.
* `journalctl -b -1`: Prints the logs from the *previous* boot cycle (useful if the server crashed and you just restarted it).

### 3. Silent Failures
Sometimes a server boots perfectly, but a specific service fails silently in the background.
* `systemctl --failed`: This command instantly lists any service that attempted to start during boot but crashed. 

## Scenario-Based Troubleshooting

### Scenario A: The `fstab` Crash (Emergency Mode)
**The Incident:** A junior engineer adds a new hard drive to the server and edits `/etc/fstab` to make it mount automatically on boot. They make a typo. They reboot the server. The server never comes back online. The console says: `Welcome to Emergency Mode! Root password required for maintenance.`

**The Investigation & Fix:**
1. The engineer types the root password to access the restricted terminal.
2. They run `journalctl -xb` (the `-x` provides extra explanation).
3. Scanning the red text, they see: `Dependency failed for /data. Failed to mount /data.`
4. They realize the `/etc/fstab` file is broken. But the hard drive is currently in a "Read-Only" safety state.
5. They force the drive into Read/Write mode: `mount -o remount,rw /`
6. They open the file: `nano /etc/fstab`
7. They spot the typo (`/dev/sdb11` instead of `/dev/sdb1`), fix it, save the file, and type `reboot`. The server boots perfectly.

### Scenario B: The Port Conflict
**The Incident:** A server reboots for routine updates. When it comes back online, the customer's web application is down. 

**The Investigation & Fix:**
1. The engineer SSHs into the server and checks for silent failures: `systemctl --failed`.
2. The output shows that `nginx.service` failed to start.
3. The engineer checks the status: `systemctl status nginx`. The log explicitly says: `[emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)`.
4. The engineer knows Port 80 is stolen. They run `ss -tulpn | grep 80`.
5. The output shows that `apache2` is running on Port 80. Another user accidentally installed Apache, which is configured to start automatically on boot, stealing Nginx's port.
6. The engineer runs `systemctl disable --now apache2` to kill it permanently, and then `systemctl start nginx`. The website is restored.

## Hands-on Lab

> [!CAUTION]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 26 Practice Guide](../practice-files/V1-C26-practice.md). You will audit your own VM for silent boot failures and parse your current boot log.

## Interview Questions

### Question 1: What is the very first process started by the Linux Kernel during the boot sequence, and what is its PID?
* **Target Answer**: "The first process started by the kernel is the init system, which on modern Linux distributions is `systemd`. It is always assigned Process ID (PID) 1. Every other process on the system is a child of `systemd`."

### Question 2: A server drops into Emergency Mode during boot. You try to edit a configuration file using `nano`, but the system says 'Read-only file system'. How do you fix this?
* **Target Answer**: "During Emergency Mode, the root filesystem is often mounted as read-only to prevent further corruption. To edit files, you must remount the filesystem with read and write permissions by executing `mount -o remount,rw /`."

### Question 3: How can you quickly check if any background services failed to start during the boot process?
* **Target Answer**: "I would run `systemctl --failed`. This command filters the `systemd` unit list and only outputs services that attempted to launch but entered a failed state."

## Chapter Summary

The boot sequence is not magic; it is a predictable chain of four events. If the server crashes, use `journalctl -xb` to find the broken link in the chain. If the server boots but an application is down, use `systemctl --failed` to hunt down the silent error. 

## Completion Checklist

- [ ] I can name the 4 stages of the Linux boot process.
- [ ] I know how to view logs for the current boot cycle (`journalctl -b`).
- [ ] I understand the command needed to escape a Read-Only emergency state.

---

## Navigation

⬅ Previous:
[Chapter 25 – DNS & Name Resolution](V1-C25-dns-and-name-resolution.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 27 – Introduction to Web Servers](V1-C27-introduction-to-web-servers.md)
