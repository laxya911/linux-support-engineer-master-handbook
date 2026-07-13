---
volume: 1
chapter: 3
part: 1
id: V1-C03
title: Provisioning Linux
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 1.0.0
difficulty: Beginner
estimated_time: 2 Hours
reading_time: 40 Minutes
labs: 1
interview_questions: 2
prerequisites: Previous Chapter
last_updated: 2026-07
status: Published
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 3 — Provisioning Linux


## Learning Objectives

A server is only as good as its foundation. Whether you're deploying a local virtual machine or spinning up cloud infrastructure, understanding how to properly provision a Linux environment is your first step to building reliable systems.

By the end of this chapter, you will be able to:
* Explain the difference between installing a single OS via ISO and provisioning servers at scale.
* Understand why enterprise servers separate filesystems into different partitions (like `/var` and `/home`).
* Describe how Kickstart and Cloud-init automate bare-metal and cloud deployments.
* Compare bare-metal, virtualized, and cloud-native server provisioning.

## Introduction

In Chapter 1, we asked you to download an ISO and install Linux inside a virtual machine. This is how beginners learn, but it is not how enterprise IT works. 

If you are a Linux Support Engineer responsible for an infrastructure hosting 5,000 servers, you cannot insert 5,000 ISOs and click "Next" through an installation wizard. You need automation. You need standard templates. You need **Provisioning**.

This chapter transitions your mindset from *installing* a single server manually to *provisioning* fleet-wide infrastructure automatically. 

## Theory & Concepts

### 1. Storage Layouts: The Philosophy of Partitioning

When installing Linux manually, beginners often allocate 100% of the disk to a single partition (`/`, known as the **root partition**). In a production environment, this is extremely dangerous.

Why? Because if an application writes a massive log file until the disk reaches 100% capacity, the entire operating system will crash. The kernel cannot write to temporary files, SSH logins will fail, and the system becomes unrecoverable without out-of-band management.

Enterprise servers segregate the disk into distinct filesystems:
* `/` (**Root**): Contains the operating system binaries and core libraries.
* `/var` (**Variable Data**): Holds log files, databases, and application data. If a log file fills up `/var`, the OS running on `/` remains safe.
* `/home` (**User Data**): Holds files belonging to individual users.
* `/tmp` (**Temporary Files**): Holds temporary application data, often mounted directly in RAM.

> [!TIP] Support Engineer Tip #3
> **Protect the Root Filesystem.** If you are asked to provision a server for a third-party application, always insist on mounting `/opt` or `/var` on a separate virtual disk. Never let third-party logs compete with the kernel for disk space.

### 2. Automated Provisioning Technologies

Instead of humans clicking through installation screens, engineers write configuration files that answer the installation prompts automatically.

#### Kickstart (RHEL / CentOS)
Developed by Red Hat, a Kickstart file (`ks.cfg`) is a plain-text configuration file that dictates exactly how a server should be built. It defines the root password, network settings, partition layouts, and which packages to install.
> A bare-metal server boots via the network (PXE), retrieves the Kickstart file, and installs itself entirely unattended.

#### Preseed (Debian / Ubuntu)
The Debian equivalent to Kickstart. It provides answers to the `debconf` prompts that appear during an interactive Ubuntu installation.

#### Cloud-init (Cloud Environments)
If you deploy an Ubuntu VM in AWS or Azure, you are not installing an OS. You are cloning a pre-built image (an AMI). **Cloud-init** is the industry standard script that runs on the very first boot of that cloned image. It dynamically injects SSH keys, sets the hostname, and runs initial configuration scripts so the VM is ready for use immediately.

### 3. Bare-Metal vs. Virtual vs. Cloud

* **Bare-Metal**: Physical servers racked in a data center. Provisioning usually involves PXE (Preboot Execution Environment) booting over the network and pulling a Kickstart file.
* **Virtualization (VMware/Proxmox)**: You create a "Golden Image" (a perfectly configured virtual machine) and clone it. Provisioning takes seconds.
* **Cloud (AWS/Azure/GCP)**: The cloud provider manages the hypervisor. You request an instance via API (e.g., using Terraform), and Cloud-init configures it on boot.

