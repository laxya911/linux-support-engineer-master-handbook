---
volume: 1
chapter: 23
part: 1
id: V1-C23
title: Basic System Monitoring
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
prerequisites: Chapter 22
last_updated: 2026-07
status: In Progress
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 23 — Basic System Monitoring

* **Difficulty:** Intermediate
* **Estimated Time:** 2 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

You can't fix what you can't measure. We'll explore the real-time monitoring tools that help you instantly identify whether the CPU, RAM, or Disk I/O is the bottleneck.

By the end of this chapter, you will be able to:
* Parse the `uptime` command to read 1-minute, 5-minute, and 15-minute Load Averages.
* Understand Load Average using the "Bridge Analogy".
* Use `free -h` to differentiate between "Free" and "Available" memory.
* Use `top` to locate and terminate runaway CPU processes.

## Visual Architecture: The Bridge Analogy (Load Average)

Load Average is not a percentage. It is a measurement of the queue of processes waiting for CPU time. Imagine your CPU is a single-lane bridge.

```mermaid
flowchart LR
    A["Load 0.5 (Healthy)"] --> B["Bridge is half full.\nCars drive across at full speed."]
    
    C["Load 1.0 (Warning)"] --> D["Bridge is exactly full.\nTraffic is moving, but at capacity."]
    
    E["Load 2.0 (Critical)"] --> F["Bridge is full, and a line of cars\nis backed up on the highway waiting.\nServer is slow."]
    
    style A fill:#00b894,stroke:#55efc4,color:#000
    style C fill:#f39c12,stroke:#f1c40f,color:#000
    style E fill:#d63031,stroke:#ff7675,color:#fff
```
*(Note: If you have a 4-Core CPU server, you have a 4-lane bridge. In that case, a load of `4.0` means the bridge is exactly full).*

## Theory & Concepts

### 1. `uptime` (The Quick Health Check)
If a server feels slow, your very first instinct should be to type `uptime`.
It prints the current time, how long the server has been running, how many users are logged in, and the **Load Averages**.
* Output format: `load average: 0.20, 0.55, 1.20`
* These numbers represent the 1-minute, 5-minute, and 15-minute averages.
* If the 1-minute load is high, but the 15-minute load is low, it means a sudden spike of traffic just occurred.

### 2. `top` (The Process Monitor)
If `uptime` reveals a high load, you must find out *which* process is causing it.
* `top`: This is the built-in task manager. It refreshes every 3 seconds.
* Press `P` while it is running to sort the list by CPU usage.
* Look at the `PID` (Process ID) and the `COMMAND` columns. If you see a PHP script consuming 99% CPU, you have found the culprit.
* *(Modern Alternative: `htop` is a colorful, interactive version of `top` that you can navigate with your mouse, though it often requires manual installation).*

### 3. `free -h` (The Memory Check)
Checking RAM in Linux is tricky because Linux intentionally uses "free" RAM to cache hard drive data to make the system faster. 
* Do not look at the `free` column! It will often say 0 MB, which panics junior engineers.
* **Always look at the `available` column**. This is the actual amount of RAM your applications can claim before the server runs out of memory.

## Real-World Scenarios

> [!IMPORTANT]
> **Incident Report & Roleplay**
>
> **👤 End User (Dave):**
> *""My e-commerce website is completely unresponsive. It takes 30 seconds just to load the homepage!""*
>
> **🧑‍💻 Tech Support (Charlie):**
> - **Diagnosis:** The server is bottlenecking on CPU, RAM, or Disk Space.
>
> **👨‍🔧 Junior Admin (Bob):**
> - **Investigation:** 
>     1. The engineer runs `df -h` (Chapter 17). Disk space is at 40%. (Healthy).
>     2. The engineer runs `free -h`. The `available` column shows 4GB of RAM. (Healthy).
>     3. The engineer runs `uptime`. The server has 2 CPUs, but the load average is `18.5, 12.0, 5.0`. (Critical Traffic Jam).
>     4. The engineer runs `top` and sorts by CPU. They see a massive, runaway database query consuming 200% CPU (maxing out both cores).
>
> **🦸‍♀️ Senior Admin (Alice):**
> - **The Fix:** The engineer identifies the Process ID (PID) of the database query and kills it. The load average immediately drops back to `0.5`, and the website instantly loads.
>   
>
## Hands-on Lab

> [!CAUTION]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 23 Practice Guide](../practice-files/V1-C23-practice.md). You will parse your system's load averages and learn how to navigate the `top` interface.

## Interview Questions

### Question 1: A customer with a 2-Core CPU server complains of slowness. You run `uptime` and see a load average of `1.50`. Is the CPU overloaded?
* **Target Answer**: "No. Because the server has 2 cores, the maximum 'full capacity' load is 2.0. A load of 1.50 means the CPUs are working hard, but there is still 25% of the total processing capacity sitting idle. The slowness is likely caused by something else, such as network latency or disk I/O."

### Question 2: Why does the `free` command often show 0MB of free RAM, even on a healthy server?
* **Target Answer**: "Linux is designed to use all unused RAM for disk caching to improve system performance. This fills up the 'free' column. However, if an application requests memory, Linux instantly drops the cache to hand over the RAM. Therefore, you should always look at the 'available' column, not the 'free' column."

### Question 3: How do you find the exact Process ID (PID) of the application consuming the most CPU?
* **Target Answer**: "I would run the `top` command. By default, it often sorts by CPU usage, but I can press `Shift+P` (or just `P`) to ensure the highest CPU consumers are pushed to the top of the list. The PID is located in the far-left column."

## Chapter Summary

Monitoring is about proving theories. If the server is slow, don't guess. Run `uptime` to check the CPU queue, run `free -h` to check the available memory, and run `df -h` to check the disk space. Once you isolate the bottleneck, use `top` to identify the specific process responsible.

## Completion Checklist

- [ ] I understand the Bridge Analogy for Load Averages.
- [ ] I know why the `free` memory column is deceptive.
- [ ] I can launch `top`, read it, and exit it by pressing `q`.

---

## Navigation

⬅ Previous:
[Chapter 22 – User Automation (Cron)](V1-C22-user-automation-cron.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 24 – Introduction to Networking (Firewalls)](V1-C24-introduction-to-networking-firewalls.md)
