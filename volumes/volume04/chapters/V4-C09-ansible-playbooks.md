---
volume: 4
chapter: 9
part: 2
id: V4-C09
title: Writing Ansible Playbooks & Roles
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
prerequisites: V4-C08
last_updated: 2026-07
status: In Progress
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 9 — Writing Ansible Playbooks & Roles

## Learning Objectives

Automation is only as good as the playbooks you write. In this chapter, we explore advanced Ansible Playbook design, focusing on idempotency, roles, and modular infrastructure management.

By the end of this chapter, you will be able to:
* Define Idempotency.
* Write a multi-task Ansible Playbook using YAML.
* Trigger service restarts conditionally using Handlers.
* Understand how Ansible Roles promote code reuse.

## Visual Architecture: The Playbook

Ad-Hoc commands are great for quick fixes (like changing a password). But if you want to deploy a complex NGINX web server, install SSL certificates, and configure log rotation, you cannot type 15 Ad-Hoc commands. 
Instead, you write an **Ansible Playbook**. A Playbook is a YAML file containing a list of `Tasks`. You simply run `ansible-playbook setup-web.yml`, and Ansible executes the tasks sequentially from top to bottom.

```mermaid
flowchart TD
    A["ansible-playbook web.yml "] --> B["Task 1: Install NGINX "]
    B --> C["Task 2: Copy index.html "]
    C --> D["Task 3: Ensure NGINX is started "]
    
    D -->|"If Task 2 changed a config file..."| E["Handler: Restart NGINX "]
    D -->|"If nothing changed..."| F["Done. Playbook exits."]
    
    style A fill:#8e44ad,stroke:#9b59b6,color:#fff
    style E fill:#f39c12,stroke:#f1c40f,color:#000

```

## Theory & Concepts

### 1. Idempotency (The Golden Rule)
A bash script is usually *not* idempotent. If a bash script says `echo "text" >> file.txt`, and you run the script 5 times, you will get 5 lines of text. This breaks the server.
**Idempotency** means you can run an Ansible Playbook 100 times, and the result is exactly the same as running it 1 time. Ansible Modules check the current state of the server *before* making a change. If the server already matches the Playbook, Ansible reports `ok` and skips the task entirely.

### 2. Handlers
If you copy a new `nginx.conf` file to a server, you must restart the NGINX service for the changes to take effect. But if you run the Playbook tomorrow (and the config hasn't changed), you *don't* want to restart NGINX and cause a blip in traffic!
**Handlers** solve this. A Handler is a special task that only runs at the very end of the Playbook, and *only* if another task specifically triggered it via a `notify` statement. 

### 3. Roles
As your infrastructure grows, your Playbook will become 2,000 lines long and impossible to read. **Roles** allow you to break your Playbook into modular, reusable folders. You can create a `mysql` role and a `nginx` role. If a new project requires a database, you just include the `mysql` role in the new Playbook instead of rewriting the tasks!

## Scenario-Based Troubleshooting

### Scenario A: The Configuration Drift

> [!IMPORTANT]  
> **Incident Report: The Configuration Drift**  
> **Reporter:** Automated Monitoring / End User  
> **The Incident:** A company has 10 identical NGINX load balancers. Over the course of three years, different system administrators manually SSH into the servers during emergencies to tweak configurations. 
Eventually, the servers begin acting strangely. Server 3 drops SSL connections, and Server 7 runs out of memory. The environment has suffered from **Configuration Drift**. The servers are no longer identical.


**The Investigation (Single Engineer Diagnosis):**

1. The Senior DevOps Engineer refuses to log into 10 servers to manually find the differences.

2. The engineer writes a definitive `nginx-baseline.yml` Ansible Playbook containing the exact, correct state of the load balancers (the correct packages, the correct config files, the correct SSL certificates).

3. The engineer runs `ansible-playbook nginx-baseline.yml -i inventory.ini`.
4. **The Orchestration Magic:** Because Ansible is Idempotent, it scans all 10 servers. 
    * On Server 1 (which was correct), Ansible reports `ok` and does nothing. 
    * On Server 3, Ansible notices the SSL config is wrong, overwrites it with the correct file, and triggers a Handler to restart NGINX. 
    * On Server 7, Ansible notices a rogue memory-hogging package was manually installed by a Junior Admin, and uninstalls it.
5. Within 60 seconds, all 10 servers are forcefully brought back into perfect, identical alignment. The engineer then schedules the Playbook to run every night via Cron to ensure Configuration Drift never happens again.

> [!IMPORTANT]  
> **Best Practice: Cattle, Not Pets**  
> If an administrator manually edits a config file on a production server (treating it like a Pet), the nightly Ansible Playbook will overwrite their changes (treating it like Cattle). Administrators must be trained to *never* SSH into servers to make changes. If a config change is required, they must edit the Ansible Playbook in Git and let the CI/CD pipeline deploy it to all servers simultaneously.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 9 Practice Guide](../practice-files/V4-C09-practice.md) to write an Idempotent Playbook with a conditional Handler!

## Interview Questions

### Question 1: What is 'Idempotency' in the context of Configuration Management?
* **Target Answer**: "Idempotency is the property where an operation can be applied multiple times without changing the result beyond the initial application. In Ansible, this means if you run a Playbook 10 times, the server's end state is exactly the same as if you ran it once. Ansible achieves this by checking the current state of the server and only applying changes if the server deviates from the desired state."

### Question 2: How do Handlers differ from standard Tasks in an Ansible Playbook?
* **Target Answer**: "Standard Tasks are executed sequentially from top to bottom every time the Playbook runs. Handlers are special tasks that only execute at the very end of the Playbook, and they *only* execute if they were explicitly triggered (notified) by a standard Task that reported a 'changed' state. This is critical for preventing unnecessary service restarts when configuration files haven't actually been modified."

### Question 3: Explain the concept of 'Configuration Drift' and how Ansible solves it.
* **Target Answer**: "Configuration Drift occurs when servers in a cluster gradually become misaligned over time due to manual, undocumented changes made by administrators directly on the servers. Ansible solves this by acting as the declarative Source of Truth. By running an idempotent Playbook periodically (e.g., nightly), Ansible detects any manual deviations on the servers and forcefully reverts them back to the standardized baseline."

## Chapter Summary

Playbooks are the heart of Ansible. They allow you to define the perfect server setup once, and then apply that perfection to 1 server or 10,000 servers. By embracing idempotency and roles, you ensure your infrastructure is always predictable, scalable, and self-documenting.

## Completion Checklist

- [ ] I can define Idempotency.
- [ ] I understand how to use `notify` to trigger a Handler.
- [ ] I understand the danger of Configuration Drift.

---

## Navigation

⬅ Previous:
[Chapter 8 – Configuration Management at Scale](V4-C08-ansible-intro.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 10 – CI/CD Pipelines](V4-C10-cicd-pipelines.md)
