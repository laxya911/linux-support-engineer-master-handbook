# Chapter 17: The Blameless Post-Mortem

When the fire is out and the systems are running again, the natural human instinct is to close the laptop, breathe a sigh of relief, and never think about the incident again. 

This is the fastest way to guarantee the exact same outage happens next month.

The true value of an incident is not the downtime; it is the *data*. An incident is the system telling you exactly where its breaking point is. To extract that data, Senior Engineers write a **Post-Mortem**.

## What is a Post-Mortem?

A Post-Mortem is a formal, written document that explains an incident from start to finish. It is the most important document a Site Reliability Engineer writes. 

A good Post-Mortem answers three questions:
1. What went wrong?
2. Why did it go wrong?
3. What are we changing *today* to ensure this never happens again?

A Post-Mortem is not a quick email. It is a highly structured document that is heavily scrutinized by the engineering team.

## The Core Principle: Blamelessness

The most critical rule of a Post-Mortem is that it must be **blameless**. 

If an engineer runs a script that deletes the production database, the Post-Mortem must *never* state: "Alice made a careless mistake and deleted the database. We told Alice to be more careful."

If you blame Alice, you create a culture of fear. Next time Alice makes a mistake, she will hide it, hoping nobody notices. The outage will last longer, and the true root cause will never be discovered.

A Blameless Post-Mortem assumes that every engineer is competent and acts with good intentions based on the information they had at the time. Therefore, if Alice deleted the database, the failure is a *systemic* failure. 

The Blameless Post-Mortem asks:
* Why was Alice able to run a destructive script without an automated peer review?
* Why did the staging environment give Alice false confidence that the script was safe?
* Why didn't our IAM permissions block a junior engineer from executing a `DROP TABLE` command in production?

You do not fix Alice. You fix the system.

## The Structure of a Post-Mortem

A standard SRE Post-Mortem contains the following sections:

### 1. Executive Summary
A one-paragraph, non-technical summary of the incident for leadership.
*(e.g., "From 14:00 to 15:30 on Tuesday, the primary payment gateway failed, causing a 10% drop in revenue. The root cause was a memory leak in the v2.4 deployment. We rolled back to v2.3 to restore service.")*

### 2. Impact
A brutal, honest assessment of the damage. 
*(e.g., "450,000 user requests failed with HTTP 500 errors. 14,000 checkout transactions were dropped. Estimated revenue loss: $120,000.")*

### 3. Timeline
A minute-by-minute transcript of the incident response.
*(e.g., "14:02 - PagerDuty alert fires. 14:05 - Alice joins the War Room. 14:15 - Bob identifies the memory leak.")*

### 4. Root Cause Analysis (The 5 Whys)
You must dig past the symptoms to find the core systemic failure using the "5 Whys" technique.
* *Why did the API crash?* Because it ran out of memory.
* *Why did it run out of memory?* Because the new image resizing library leaks memory.
* *Why was the library deployed?* Because it passed the CI/CD pipeline.
* *Why did it pass CI/CD?* Because we don't have long-running load tests in staging.
* *Root Cause:* Lack of automated load testing allowed a memory leak to reach production.

### 5. Action Items (The Most Important Section)
A list of Jira tickets created specifically to fix the root cause. If a Post-Mortem has no Action Items, it is a worthless document. 

---

## Scenario-Based Troubleshooting

### Scenario A: The Witch Hunt

> [!IMPORTANT]  
> **Incident Report: The Erased Configs**  
> **Reporter:** SRE Manager  
> **SOP execution:**
> 
> 1. **10:00 AM — Incident Receipt:** An engineer (Charlie) meant to clean up temporary files in `/tmp/configs/` using `rm -rf *`, but accidentally executed the command in `/etc/nginx/`, deleting all production web server configurations. NGINX crashed globally.
> 
> 2. **10:45 AM — Resolution:** Service is restored by pulling the NGINX configs from the Git repository and restarting the proxies.
> 
> 3. **11:00 AM — Post-Mortem Drafting:** The Engineering Manager starts writing the Post-Mortem. Their initial draft says: *"Root Cause: Charlie ran the wrong command. Action Item: Charlie must complete Linux CLI training."*
> 
> 4. **11:15 AM — Investigation (Blameless Review):** The SRE Lead rejects the draft. They rewrite the root cause using the 5 Whys. They discover that Charlie was logged in as `root` because the company's `sudo` policies are broken, forcing engineers to use `su -` for daily tasks. Furthermore, the NGINX servers are manually configured "pets," not immutable Terraform infrastructure, meaning a deleted file on the server actually takes the site down.
> 
> 5. **11:30 AM — Final Root Cause:** The root cause is a lack of immutable infrastructure and overly permissive default IAM roles.
> 
> 6. **11:45 AM — Action Items:** 
>    * Ticket 1: Revoke direct SSH access to production web servers.
>    * Ticket 2: Convert all NGINX deployments to immutable Docker containers running in Kubernetes.
> 
> 7. **Documentation:** Publish the Blameless Post-Mortem to the entire company wiki to share the learnings globally.

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Writing Action Items like "Investigate better monitoring" or "Be more careful when deploying." Action items must be concrete, verifiable engineering tasks. "Write a Prometheus alerting rule that triggers when NGINX CPU exceeds 80% for 5 minutes" is a good action item.

> [!TIP] Pro-Tip
> The timeline section of a Post-Mortem is notoriously difficult to write from memory. This is why you must use a dedicated Slack channel during the War Room (as discussed in Chapter 16). You can simply export the timestamps and chat logs from the Slack channel directly into the Post-Mortem timeline.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 17 Practice Guide](../practice-files/V5-C17-practice.md) to read an incident summary and write a formal, blameless Post-Mortem using the 5 Whys!

## Interview Questions

### Question 1: What is the core philosophy of a "Blameless" Post-Mortem?
* **Target Answer**: "A blameless post-mortem assumes that every engineer acted with good intentions and competence based on the information they had. Instead of blaming human error (e.g., 'Alice ran the wrong script'), it focuses entirely on the systemic failures that allowed the human error to occur (e.g., 'Why wasn't the script peer-reviewed? Why did the system allow a junior engineer to execute a destructive command in production without safeguards?'). You fix the system, not the human."

### Question 2: How do you use the '5 Whys' technique in Root Cause Analysis?
* **Target Answer**: "The 5 Whys technique prevents you from stopping at the symptom. You start with the failure ('The database crashed') and ask 'Why?' ('It ran out of disk space'). You ask 'Why?' again ('Because logs filled up the drive'). You keep asking 'Why?' until you reach a fundamental process or architecture flaw ('Because our log rotation script was never added to the CI/CD deployment template'). That final answer is the true root cause."

### Question 3: What makes a 'good' Action Item in a Post-Mortem?
* **Target Answer**: "A good action item must be a concrete, measurable, and assignable engineering task with a clear deadline. Vague statements like 'improve monitoring' are useless. A good action item is: 'Create a Datadog alert for Disk Space > 85%, assign to Bob, due by Friday.' Without concrete action items, the post-mortem is just an essay that won't prevent the incident from recurring."

---

## Navigation

⬅ Previous:
[Chapter 16 – Incident Command System (ICS)](V5-C16-incident-command.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 18 – Game Days and Chaos Testing](V5-C18-game-days.md)
