---
volume: 2
chapter: 4
part: 2
id: V2-C04
title: Logical Volume Management (LVM)
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

# Chapter 4 — Logical Volume Management (LVM)


## Learning Objectives

By the end of this chapter, you will be able to:
* Explain why standard disk partitions are rigid and dangerous for enterprise workloads.
* Define the 3 layers of LVM: Physical Volumes (PV), Volume Groups (VG), and Logical Volumes (LV).
* Add a new hard drive to an existing Volume Group.
* Extend a live filesystem using `lvextend` and `resize2fs` (or `xfs_growfs`).


> [!IMPORTANT]
> **ServiceNow Ticket: INC-57671**
> **Priority:** High
> **Reported By:** Enterprise Application Team
> **Issue:** We are experiencing a critical failure related to Logical Volume Management (LVM). Please investigate immediately.
> 
> **Support Engineer Objective:** Use operational thinking to collect evidence, identify the root cause, and restore service without causing further disruption.

## Visual Architecture: The Storage Pool

In traditional Linux setups (like you learned in Volume 1), you format a hard drive and create a partition. If that partition fills up, you are trapped. 
LVM solves this by creating an abstract "pool" of storage. You throw hard drives into the pool, and then you scoop out flexible chunks of storage called Logical Volumes. 

```mermaid
flowchart TD
    A["Hard Drive 1 \n 50GB"] --> C{"Volume Group \n 'ubuntu-vg' \n 150GB Pool"}
    B["Hard Drive 2 \n 100GB"] --> C
    
    C -->|"Carve out 20GB"| D["Logical Volume \n '/' (Root)"]
    C -->|"Carve out 80GB"| E["Logical Volume \n '/var' (Databases)"]
    C -->|"50GB Remaining"| F["Free Space \n (Ready for emergencies)"]
    
    style A fill:#2d3436,stroke:#b2bec3,color:#fff
    style B fill:#2d3436,stroke:#b2bec3,color:#fff
    style C fill:#0984e3,stroke:#74b9ff,color:#fff
    style D fill:#00b894,stroke:#55efc4,color:#000
    style E fill:#00b894,stroke:#55efc4,color:#000
    style F fill:#f39c12,stroke:#f1c40f,color:#000
```

## Theory & Concepts

### 1. The 3 Layers of LVM
LVM acts as an abstraction layer between the physical hard drive and the operating system.
1. **Physical Volumes (PV):** The actual, physical hard drives plugged into the server (e.g., `/dev/sdb`). You use the `pvcreate` command to mark them for LVM use.
2. **Volume Groups (VG):** The giant pool of storage. You use `vgcreate` to group multiple PVs together. If you group two 50GB drives together, you get a 100GB VG.
3. **Logical Volumes (LV):** The virtual partitions you carve out of the VG. You use `lvcreate` to make them, and then you format them with a filesystem (like `ext4`) and mount them to a folder.

### 2. The Commands
You can view the state of your LVM architecture at any time using three simple commands:
* `pvs` (Physical Volume Status)
* `vgs` (Volume Group Status)
* `lvs` (Logical Volume Status)

## Scenario-Based Troubleshooting

### Scenario A: The Full Disk Emergency
**The Incident:** An automated monitoring alert fires: `CRITICAL: /var is 100% full`. The `/var` directory is where the production MySQL database lives. Because the disk is full, the database crashes. Customers cannot place orders. 

**The Investigation & Fix:**

1. The Support Engineer logs in and runs `df -h`. They confirm that `/dev/mapper/ubuntu--vg-var` is at 100% usage.
2. The engineer runs `vgs` to check if there is any free space left in the storage pool. The output shows `VFree: 50g`. They have 50GB of unassigned storage sitting in the pool!
3. The engineer uses LVM to instantly extend the partition:
   `lvextend -L +50G /dev/mapper/ubuntu--vg-var`
4. The LVM partition is now larger, but the filesystem sitting *inside* the partition doesn't know it yet. The engineer must expand the filesystem to fill the new space.
   * If the filesystem is `ext4` (Ubuntu standard): `resize2fs /dev/mapper/ubuntu--vg-var`
   * If the filesystem is `xfs` (RHEL standard): `xfs_growfs /var`
5. The engineer runs `df -h` again. The `/var` partition now has 50GB of free space.
6. The engineer runs `systemctl start mysql`. The database comes back online.

> [!IMPORTANT]  
> Notice that the engineer **never rebooted the server** and **never unmounted the drive**. LVM allows you to resize live filesystems while the server is running in production!


## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 4 Practice Guide](../practice-files/V2-C04-practice.md) to use `lsblk` and the LVM status commands to map out your own server's storage architecture.

## Interview Questions

### Question 1: What is the primary advantage of using LVM (Logical Volume Management) over standard partitions?
* **Target Answer**: "Standard partitions are rigid; if a standard partition fills up, resizing it usually requires unmounting the drive and experiencing downtime. LVM creates an abstraction layer that allows administrators to pool multiple physical hard drives together and dynamically resize Logical Volumes on the fly, without unmounting the filesystem or rebooting the server."

### Question 2: You just added 20GB of space to a Logical Volume using `lvextend`, but when you run `df -h`, the extra space does not show up. What step did you forget?
* **Target Answer**: "I forgot to resize the filesystem that sits on top of the Logical Volume. `lvextend` only increases the size of the block device. I must also run `resize2fs` (for ext4 filesystems) or `xfs_growfs` (for XFS filesystems) to instruct the filesystem to expand into the newly provided space."

### Question 3: Explain the relationship between a PV, a VG, and an LV.
* **Target Answer**: "A Physical Volume (PV) is the raw hard drive. Multiple PVs are pooled together to create a Volume Group (VG), which acts as a giant bucket of unified storage. From that Volume Group, administrators carve out smaller, flexible virtual partitions called Logical Volumes (LV), which are then formatted and mounted to the operating system."

## Chapter Summary

Storage emergencies are the most stressful events in IT. LVM reduces that stress by giving you flexibility. Always leave 20% of your Volume Group unallocated (free). That way, when a partition fills up in the middle of the night, you can instantly `lvextend` and `resize2fs` your way out of the crisis.

## Completion Checklist

- [ ] I can define PV, VG, and LV.
- [ ] I understand why `lvextend` must always be followed by `resize2fs` or `xfs_growfs`.
- [ ] I can list the commands to view LVM architecture (`pvs`, `vgs`, `lvs`).

---

## Navigation

← Previous: [Chapter 3 — Centralized Authentication](V2-C03-centralized-authentication.md)

↑ Volume Contents: [Table of Contents](TOC.md)

→ Next: [Chapter 5 — RAID Arrays](V2-C05-raid-arrays.md)
