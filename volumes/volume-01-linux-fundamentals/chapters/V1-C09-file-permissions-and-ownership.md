---
volume: 1
chapter: 9
part: 1
id: V1-C09
title: File Permissions & Ownership
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Intermediate
estimated_time: 2 Hours
reading_time: 40 Minutes
labs: 1
interview_questions: 3
prerequisites: Chapter 8
last_updated: 2026-07
status: In Progress
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 9 — File Permissions & Ownership

* **Difficulty:** Intermediate
* **Estimated Time:** 2 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

A single incorrect permission can either lock users out of their data or expose the entire server to a breach. Here, we decode the octal permission model and explore how ownership dictates security.

By the end of this chapter, you will be able to:
* Decode the 10-character `ls -l` permission string (e.g., `-rwxr-xr--`).
* Understand the Octal permission model (Read=4, Write=2, Execute=1).
* Use `chmod` to securely restrict file access.
* Use `chown` to transfer ownership of files to different users and groups.

## Visual Architecture: Decoding Permissions

When you type `ls -l`, you see a string like `-rwxr-xr--`. This string is divided into four distinct blocks.

```mermaid
flowchart TD
    A["-rwxr-xr--"] --> B["Type (-)"]
    A --> C["User (rwx)"]
    A --> D["Group (r-x)"]
    A --> E["Other (r--)"]
    
    B -.->|"File or Directory"| B1("File")
    C -.->|"Owner's Rights"| C1("Read, Write, Execute")
    D -.->|"Group's Rights"| D1("Read, Execute")
    E -.->|"Everyone Else"| E1("Read Only")
    
    style A fill:#2d3436,stroke:#b2bec3,color:#fff
    style B fill:#d63031,stroke:#ff7675,color:#fff
    style C fill:#0984e3,stroke:#74b9ff,color:#fff
    style D fill:#00b894,stroke:#55efc4,color:#fff
    style E fill:#f39c12,stroke:#f1c40f,color:#000
```

## Theory & Concepts

### 1. The Triad (User, Group, Other)
Every file and directory in Linux belongs to one specific **User** (the Owner) and one specific **Group**. 
Permissions dictate what the Owner can do, what members of the Group can do, and what Everyone Else (Other) can do.

### 2. The Actions (Read, Write, Execute)
* **Read (r)**: View the contents of a file, or list the contents of a directory.
* **Write (w)**: Modify or delete the file, or create/delete files inside a directory.
* **Execute (x)**: Run the file as a script/program, or `cd` into the directory. *(If a directory does not have the 'x' permission, you cannot enter it, even if you have 'r'!).*

### 3. The Octal Model (Math Time)
To change permissions quickly, Linux engineers use Octal math.
* `Read` = 4
* `Write` = 2
* `Execute` = 1

You add these numbers together for each of the three blocks (User, Group, Other).
* **7** = Read + Write + Execute (4+2+1)
* **6** = Read + Write (4+2+0)
* **5** = Read + Execute (4+0+1)
* **4** = Read Only (4+0+0)
* **0** = No Access

If you want the Owner to have full access (7), the Group to have read/execute (5), and Others to have read/execute (5), the permission is **755**.

### 4. `chmod` (Change Mode)
Use `chmod` to apply these permissions to a file.
* `chmod 644 document.txt`: Owner can read/write. Group and Other can only read. This is the standard for most files.
* `chmod 755 script.sh`: Owner can do everything. Group and Other can read and execute. This is standard for executable scripts.
* `chmod 600 id_rsa`: Owner can read/write. Group and Other are completely blocked. This is mandatory for private SSH keys.

### 5. `chown` (Change Ownership)
Use `chown` to transfer ownership of a file. Only the root user can assign files to someone else.
* `chown sarah document.txt`: Gives ownership to the user Sarah.
* `chown sarah:developers document.txt`: Gives ownership to the user Sarah, and assigns the file to the `developers` group.
* `chown -R www-data:www-data /var/www/html`: Recursively changes the owner and group for an entire web directory.

## Real-World Scenarios

> [!IMPORTANT]
> **Incident Report & Roleplay**
>
> **👤 End User (Dave):**
> *""We uploaded our new website files to the server, but when we go to the URL, the web browser throws a '403 Forbidden' error!""*
>
> **🧑‍💻 Tech Support (Charlie):**
> - **Diagnosis:** A 403 Forbidden means the web server reached the file, but the Linux Kernel blocked it from reading it.
>
> **👨‍🔧 Junior Admin (Bob):**
> - **Investigation:** You run `ls -l /var/www/html/index.html`. You see:
>     `-rw------- 1 root root 4096 index.html`
>
> **🦸‍♀️ Senior Admin (Alice):**
> - **The Problem:** The file is owned by `root`, and permissions are `600` (only root can read it). The web server runs as the `www-data` (or `nginx`) user, so it falls into the "Other" category, which has `0` access.
>
> **🏢 Business Owner (Eve):**
> - **The Fix:** You run `sudo chown www-data:www-data /var/www/html/index.html` (or `sudo chmod 644 /var/www/html/index.html`). The web server can now read the file, and the website loads perfectly.
>   
>
## Hands-on Lab

> [!CAUTION]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 9 Practice Guide](../practice-files/V1-C09-practice.md). You will create a highly sensitive file and use permissions to successfully block unauthorized users from reading it.

## Interview Questions

### Question 1: A user has Read (`r`) permission on a directory, but they cannot `cd` into it. Why?
* **Target Answer**: "To enter a directory, a user must have Execute (`x`) permissions on that directory. Read (`r`) only allows them to list the contents using `ls`, but without `x`, they cannot traverse into it."

### Question 2: What does `chmod 777` do, and why is it dangerous?
* **Target Answer**: "`chmod 777` grants Read, Write, and Execute permissions to the Owner, the Group, and Everyone Else on the system. It is dangerous because it allows any user (or any compromised process) to modify, delete, or execute malicious code within that file or directory."

### Question 3: What is the numerical (octal) equivalent of `-rw-r--r--`?
* **Target Answer**: "644. The owner has read (4) + write (2) = 6. The group has read (4) = 4. Others have read (4) = 4."

## Chapter Summary

Permissions are the bedrock of Linux security. Every time you create a file or install an application, you must understand exactly who is allowed to touch it. If a service is failing to read a configuration file, or failing to write to a log file, the answer is almost always a misconfigured permission string or incorrect ownership.

## Completion Checklist

- [ ] I can translate a string like `rwxr-xr-x` into its octal equivalent (`755`).
- [ ] I understand why directories require the Execute (`x`) permission.
- [ ] I know how to change both the Owner and the Group of a file in one command.

---

## Navigation

⬅ Previous:
[Chapter 8 – Users & Groups](V1-C08-users-and-groups.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 10 – Package Management](V1-C10-package-management.md)
