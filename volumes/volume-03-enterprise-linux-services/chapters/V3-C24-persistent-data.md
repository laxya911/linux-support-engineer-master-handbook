---
volume: 3
chapter: 24
part: 5
id: V3-C24
title: Persistent Data & Networking
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Advanced
estimated_time: 1.5 Hours
reading_time: 25 Minutes
labs: 1
interview_questions: 3
prerequisites: V3-C23
last_updated: 2026-07
status: In Progress
---

# Chapter 24 — Persistent Data & Networking

* **Difficulty:** Advanced
* **Estimated Time:** 1.5 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

By the end of this chapter, you will be able to:
* Define "Container Ephemerality".
* Differentiate between Bind Mounts and Named Volumes.
* Persist database data across container restarts.
* Understand the default Bridge network.

## Visual Architecture: The Ephemeral Box

Containers are **Ephemeral**. This means they are designed to die. 
If you want to upgrade your NGINX version from 1.20 to 1.21, you do not log into the container and run `apt-get upgrade`. You destroy the container completely, download the new `nginx:1.21` image, and spin up a brand new container in 0.5 seconds. 
However, when a container is destroyed, its entire filesystem is deleted permanently. This is fine for web servers (they are stateless). This is a disaster for databases.

```mermaid
flowchart TD
    subgraph The Host OS (Safe)
        A[("/var/lib/docker/volumes/my_data/ \n (Named Volume)")]
    end
    
    subgraph The Ephemeral Container (Danger)
        B["MySQL Container \n (V 8.0)"]
    end
    
    B -->|Mounts Data To| A
    
    note1["If the MySQL Container is destroyed, \n the data in the Named Volume survives!"] -.-> A
    
    style A fill:#00b894,stroke:#55efc4,color:#000
    style B fill:#d63031,stroke:#ff7675,color:#fff
```

## Theory & Concepts

### 1. Named Volumes
To prevent data loss, you must poke a hole in the container's isolation. A **Named Volume** tells Docker: "Create a safe folder on the Host OS hard drive, and mount it inside the container at `/var/lib/mysql`." 
When MySQL writes data, it thinks it is writing to its own local filesystem, but it is actually writing to the Host OS. When the container is destroyed, the Host OS folder remains perfectly intact.

### 2. Bind Mounts
A Bind Mount is similar to a Named Volume, but instead of letting Docker manage the folder location, you explicitly define the exact Host path. 
For example: `volumes: - "/home/user/html:/usr/share/nginx/html"`.
This is amazing for development! If you edit the HTML file on your laptop (`/home/user/html`), it instantly updates inside the running web container without requiring a rebuild.

### 3. The Bridge Network
By default, Docker places all containers on a virtual `bridge` network (usually `172.17.0.0/16`). Containers can ping the outside internet because Docker sets up NAT (Network Address Translation) masquerading through the host's physical network interface.

## Scenario-Based Troubleshooting

### Scenario A: The Lost Database
**The Incident:** A security bulletin announces a critical vulnerability in Postgres 14.2. A junior engineer edits the `docker-compose.yml` file, updating the image to `postgres:14.3`, and runs `docker compose up -d`. 
Docker gracefully destroys the old container and spins up the new one. Ten minutes later, the customer support phones begin to ring. Every single customer account on the website is gone. The database is totally empty.

**The Investigation & Fix:**
1. The Support Engineer looks at the junior's `docker-compose.yml` file. It looks like this:
   ```yaml
   services:
     db:
       image: postgres:14.3
   ```
2. The engineer shakes their head. "You didn't define a volume. When Docker destroyed the 14.2 container, it took its entire internal filesystem with it. The data was inside the container, so it is gone forever."
3. The engineer restores the data from last night's AWS S3 backup. 
4. They fix the `docker-compose.yml` file to include a Named Volume, ensuring this never happens again:
   ```yaml
   services:
     db:
       image: postgres:14.3
       volumes:
         - pg_data:/var/lib/postgresql/data
   
   volumes:
     pg_data:
   ```
5. **The Result:** The `pg_data` volume is created on the Host OS. The engineer tells the junior: "Now, you can destroy this container a thousand times. When the new container spins up, it will re-attach to the `pg_data` volume, and all the customer data will still be there."

> [!IMPORTANT]  
> **Best Practice: Stateless vs. Stateful**  
> Web servers, PHP applications, and Python scripts should be "Stateless" (no volumes required). If they die, a new one spins up and instantly takes over. Databases and Caches are "Stateful". They must *always* have a Volume attached.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 24 Practice Guide](../practice-files/V3-C24-practice.md) to deliberately destroy a container and prove your data survived using a Named Volume!

## Interview Questions

### Question 1: What does it mean when we say Docker containers are 'ephemeral'?
* **Target Answer**: "Ephemerality means that containers are temporary, disposable, and designed to be destroyed and replaced at any time (for scaling or updates). Because of this, the container's internal filesystem is also temporary. Any data written directly inside a container is permanently lost the moment the container is deleted or recreated."

### Question 2: A Junior Engineer updates a database container to a newer image version. When the new container boots, all previous data is gone. What caused this?
* **Target Answer**: "The engineer failed to configure a Docker Volume. When the old container was destroyed to make way for the new image, the internal filesystem was wiped. To fix this, the database directory (e.g., `/var/lib/mysql`) must be mounted to a Named Volume or a Bind Mount on the Host OS, ensuring the data persists independently of the container lifecycle."

### Question 3: What is the difference between a Named Volume and a Bind Mount?
* **Target Answer**: "A Named Volume is fully managed by Docker. You simply provide a name (e.g., `db_data`), and Docker creates the directory in a secure location on the host (`/var/lib/docker/volumes/`). A Bind Mount requires the engineer to explicitly specify a hardcoded path on the host system (e.g., `/home/user/project`). Bind Mounts are excellent for local development, while Named Volumes are preferred for production data safety."

## Chapter Summary

Data gravity is real. You can treat your web servers like disposable cattle, but your databases must be treated like pets. Volumes are the anchor that ties ephemeral compute containers to permanent, safe storage.

## Completion Checklist

- [ ] I understand why containers should never be upgraded from the inside.
- [ ] I understand the difference between a Bind Mount and a Named Volume.
- [ ] I know how to attach a volume in a `docker-compose.yml` file.

---

## Navigation

⬅ Previous:
[Chapter 23 – Multi-Container Apps (Docker Compose)](V3-C23-docker-compose.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 25 – Introduction to Orchestration (K8s Prep)](V3-C25-orchestration-intro.md)
