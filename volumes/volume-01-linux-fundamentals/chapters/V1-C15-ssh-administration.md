---
volume: 1
chapter: 15
part: 1
id: V1-C15
title: SSH Administration
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Advanced
estimated_time: 2.5 Hours
reading_time: 50 Minutes
labs: 1
interview_questions: 3
prerequisites: Chapter 14
last_updated: 2026-07
status: In Progress
---

# Chapter 15 — SSH Administration

* **Difficulty:** Advanced
* **Estimated Time:** 2.5 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

By the end of this chapter, you will be able to:
* Explain how the Public/Private Key exchange protocol works.
* Generate cryptographic keypairs using `ssh-keygen`.
* Distribute public keys using `ssh-copy-id`.
* Harden a server by modifying `/etc/ssh/sshd_config` and restarting the daemon.

## Visual Architecture: The Cryptographic Handshake

Passwords can be guessed. Cryptographic keys cannot. When you use SSH Key Authentication, your computer mathematically proves it holds a private key without ever transmitting it over the network.

```mermaid
sequenceDiagram
    participant C as Client (Laptop)
    participant S as Server (Linux VM)
    
    Note over C: Holds Private Key (Secret)
    Note over S: Holds Public Key (Lock)
    
    C->>S: "I want to log in as user 'sarah'"
    S->>C: Challenge: "Encrypt this random message using Sarah's Private Key."
    
    Note over C: Encrypts message using Private Key
    C->>S: Returns Encrypted Message
    
    Note over S: Decrypts message using Sarah's Public Key
    S-->>S: Did the decrypted message match the original?
    
    alt Match Successful
        S->>C: Access Granted!
    else Match Failed
        S->>C: Connection Terminated
    end
```

## Theory & Concepts

### 1. The Secure Shell (SSH)
SSH is a cryptographic network protocol for operating network services securely over an unsecured network. It operates on **TCP Port 22**.
The server runs the SSH Daemon (`sshd`), and you connect to it using an SSH Client (`ssh`).

### 2. Passwords vs PKI
By default, SSH asks for a password. However, enterprise environments disable password authentication entirely. Instead, they use PKI (Public Key Infrastructure).
* **Private Key (`id_rsa`)**: The secret key. It lives on your laptop. You NEVER share it. If someone steals it, they are you.
* **Public Key (`id_rsa.pub`)**: The lock. You give this to any server you want to log into. The server places it in a file called `~/.ssh/authorized_keys`.

### 3. Generating and Distributing Keys
* `ssh-keygen -t rsa -b 4096`: This command creates the keypair on your laptop. The `-t` specifies the type (RSA), and `-b` specifies the bit length (4096 is highly secure).
* `ssh-copy-id username@192.168.1.50`: This command takes your Public Key and copies it into the remote server's `authorized_keys` file.

### 4. Hardening the Daemon (`sshd_config`)
The SSH daemon's behavior is controlled by `/etc/ssh/sshd_config`. 
*Note: Do not confuse `sshd_config` (server config) with `ssh_config` (client config).*

As a Support Engineer, you will frequently edit this file to lock down the server.
1. `sudo vim /etc/ssh/sshd_config`
2. Change `PermitRootLogin yes` to `PermitRootLogin no`.
3. Change `PasswordAuthentication yes` to `PasswordAuthentication no` *(Only do this AFTER you have successfully tested key-based login!)*
4. Save the file.
5. `sudo systemctl restart sshd`. *(You must restart the daemon for it to read the new configuration).*

## Real-World Scenarios

**Customer:**
*"We are failing our security audit. The auditor's bot is brute-forcing our server on Port 22 with millions of password guesses for the root user. Stop this immediately."*

How should a Linux Support Engineer investigate?
* **Mental Map:** The server is exposed to the internet, and bots are guessing passwords. The fix is to completely disable root login and disable password authentication over SSH.
* **The Fix:** 
  1. The engineer ensures they have their Public Key installed on a standard user account and verifies they can escalate via `sudo`.
  2. The engineer opens `/etc/ssh/sshd_config`.
  3. They set `PermitRootLogin no` and `PasswordAuthentication no`.
  4. They run `systemctl restart sshd`.
  5. The bot immediately fails because the server no longer accepts passwords, and it completely rejects any attempt to log in directly as root.

## Hands-on Lab

> [!CAUTION]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 15 Practice Guide](../practice-files/V1-C15-practice.md). You will generate an RSA keypair and successfully harden your local SSH configuration.

## Interview Questions

### Question 1: What is the difference between `/etc/ssh/ssh_config` and `/etc/ssh/sshd_config`?
* **Target Answer**: "`ssh_config` controls the behavior of the SSH *client* (when you are connecting *out* to another machine). `sshd_config` controls the behavior of the SSH *daemon* (when users are connecting *in* to your machine)."

### Question 2: A customer lost their Private Key. Can you recover it from the Public Key stored on the server?
* **Target Answer**: "No. It is mathematically impossible (within current computational limits) to reverse-engineer a private key from a public key. The customer has permanently lost access. They must generate a new keypair, and we must manually copy their new public key to the server."

### Question 3: After changing `PermitRootLogin no` in the configuration file, you can still log in as root. Why?
* **Target Answer**: "You did not restart or reload the SSH daemon. Changes to `/etc/ssh/sshd_config` do not take effect dynamically; they require a `systemctl restart sshd` (or `reload`) to force the daemon to read the updated configuration from the disk."

## Chapter Summary

SSH is your primary weapon as a Linux Support Engineer. Understanding how to generate cryptographic keys, distribute them, and harden the `sshd_config` file is the difference between a secure enterprise environment and a compromised server. Remember: never share your private key, and always test your access before disabling passwords!

## Completion Checklist

- [ ] I understand the difference between a Public Key (the lock) and a Private Key (the key).
- [ ] I know which configuration file controls the server daemon.
- [ ] I remember to restart the `sshd` service after making configuration changes.

---

## Navigation

⬅ Previous:
[Chapter 14 – Networking Fundamentals](V1-C14-networking-fundamentals.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 16 – Archiving and Compression](V1-C16-archiving-and-compression.md)
