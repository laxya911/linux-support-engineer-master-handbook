---
volume: 1
chapter: 20
part: 1
id: V1-C20
title: Bash Scripting Basics
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
prerequisites: Chapter 19
last_updated: 2026-07
status: In Progress
---

# Chapter 20 — Bash Scripting Basics

* **Difficulty:** Intermediate
* **Estimated Time:** 2 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

By the end of this chapter, you will be able to:
* Understand the purpose of a shell script.
* Write a basic script with the mandatory Shebang (`#!/bin/bash`).
* Apply executable permissions using `chmod +x`.
* Declare and use simple variables.

## Visual Architecture: The Script Lifecycle

When you type `./script.sh`, how does Linux know what to do with the text inside the file? It reads the very first line (the Shebang) to determine which interpreter to launch.

```mermaid
flowchart TD
    A["User types: ./backup.sh"] --> B["Linux Kernel checks file permissions"]
    
    B --> C{"Is 'x' (Execute) flag set?"}
    C -->|No| D["Error: Permission Denied"]
    
    C -->|Yes| E["Kernel reads Line 1 (The Shebang)"]
    
    E -->|#!/bin/bash| F["Kernel launches the Bash Interpreter"]
    E -.->|#!/usr/bin/python3| G["Kernel launches the Python Interpreter"]
    
    F --> H["Bash executes the commands line-by-line"]
    
    style A fill:#0984e3,stroke:#74b9ff,color:#fff
    style D fill:#d63031,stroke:#ff7675,color:#fff
    style F fill:#00b894,stroke:#55efc4,color:#000
    style H fill:#f39c12,stroke:#f1c40f,color:#000
```

## Theory & Concepts

### 1. What is a Shell Script?
A shell script is simply a text file containing a list of Linux commands. Instead of typing `apt update`, `apt upgrade`, and `systemctl restart nginx` one by one, you put them in a file. When you run the file, Linux types them for you, in order, at lightning speed.

### 2. The Shebang (`#!`)
Every bash script **must** start with this exact line: `#!/bin/bash`.
* The `#` is a hash.
* The `!` is a bang.
* Together, they tell the Linux Kernel: "Do not read the rest of this file. Hand this file over to the `/bin/bash` program to read."

### 3. Execution Permissions
By default, when you create a file in Linux, it is created with Read and Write (`rw-`) permissions. It is *never* created with Execute (`x`) permissions.
If you try to run it, the Kernel will block you.
* **The Fix**: You must run `chmod +x script.sh`. This adds the Execute permission, turning the text file into an application.

### 4. Running the Script (`./`)
To run a script in your current directory, you cannot just type `script.sh`. You must type `./script.sh`. 
* The `.` means "the folder I am currently standing in".
* The `/` is the directory separator.
* You are telling Linux: "Run the script.sh file located exactly where I am standing right now." *(We will explain why this is necessary in Chapter 21 when we cover the `$PATH` variable).*

### 5. Variables
Scripts become powerful when they can store data dynamically.
* **Setting a variable**: `NAME="Laxman"` *(Do not put spaces around the equals sign!)*
* **Using a variable**: `echo "Hello, $NAME"` *(You must use the `$` symbol to extract the data from the variable).*

## Real-World Scenarios

**Customer:**
*"Every morning, I log into our database server and run `df -h` to check disk space, `free -m` to check RAM, and `uptime` to see how long it has been running. It takes me 10 minutes to do this across all our servers."*

How should a Linux Support Engineer investigate?
* **Mental Map:** This is manual, repetitive toil. It must be automated.
* **The Fix:** The engineer creates a script called `health_check.sh`:
  ```bash
  #!/bin/bash
  echo "--- Disk Space ---"
  df -h
  echo "--- RAM Usage ---"
  free -m
  echo "--- Uptime ---"
  uptime
  ```
* The engineer runs `chmod +x health_check.sh`. 
* **Result:** Now, the customer just types `./health_check.sh` and instantly receives a perfectly formatted report.

## Hands-on Lab

> [!NOTE]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 20 Practice Guide](../practice-files/V1-C20-practice.md) to write, authorize, and execute your very first Bash script.

## Interview Questions

### Question 1: What is the purpose of the `#!/bin/bash` line at the top of a script?
* **Target Answer**: "It is called the shebang. It instructs the operating system's kernel to use the `/bin/bash` interpreter to parse and execute the subsequent lines in the file."

### Question 2: You wrote a script, but when you type `./backup.sh`, the terminal says "Permission Denied". You are the owner of the file. What is wrong?
* **Target Answer**: "The file does not have the Execute (`x`) permission set. By default, Linux text files are not executable for security reasons. You must run `chmod +x backup.sh` to make it executable."

### Question 3: In bash, why will the command `USER = "admin"` fail?
* **Target Answer**: "In bash variable assignment, there cannot be any spaces around the equals sign. It must be `USER="admin"`. If you include spaces, bash will attempt to run the word 'USER' as a command, and '=' as its argument."

## Chapter Summary

Scripting is the difference between a Junior Administrator and a Senior Engineer. A script is just a list of commands you were going to type anyway, bundled under a Shebang, made executable with `chmod +x`, and run with `./`. 

## Completion Checklist

- [ ] I can write the Shebang from memory.
- [ ] I know why `chmod +x` is mandatory for new scripts.
- [ ] I know how to declare a variable without syntax errors.

---

## Navigation

⬅ Previous:
[Chapter 19 – Output Redirection (Piping)](V1-C19-output-redirection.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 21 – Environment Variables](V1-C21-environment-variables.md)
