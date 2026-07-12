---
volume: 2
chapter: 14
part: 4
id: V2-C14
title: Mandatory Access Control (SELinux & AppArmor)
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
prerequisites: Volume 1 Completion
last_updated: 2026-07
status: In Progress
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 14 — Mandatory Access Control (SELinux & AppArmor)


## Learning Objectives

By the end of this chapter, you will be able to:
* Differentiate between Discretionary Access Control (DAC) and Mandatory Access Control (MAC).
* Understand the concept of SELinux Security Contexts.
* Toggle SELinux between Enforcing and Permissive modes.
* Troubleshoot "Hidden Denials" where SELinux blocks access despite `chmod 777` permissions.


> [!IMPORTANT]
> **ServiceNow Ticket: INC-19190**
> **Priority:** High
> **Reported By:** Enterprise Application Team
> **Issue:** We are experiencing a critical failure related to Mandatory Access Control (SELinux & AppArmor). Please investigate immediately.
> 
> **Support Engineer Objective:** Use operational thinking to collect evidence, identify the root cause, and restore service without causing further disruption.

## Visual Architecture: The Two Bouncers

Every time a process tries to open a file in Linux, it must pass two bouncers. 
The first bouncer is DAC (`chmod`). He checks if the file owner matches the process owner. 
The second bouncer is MAC (SELinux or AppArmor). He doesn't care about the owner. He checks the *policy rules*. If the policy says "Web servers are never allowed to read passwords," MAC will block the web server, even if the web server legally owns the password file!

```mermaid
flowchart LR
    A["Process \n (Nginx Web Server)"] -->|"Requests to read"| B{"DAC Bouncer \n (chmod / chown)"}
    
    B -->|"Permissions OK (777)"| C{"MAC Bouncer \n (SELinux)"}
    B -->|"Permissions Denied"| E["Access Denied"]
    
    C -->|"Security Context Matches"| D["Read /var/www/html/index.html"]
    C -->|"Security Context Fails"| F["Access Denied \n (Logged to /var/log/audit)"]
    
    style A fill:#0984e3,stroke:#74b9ff,color:#fff
    style B fill:#f39c12,stroke:#f1c40f,color:#000
    style C fill:#d63031,stroke:#ff7675,color:#fff
    style D fill:#00b894,stroke:#55efc4,color:#000
```

## Theory & Concepts

### 1. DAC vs. MAC
* **DAC (Discretionary Access Control):** You learned this in Volume 1. Users use `chmod` and `chown` to set permissions. The problem? If a hacker compromises the `root` user, `root` has the *discretion* to bypass all `chmod` rules.
* **MAC (Mandatory Access Control):** A higher authority. Administrators write strict, mandatory rules that dictate what a process is allowed to do. Even if a hacker compromises `root`, MAC will still block `root` from violating the policy. 

### 2. The Two Implementations
* **SELinux (Security-Enhanced Linux):** Developed by the NSA. Standard on RHEL, CentOS, and Fedora. It uses label-based "Security Contexts".
* **AppArmor:** Standard on Ubuntu and Debian. It uses path-based rules. It is generally considered easier to use than SELinux, but slightly less granular.

### 3. SELinux Modes
SELinux has three modes of operation, viewed by typing `sestatus`:
1. **Enforcing:** Active. It blocks violations and logs them.
2. **Permissive:** Passive. It *allows* violations but logs them (used for troubleshooting).
3. **Disabled:** Turned off entirely (not recommended).
You can temporarily switch to Permissive mode by typing `setenforce 0`.

## Scenario-Based Troubleshooting

### Scenario A: The Hidden Deny (Why 777 fails)
**The Incident:** A junior developer sets up a new web server on RHEL. They don't want to use the default `/var/www/html` directory. Instead, they create a folder at `/home/user/website` and point Nginx to it. 
They load the website in their browser, but they get a `403 Forbidden` error. 
Frustrated, the developer runs `chmod -R 777 /home/user/website`. They try again. They still get `403 Forbidden`! They submit a ticket to the Linux Engineering team claiming the server is broken.

**The Investigation & Fix:**

1. The Support Engineer logs in. They see the `777` permissions and immediately know standard DAC is not the problem.
2. The engineer runs `sestatus` and confirms SELinux is `Enforcing`. 
3. To prove SELinux is the culprit, the engineer temporarily disables it: `setenforce 0`. They reload the webpage. The website loads perfectly! They immediately turn SELinux back on: `setenforce 1`.
4. The engineer checks the audit log: `grep nginx /var/log/audit/audit.log`. 
5. The log reveals the problem: The folder `/home/user/website` has a Security Context of `user_home_t`. The Nginx process is only allowed to read files with a Security Context of `httpd_sys_content_t`.
6. Even though the developer set `chmod 777`, SELinux blocked Nginx because Web Servers are not allowed to read Home Directories.
7. The engineer uses the `chcon` (Change Context) command to update the labels on the developer's folder:
   `chcon -Rt httpd_sys_content_t /home/user/website`
8. The website loads perfectly, and the engineer removes the dangerous `777` permissions.


## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 14 Practice Guide](../practice-files/V2-C14-practice.md) to inspect the hidden Security Context labels attached to your files using the `-Z` flag.

## Interview Questions

### Question 1: You have verified that a file has `777` permissions, but a service still receives a "Permission Denied" error when trying to read it. What is the most likely cause?
* **Target Answer**: "The most likely cause is a Mandatory Access Control system like SELinux or AppArmor. Standard `777` permissions only satisfy Discretionary Access Control (DAC). If the SELinux security context of the file does not match the policy rules for the service attempting to read it, SELinux will block the read operation, creating a 'hidden deny'."

### Question 2: How can you quickly determine if SELinux is the cause of a broken application without permanently changing the server configuration?
* **Target Answer**: "I would run the `setenforce 0` command to temporarily place SELinux into 'Permissive' mode. In Permissive mode, SELinux allows all actions but continues to log policy violations. If the application suddenly starts working, I have proven SELinux is the culprit. I would then run `setenforce 1` to restore protection and begin fixing the file contexts."

### Question 3: What command do you use to view the SELinux security contexts (labels) attached to files in a directory?
* **Target Answer**: "You append the uppercase `-Z` flag to standard commands. For example, `ls -lZ` will display the standard file permissions alongside the SELinux user, role, and type context labels."

## Chapter Summary

SELinux and AppArmor are incredibly powerful security tools that stop hackers from doing damage even if they manage to steal the `root` password. Never disable them permanently to "fix" a broken application. Use `setenforce 0` to test, read the audit logs, and fix the file contexts using `chcon` or `restorecon`.

## Completion Checklist

- [ ] I understand the difference between DAC (`chmod`) and MAC (SELinux).
- [ ] I can explain Enforcing vs. Permissive modes.
- [ ] I know how to check if SELinux is running (`sestatus`).

---

## Navigation

← Previous: [Chapter 13 — Intrusion Prevention (fail2ban)](V2-C13-intrusion-prevention.md)

↑ Volume Contents: [Table of Contents](TOC.md)

→ Next: [Chapter 15 — Security Auditing & Compliance](V2-C15-security-auditing.md)
