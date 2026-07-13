---
volume: 2
chapter: 25
part: 6
id: V2-C25
title: Capstone Project
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 1.0.0
difficulty: Advanced
estimated_time: 3 Hours
reading_time: 15 Minutes
labs: 1
interview_questions: 0
prerequisites: Previous Chapter
last_updated: 2026-07
status: Published
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 25 — Capstone Project


## The Journey So Far

Congratulations. You have reached the end of Volume 2: Linux System Administration. 
If you have completed Volumes 1 and 2, you have officially transformed from a Linux Beginner into a Junior Linux Support Engineer. 

You no longer view Linux as a scary black box. You understand how the system authenticates users (PAM/SSSD). You know how storage is layered (LVM) and distributed (NFS). You can configure static IPs, manipulate routing tables, and capture raw packet data off the wire (`tcpdump`). You understand the absolute necessity of SSH Keys, the power of active firewalls (`fail2ban`), and how Mandatory Access Control (`SELinux`) defends against compromised services. 

Finally, you learned the mindset of a Senior Engineer. You learned how to automate your tasks (`cron` and Bash scripting), how to recover from disasters (`rsync`), and how to write blameless RCAs to ensure an incident only happens once.

## The Final Test

In the real world, problems do not happen in a vacuum. A single misconfiguration in one subsystem often triggers a cascading failure in another. 
To prove you are ready to manage enterprise production servers, you must pass the Capstone Project. 

In this Capstone, you will not be given step-by-step commands. You will be given a list of symptoms and business requirements. It is entirely up to you to apply the OODA loop, investigate the symptoms, and implement the permanent fixes.


## Real-World Support Ticket

> [!IMPORTANT] ServiceNow Ticket: INC-2026225
> **Title:** The Cascading Failure (Capstone)
> **Assigned To:** Charlie (L2 Support Engineer)
> **Status:** IN PROGRESS
> 
> **1) Ticket intake & triage**
> Charlie takes a P1 Critical ticket: 'Everything is down.' Users cannot reach the web app, and the database is unreachable.
> 
> **2) Discovery & diagnosis**
> Charlie follows the OSI model. Layer 1/2/3: The network is up. Layer 4: Port 80 is open. Layer 7: Nginx returns a 502 Bad Gateway. He checks the backend app logs and sees 'Cannot connect to database.' He checks the database and sees 'No space left on device.'
> 
> **3) Immediate containment**
> Charlie cleans up old database transaction logs to free up enough space for the database engine to start running again.
> 
> **4) Resolution planning & execution**
> With the database running, Charlie restarts the backend application, which reconnects to the database. Nginx immediately begins serving traffic.
> 
> **5) Verification**
> Charlie confirms 200 OK responses in the Nginx access logs and verifies the application UI.
> 
> **6) Closure & documentation**
> Charlie documents the full chain: Disk full -> DB crash -> App crash -> 502 Gateway.
> 
> **7) Post-resolution follow-up**
> Charlie implements strict monitoring on the database disk volume.
> 
> **8) Escalation rules**
> If the database had corrupted its tables due to the crash, Charlie would have escalated to the DBA team for a repair.


## Hands-on Lab

> [!CAUTION]  
> **Warning: Extreme Difficulty**
> Proceed to the [Chapter 25 Practice Guide](../practice-files/V2-C25-practice.md) to receive your final mission briefing. Good luck, Engineer.

---

---

**Chapter Transition**
> Congratulations on completing Volume 2. Next up: Volume 3 - Automation & Infrastructure.

---

**Chapter Transition**
> Congratulations on completing Volume 2. Next up: Volume 3 - Automation & Infrastructure.

---




## Navigation

← Previous: [Chapter 24 — Intermediate Troubleshooting](V2-C24-intermediate-troubleshooting.md)

↑ Volume Contents: [Table of Contents](TOC.md)

→ Next: None
