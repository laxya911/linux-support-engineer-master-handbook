---
volume: 2
chapter: 12
part: 4
id: V2-C12
title: SSH Hardening
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 1.0.0
difficulty: Intermediate
estimated_time: 1.5 Hours
reading_time: 30 Minutes
labs: 1
interview_questions: 3
prerequisites: Previous Chapter
last_updated: 2026-07
status: Published
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 12 — SSH Hardening


## Learning Objectives

By the end of this chapter, you will be able to:
* Explain the concept of Public/Private Key Cryptography for SSH.
* Configure the `/etc/ssh/sshd_config` file to disable root logins and password authentication.
* Troubleshoot "Permission Denied" errors caused by incorrect `.ssh` directory permissions.


> [!NOTE]
> **The Enterprise Mindset: SSH Hardening**
>
> Mastering SSH Hardening is critical for stability and accountability. We will explore how to handle SSH Hardening to ensure continuous uptime.

## Visual Architecture: The Cryptographic Padlock

In modern cloud environments, passwords are dead. If a server is accessible via the internet, automated bots will attempt to guess your password millions of times a day. To secure a server, you disable passwords entirely and use SSH Keys. 

```mermaid
flowchart LR
    A["Developer's Laptop"] -->|"Holds the 'Private Key' \n (id_ed25519)"| B{"The Internet"}
    
    B -->|"Attempts to unlock"| C["Linux Server"]
    
    C -->|"Checks the 'Public Key' Padlock \n (~/.ssh/authorized_keys)"| D["Access Granted"]
    
    style A fill:#0984e3,stroke:#74b9ff,color:#fff
    style B fill:#d63031,stroke:#ff7675,color:#fff
    style C fill:#f39c12,stroke:#f1c40f,color:#000
    style D fill:#00b894,stroke:#55efc4,color:#000
```

## Theory & Concepts

### 1. Public/Private Key Pairs
When you generate an SSH key, you create two files:
* **The Private Key (`id_ed25519`)**: This is the literal key. It never leaves your laptop. If someone steals it, they can access your servers.
* **The Public Key (`id_ed25519.pub`)**: This is the padlock. You can safely give this to anyone or paste it onto any server in the world. 
When you connect, the server checks if the mathematical signature of your Private Key fits the Public Key padlock stored in the server's `~/.ssh/authorized_keys` file.

### 2. The SSH Daemon Configuration
The master configuration file for the SSH service is `/etc/ssh/sshd_config`. 
Every time you provision a new server, you must edit this file to enforce the following rules:
* `PermitRootLogin no`: Forces attackers to guess *both* a username and a password/key, rather than just attacking the `root` account.
* `PasswordAuthentication no`: Disables passwords entirely. If an attacker doesn't have the cryptographic key, the server instantly drops the connection.

### 3. The Paranoia of SSH
SSH is designed to be deeply paranoid. If the `~/.ssh` directory or the `authorized_keys` file has loose permissions, SSH will assume a hacker has tampered with the padlocks. It will quietly refuse to read the keys and deny access.

## Industry Incident Spotlight: The Heartbleed Bug

> [!CAUTION] **The Vulnerability that Shook the Internet**
> In 2014, the Heartbleed vulnerability (CVE-2014-0160) in OpenSSL was publicly disclosed, affecting an estimated 17% of all secure web servers on the internet.
>
> **The Timeline:**
> - A bug was introduced in the OpenSSL codebase in 2012, affecting the TLS heartbeat extension.
> - For two years, the vulnerability went unnoticed by the open-source community.
> - Security researchers discovered that the bug allowed attackers to read up to 64 kilobytes of server memory per heartbeat request.
>
> **The Root Cause:**
> A missing bounds check in the heartbeat implementation. When a client sent a heartbeat request, they could lie about the payload size, causing the server to respond with its own memory contents (which often included private SSL keys, passwords, and session cookies).
>
> **The Business Impact:**
> Global panic. Companies worldwide had to revoke and reissue their SSL certificates, patch their servers, and advise millions of users to change their passwords.
>
> **The Lessons Learned:**
> 1. **Open source does not automatically mean secure.** Even widely scrutinized code can harbor devastating bugs.
> 2. Hardening a server means keeping packages updated and rotating cryptographic keys in response to massive vulnerabilities.


## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 12 Practice Guide](../practice-files/V2-C12-practice.md) to generate a modern `ed25519` keypair and inspect your server's `sshd_config` file.

## Interview Questions

### Question 1: Why is it an industry standard to set `PermitRootLogin no` in the `sshd_config` file?
* **Target Answer**: "The `root` user exists on every Linux system. If `PermitRootLogin` is allowed, attackers only have to guess the password. By disabling it, attackers are forced to guess both a valid username and the password. Furthermore, forcing administrators to log in with standard user accounts (and then use `sudo`) creates a perfect audit trail of who performed which actions."

### Question 2: A user has pasted their Public SSH key into their `authorized_keys` file, but the server still prompts them for a password. What is the most likely cause?
* **Target Answer**: "The most likely cause is incorrect file or directory permissions. SSH requires strict permissions to ensure the keys haven't been tampered with by other users. The user's home directory must not be writable by others, the `~/.ssh` directory must be set to `700`, and the `authorized_keys` file must be set to `600`."

### Question 3: Should you ever share your Private SSH key with a co-worker so they can access a server?
* **Target Answer**: "Absolutely never. A Private Key is tied to an individual's identity. If a co-worker needs access to a server, they should generate their own keypair, and I will append their Public Key to the server's `authorized_keys` file. Sharing a Private Key destroys non-repudiation and compromises the entire cryptographic trust model."

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Disabling password authentication before verifying that your SSH keys actually work.

> [!CAUTION] Think Before You Type
> `systemctl restart sshd` (Did you test the config with `sshd -t` first?)

## Chapter Summary

Securing SSH is the first and most important step when building a new server. Disable root logins, disable passwords, and enforce keys. And if SSH suddenly starts ignoring your keys, you don't need to generate new ones—you just need to fix your `chmod` permissions!

## Completion Checklist

- [ ] I understand the difference between a Public Key (padlock) and Private Key (key).
- [ ] I know the correct permissions for the `.ssh` directory (`700`).
- [ ] I know the correct permissions for the `authorized_keys` file (`600`).

---

---

**Chapter Transition**
> SSH keys are secure, but what about brute force attacks on other services? We need automated intrusion prevention.

---

**Chapter Transition**
> SSH keys are secure, but what about brute force attacks on other services? We need automated intrusion prevention.

---




## Navigation

← Previous: [Chapter 11 — Advanced Firewalls (UFW & firewalld)](V2-C11-advanced-firewalls.md)

↑ Volume Contents: [Table of Contents](TOC.md)

→ Next: [Chapter 13 — Intrusion Prevention (fail2ban)](V2-C13-intrusion-prevention.md)
