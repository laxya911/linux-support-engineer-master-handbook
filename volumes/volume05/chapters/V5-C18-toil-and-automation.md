# Chapter 18: Eliminating Toil

If you are fighting fires 40 hours a week, you are not an engineer; you are a firefighter. 

The core tenant of Site Reliability Engineering (SRE) is that operations is a software problem. If a human is manually resetting a database connection, expanding a full hard drive, or adding a new user to a VPN, the system is fundamentally broken.

Google defines this type of manual, repetitive work as **Toil**. To advance to a Senior Engineer, you must declare war on Toil.

## What is Toil?

Not all work is Toil. Writing a Python script is engineering. Sitting in a sprint planning meeting is overhead. 

Toil has very specific characteristics:
1. **Manual:** A human is typing commands.
2. **Repetitive:** You are doing the exact same task you did last week.
3. **Automatable:** A machine could easily be programmed to do it.
4. **Reactive:** You are doing it because an alert fired or a user submitted a ticket.
5. **No Enduring Value:** After you finish the task, the system is in the exact same state it was yesterday. It has not improved.

If your team is spending 80% of their time on Toil, they have 0% time to build automation to prevent the Toil. This is a death spiral that causes massive engineer burnout.

## The 50% Rule

SRE teams strictly enforce the 50% Rule: **No engineer should spend more than 50% of their time on Toil (Ops work).** The other 50% must be spent on Engineering (writing code, building automation, and improving the architecture).

If a team breaches the 50% limit, they pull the Andon Cord. They route all incoming support tickets directly to the Development teams until the SRE team has enough breathing room to automate the repetitive tickets away.

## How to Eliminate Toil

### 1. Self-Service Portals
If the database team spends 10 hours a week manually running SQL queries to grant developers access to staging databases, that is Toil. 
* **The Fix:** Build a self-service Slack bot. The developer types `/db-access staging`. The bot automatically provisions temporary, time-bound credentials and DMs them to the developer. The database team never even sees the ticket.

### 2. Auto-Remediation
If an engineer gets paged at 2:00 AM every Tuesday because a legacy Java application leaks memory, and the "fix" is to SSH into the server and run `systemctl restart tomcat`, that is Toil.
* **The Fix:** Do not just write a script. Hook the script into the monitoring system. When Datadog detects the memory usage crossing 95%, Datadog automatically triggers a webhook to an AWS Lambda function that restarts the service. The engineer sleeps through the night. (And the next morning, they write an Action Item to actually fix the Java code).

### 3. Infrastructure as Code (IaC)
If an engineer spends 4 hours clicking through the AWS console to provision a new VPC and 10 EC2 instances for a new client, that is Toil.
* **The Fix:** Write the infrastructure in Terraform. The next time a client is onboarded, provisioning the infrastructure takes 45 seconds.

---

## Scenario-Based Troubleshooting

### Scenario A: The Disk Space Loop

> [!IMPORTANT]  
> **Incident Report: The Midnight Disk Expansion**  
> **Reporter:** SRE On-Call  
> **SOP execution:**
> 
> 1. **03:00 AM — Incident Receipt:** An engineer is paged because `/var/log` on the primary NGINX proxy has reached 98% capacity.
> 
> 2. **03:05 AM — Triage & Containment:** The engineer logs in via SSH, verifies the disk is almost full, and runs `logrotate -f /etc/logrotate.d/nginx` to forcefully compress and delete old logs. The disk space drops to 40%. The engineer goes back to sleep.
> 
> 3. **03:00 AM (Next Week) — Incident Receipt:** The engineer is paged again for the exact same alert on the exact same server. They run the exact same command.
> 
> 4. **09:00 AM (Next Morning) — Investigation:** The engineer refuses to do this a third time. They declare this task "Toil." They investigate *why* the disk is filling up faster than the standard logrotate schedule. They discover that a recent marketing campaign increased proxy traffic by 500%, generating 5x more logs per day.
> 
> 5. **09:30 AM — Resolution:** The engineer edits the `logrotate` configuration to rotate logs based on `size 500M` instead of `daily`. 
> 
> 6. **10:00 AM — Verification:** They monitor the server for 48 hours. Logrotate now correctly triggers multiple times a day based on the massive file size, keeping the disk space permanently below 60%.
> 
> 7. **Post-Mortem:** Discuss why the alert threshold was reactive instead of proactive.
> 
> 8. **Documentation:** Update the default base image (AMI) so all future servers use size-based log rotation rather than time-based.

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Automating a broken process. If a deployment process requires 15 manual approvals, 4 Jira tickets, and 3 hours of downtime, do not write a Bash script to automate the Jira tickets. You must re-engineer the process to remove the downtime and the approvals *before* you automate it. Automating garbage just produces faster garbage.

> [!TIP] Pro-Tip
> Use "ChatOps" to track Toil. If you have an automated script that expands a full hard drive, don't let it run silently in the background. Have the script post a message to a Slack channel: `🤖 [Auto-Remediation] Expanded /dev/sda1 on db-prod-04 by 50GB.` This gives the engineering team visibility into how often the automation is firing, allowing them to eventually fix the root cause (e.g., adding a larger drive permanently).

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 18 Practice Guide](../practice-files/V5-C18-practice.md) to write a fully automated Bash script that detects a dead service and automatically restarts it without human intervention!

## Interview Questions

### Question 1: How does Google SRE define "Toil"?
* **Target Answer**: "Toil is not just 'work I don't like.' Toil is work that is manual, repetitive, automatable, reactive, and lacks enduring value. If completing a task leaves the system in the exact same state it was yesterday, it is Toil. Conversely, writing a Terraform script is not Toil, because it provides permanent, enduring value to the organization."

### Question 2: Why do SRE teams enforce the '50% Rule' for Operations work?
* **Target Answer**: "If an engineering team spends 100% of their time fighting fires and closing repetitive support tickets, they will eventually burn out and quit. More importantly, they will never have the time to write the automation required to prevent those fires in the first place. Capping ops work at 50% guarantees that the team always has dedicated time to engineer permanent solutions."

### Question 3: Give an example of turning Toil into Self-Service.
* **Target Answer**: "If developers constantly open IT tickets asking for read-only access to staging databases, and an administrator spends 5 hours a week manually running SQL `GRANT` commands, that is Toil. The solution is to build a self-service tool (like a Slack bot or an internal web portal) where developers can click a button to automatically provision their own temporary credentials, completely removing the human administrator from the loop."



**Chapter Transition**
> Automation has eliminated toil. But how do we train the junior engineers to handle the stress of a real outage? We run War Room Simulations.

---

## Navigation

⬅ Previous:
[Chapter 17: The Blameless Post-Mortem](V5-C17-blameless-post-mortem.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 19: War Room Simulation: The Database Meltdown](V5-C19-war-room-simulation.md)