## Real-World Scenarios

> [!IMPORTANT] Incident Report: The Locked Database Server
>
> **Problem:** End User (Dave): "We deployed a new database server yesterday. Today, nobody can SSH into it, and the website is throwing 500 Internal Server Errors."
>
> **Investigation:** Charlie cannot SSH into the server (`ssh: connect to host 10.0.1.50 port 22: Connection refused`). He logs into the hypervisor console and sees out-of-memory and no-space-left-on-device errors flooding the `dmesg` screen.
> 
> ```bash
> charlie@vmware-console:~$ df -h
> Filesystem      Size  Used Avail Use% Mounted on
> /dev/sda1        20G   20G     0 100% /
> ```
>
> **Evidence:** The root filesystem `/` is 100% full.
>
> **Wrong Assumption:** Bob (Junior Admin) says: "Let's increase the disk size in VMware and reboot it."
>
> **Root Cause:** Alice (Senior Admin) investigates *why* it filled up. Running `du -sh /*` reveals `/var/lib/mysql` is 18GB. The server was provisioned by a junior developer with a single 20GB `/` partition. As the database grew, it consumed the entire OS disk, leaving no space for the OS to create temporary session files for SSH.
>
> **Lessons Learned:** Increasing the disk size treats the symptom. The fix is to provision a secondary virtual disk, mount it at `/var/lib/mysql`, and migrate the data. This physically isolates the database growth from the operating system's stability.
## Hands-on Lab

> [!NOTE]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 3 Practice Guide](../practice-files/V1-C03-practice.md) to practice reading a Cloud-init configuration and designing enterprise storage layouts.

## Interview Questions

### Question 1: Why shouldn't you install a production database on a single root (/) partition?
**Scenario**: You are reviewing an infrastructure design with a junior engineer.
* **Target Answer**: "If the database grows unexpectedly and consumes all available disk space, the entire operating system will lock up. By separating the database directory (like `/var` or `/opt`) into its own partition or logical volume, we isolate the risk. If the partition fills up, the database crashes, but the OS remains accessible for troubleshooting."

### Question 2: What is the purpose of Cloud-init?
* **Target Answer**: "Cloud-init is a widely adopted utility used to customize cloud instances during their initial boot. It handles tasks like expanding the root filesystem to match the requested volume size, configuring network interfaces, injecting SSH public keys for secure access, and running startup scripts, allowing for fully automated provisioning."

> [!TIP] Support Engineer Tip #4: The SSH Lockout
> I once edited the `/etc/ssh/sshd_config` over a remote SSH session and restarted the service without keeping a second session open. The configuration was invalid, the SSH daemon crashed, and I could no longer connect to fix the typo. I had to wake up a datacenter technician at 3 AM to connect a physical keyboard.
>
> **Always keep a secondary SSH connection open until you've confirmed the new network or SSH configuration works.**



## Chapter Summary

Provisioning is about scale, consistency, and resilience. As a Support Engineer, understanding how a server was provisioned (via Kickstart, a cloned template, or Cloud-init) tells you how it receives its configuration. Understanding why disks are partitioned protects the systems you support from catastrophic failures. 

## Completion Checklist

- [ ] I understand the danger of a single root (`/`) partition.
- [ ] I can explain the difference between Kickstart and Cloud-init.
- [ ] I know why enterprise environments rely on automated provisioning.



**Chapter Transition**
> The server is provisioned, but what exactly happens between pressing the power button and seeing the login prompt?

---

## Navigation

⬅ Previous:
[Chapter 2 — Linux Architecture & Distributions](V1-C02-linux-architecture-and-distributions.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 4 — Linux Boot Process](V1-C04-linux-boot-process.md)
