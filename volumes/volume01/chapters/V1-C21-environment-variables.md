---
volume: 1
chapter: 21
part: 1
id: V1-C21
title: Environment Variables
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 1.0.0
difficulty: Advanced
estimated_time: 2 Hours
reading_time: 45 Minutes
labs: 1
interview_questions: 3
prerequisites: Previous Chapter
last_updated: 2026-07
status: Published
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 21 — Environment Variables


## Learning Objectives

How do applications know where to find their configurations? Environment variables act as the invisible global state of your shell, dictating everything from your `$PATH` to system locales.

By the end of this chapter, you will be able to:
* Differentiate between local variables and global environment variables.
* Explain exactly how the `$PATH` variable resolves commands.
* Append a custom directory to `$PATH`.
* Make variable modifications permanent using `~/.bashrc`.

## Visual Architecture: The Search for a Command

When you type `ping`, Linux does not magically know where the `ping` application lives. It must search for it. The `$PATH` variable provides the exact list of directories the Kernel is allowed to search.

```mermaid
flowchart LR
    A["User types: ping google.com"] --> B["Kernel reads $PATH variable"]
    
    B --> C{"Is 'ping' inside /usr/local/bin/?"}
    C -->|"No"| D{"Is 'ping' inside /usr/bin/?"}
    
    D -->|"No"| E{"Is 'ping' inside /bin/?"}
    
    E -->|"Yes"| F["Kernel finds /bin/ping and executes it!"]
    
    E -->|"No"| G["Error: command not found"]
    
    style A fill:#0984e3,stroke:#74b9ff,color:#fff
    style G fill:#d63031,stroke:#ff7675,color:#fff
    style F fill:#00b894,stroke:#55efc4,color:#000
```

## Theory & Concepts

### 1. What are Environment Variables?
Your shell needs to keep track of a lot of information: Who are you? Where is your home directory? What language do you speak? 
It stores this data in **Environment Variables**. 
* They are always written in ALL CAPS.
* You can view all of them by running the `env` or `printenv` commands.
* Common examples: `$USER` (your username), `$HOME` (your home directory), `$PWD` (your present working directory).

### 2. The Almighty `$PATH`
`$PATH` is the most important variable in Linux. It is a colon-separated list of directories. 
If you type `ls`, Linux checks the first directory in the `$PATH` list. If `ls` isn't there, it checks the second directory. It keeps checking until it finds the executable. If it checks every directory and still can't find it, it returns `command not found`.

**Why `./` is required for scripts:**
When you wrote a script in Chapter 20, you had to run it using `./script.sh`. Why? Because the folder you created the script in (e.g., your home directory) is **NOT** in the `$PATH` variable! The `./` explicitly tells Linux: "Do not use the `$PATH` variable to search for this file. Just look right here."

### 3. Modifying the `$PATH`
If you install a custom application into `/opt/myapp/bin`, Linux will not know it exists because `/opt/myapp/bin` is not in the default `$PATH`.
* **The Temporary Fix**: `export PATH=$PATH:/opt/myapp/bin`
*(Translation: Make the new PATH equal to the old PATH, plus my new directory).*

> [!TIP] Support Engineer Tip #20
> **Never Overwrite `$PATH`:** If you accidentally type `export PATH=/opt/myapp/bin` (forgetting the `$PATH:` part), you will destroy the existing path. Basic commands like `ls`, `cat`, and `sudo` will suddenly return "command not found". If this happens, just log out and log back in to reset it.

### 4. Making it Permanent (`.bashrc`)
If you use the `export` command in your terminal, the variable will disappear the second you log out. 
To make a variable permanent, you must write the `export` command into a configuration file that runs automatically every time you log in.
* **`~/.bashrc`**: This file lives in your home directory. It runs every time you open a terminal. If you put an `export` command at the bottom of this file, the variable becomes permanent for *you*.

## Real-World Scenarios

> [!IMPORTANT] Incident Report: The Missing Binary
>
> **Problem:** End User (Dave): "I downloaded a binary called `aws-cli` and put it in my `/home/user/tools` directory. But when I just type `aws-cli` in the terminal, it says 'command not found'. I don't want to type the full path every time. Fix this!"
>
> **Investigation:** Charlie verifies that the binary exists and has execute permissions, but confirms the directory is not in Dave's `$PATH`.
> 
> ```bash
> dave@prod-db1:~$ ls -l /home/user/tools/aws-cli
> -rwxr-xr-x 1 user user 5430291 Jul 12 10:14 /home/user/tools/aws-cli
> dave@prod-db1:~$ aws-cli
> bash: aws-cli: command not found
> dave@prod-db1:~$ echo $PATH
> /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
> ```
>
> **Evidence:** The binary is fully executable, but `/home/user/tools` is missing from the `$PATH` output.
>
> **Wrong Assumption:** Bob (Junior Admin) says: "Let's just move the `aws-cli` binary into `/usr/bin/` so the system can find it."
>
> **Root Cause:** Alice (Senior Admin) steps in. Moving random binaries into system directories (`/usr/bin`) pollutes the OS. It is much safer to add the user's custom tools directory to their personal `$PATH`.
>
> **Lessons Learned:** Alice opens the user's configuration file: `nano ~/.bashrc`. At the very bottom, she appends: `export PATH=$PATH:/home/user/tools`. She saves the file and runs `source ~/.bashrc`. 
> 
> ```bash
> dave@prod-db1:~$ source ~/.bashrc
> dave@prod-db1:~$ aws-cli --version
> aws-cli/2.13.0 Python/3.11.4 Linux/5.15.0-76-generic
> ```
> 
> The customer can now type `aws-cli` from anywhere in the system, and Linux will successfully find and execute it without cluttering the global system directories.
## Hands-on Lab

> [!CAUTION]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 21 Practice Guide](../practice-files/V1-C21-practice.md). You will create a custom application, observe the "command not found" error, and permanently fix it by modifying your `$PATH`.

## Interview Questions

### Question 1: What is the `$PATH` environment variable used for?
* **Target Answer**: "The `$PATH` variable contains a colon-separated list of directories. When a user types a command without providing an absolute path, the shell searches through these directories sequentially to locate the executable binary. If it is not found in any of those directories, it returns a 'command not found' error."

### Question 2: Why do you have to type `./script.sh` to run a script in your current directory, instead of just `script.sh`?
* **Target Answer**: "For security reasons, the current working directory (`.`) is intentionally excluded from the `$PATH` variable. Therefore, the shell will not search the current directory for executables. You must explicitly tell the shell where the script is by providing the relative path (`./`)."

### Question 3: You ran `export MY_VAR="123"`, but after rebooting the server, the variable is gone. How do you make it permanent?
* **Target Answer**: "The `export` command only applies to the current shell session. To make it persistent across reboots and new sessions, the export command must be appended to the user's profile configuration file, such as `~/.bashrc` or `~/.bash_profile`."

## Chapter Summary

The `$PATH` variable is the hidden engine behind every command you type. If you understand how Linux searches for executables, and how to permanently modify that search path using `~/.bashrc`, you will resolve software installation issues in seconds rather than hours.

## Completion Checklist

- [ ] I can view my current `$PATH` by echoing it.
- [ ] I understand the danger of overwriting `$PATH` instead of appending to it.
- [ ] I know which configuration file to edit to make variables permanent.



**Chapter Transition**
> Our scripts are dynamic and powerful. Now, how do we force the system to run them automatically at 3 AM?

---

## Navigation

⬅ Previous:
[Chapter 20 — Bash Scripting Basics](V1-C20-bash-scripting-basics.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 22 — User Automation (Cron)](V1-C22-user-automation-cron.md)
