---
volume: 1
chapter: 29
part: 1
id: V1-C29
title: Database Fundamentals
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
prerequisites: Chapter 28
last_updated: 2026-07
status: In Progress
---

# Chapter 29 — Database Fundamentals

* **Difficulty:** Advanced
* **Estimated Time:** 2 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

By the end of this chapter, you will be able to:
* Identify the standard database port (3306) and daemon (`mysqld`).
* Understand the difference between `127.0.0.1` and `0.0.0.0` bindings.
* Diagnose remote "Connection Refused" errors.
* Troubleshoot the Linux Out of Memory (OOM) Killer.

## Visual Architecture: The 3-Tier Stack

Databases are the final layer of the modern internet. A user never touches a database directly. The user touches the Web Server, the Web Server touches the Application, and the Application touches the Database.

```mermaid
flowchart TD
    A["User (Browser)"] -->|HTTPS| B["Nginx (Web Tier)"]
    
    B -->|HTTP| C["Node.js / PHP (App Tier)"]
    
    C -->|MySQL Protocol (Port 3306)| D["MySQL / MariaDB (Database Tier)"]
    
    style A fill:#0984e3,stroke:#74b9ff,color:#fff
    style B fill:#00b894,stroke:#55efc4,color:#000
    style C fill:#f39c12,stroke:#f1c40f,color:#000
    style D fill:#d63031,stroke:#ff7675,color:#fff
```

## Theory & Concepts

### 1. The Daemon and the Port
Whether you are using MySQL or MariaDB, the background service is almost always called `mysqld` (MySQL Daemon). 
When running, it listens for incoming connections on **Port 3306**.

### 2. The `bind-address` (Localhost vs. Public)
For security reasons, when you install MySQL, it configures itself to only listen to `127.0.0.1` (Localhost). This means only applications hosted on the *exact same server* can connect to it. Hackers on the internet cannot reach it.
If you have a dedicated Database Server and a separate Web Server, you must edit the database configuration file and change the `bind-address` to `0.0.0.0` (All Interfaces) so it accepts connections from the outside world.

### 3. The Linux OOM Killer
Databases are memory hogs. If your server runs out of RAM, the Linux Kernel panics. To prevent the entire operating system from crashing, the Kernel deploys the **OOM (Out of Memory) Killer**. The OOM Killer scans the server for the process using the most RAM, targets it, and instantly assassinates it. 99% of the time, the victim is MySQL.

## Scenario-Based Troubleshooting

### Scenario A: The "Connection Refused" Error
**The Incident:** A customer splits their infrastructure. They put their application on Server A, and MySQL on Server B. Their application throws a fatal error: `Connection Refused to Server B`.

**The Investigation & Fix:**
1. The engineer logs into Server B (the database). They run `ss -tulpn | grep 3306`.
2. The output says: `tcp LISTEN 127.0.0.1:3306`.
3. The engineer realizes the database is actively rejecting external traffic. It is only talking to itself.
4. They open the MySQL configuration file:
   * On Ubuntu: `nano /etc/mysql/mysql.conf.d/mysqld.cnf`
   * On RHEL: `nano /etc/my.cnf`
5. They find the line `bind-address = 127.0.0.1` and change it to `bind-address = 0.0.0.0`.
6. They save the file and run `systemctl restart mysql`. 
7. They run `ss -tulpn` again. The output now says `0.0.0.0:3306`. The application instantly connects. *(Note: The engineer also ensures the firewall only allows Server A to reach this port!)*

### Scenario B: The OOM Killer Assassin
**The Incident:** A customer reports their database crashes randomly every night around 2:00 AM. They just run `systemctl start mysql` every morning to fix it.

**The Investigation & Fix:**
1. The engineer logs in. They suspect memory exhaustion.
2. They query the system logs: `grep -i "Out of memory" /var/log/syslog` (or they check `dmesg`).
3. The logs reveal the smoking gun: `Out of memory: Killed process 4492 (mysqld)`.
4. The engineer asks the customer what happens at 2:00 AM. The customer says, "We run our daily backup script."
5. **The Fix:** The engineer informs the customer that their server only has 1GB of RAM, and the backup script requires more than that. The Kernel is executing the OOM Killer to save the system. The engineer recommends upgrading the server to 2GB of RAM or adding a Swap file.

## Hands-on Lab

> [!CAUTION]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 29 Practice Guide](../practice-files/V1-C29-practice.md). You will audit your server for evidence of OOM events.

## Interview Questions

### Question 1: An application on WebServer01 cannot connect to DatabaseServer01. You check DatabaseServer01 and see `tcp LISTEN 127.0.0.1:3306`. What is the problem?
* **Target Answer**: "The database is currently bound only to the localhost interface (`127.0.0.1`), meaning it will only accept connections originating from its own internal system. To allow external connections from WebServer01, the MySQL configuration file must be updated to set the `bind-address` to `0.0.0.0`, followed by a service restart."

### Question 2: A customer's MySQL service unexpectedly stopped overnight. You check the MySQL error logs, but there are no errors listed at the time of the crash. Where should you look next?
* **Target Answer**: "I would look at the system logs (`/var/log/syslog` or `dmesg`) and grep for 'Out of memory' or 'OOM'. Databases are frequently terminated by the Linux Kernel's OOM Killer when the system runs out of RAM. This termination happens at the OS level, which is why MySQL wouldn't have time to write an error to its own application logs."

### Question 3: What is the standard port for MySQL, and what is the name of the background daemon process?
* **Target Answer**: "The standard port is 3306, and the daemon process is named `mysqld`."

## Chapter Summary

When a database connection fails, always check the `bind-address` using `ss -tulpn`. When a database crashes silently without leaving a trace in its own application logs, always check the system logs for the OOM Killer. 

## Completion Checklist

- [ ] I understand the difference between `127.0.0.1` and `0.0.0.0` bindings.
- [ ] I can locate the `bind-address` configuration file on my distro.
- [ ] I know how to check the system logs for the OOM Killer.

---

## Navigation

⬅ Previous:
[Chapter 28 – Reverse Proxies & Load Balancing](V1-C28-reverse-proxies-and-load-balancing.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 30 – Conclusion & Career Path](V1-C30-conclusion-and-career-path.md)
