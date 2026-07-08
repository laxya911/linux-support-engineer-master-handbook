# Practice Guide: Chapter 19 (Volume 2)

## Objective
To practice thinking like a Senior Support Engineer by filling out a Root Cause Analysis (RCA) template for a fictional outage.

## The Fictional Scenario
You are the lead engineer. At 9:00 AM on Monday, the customer service team reports they cannot access the internal CRM website. 
You log in and check the firewall (`ufw status`). The firewall is completely disabled!
You ask the junior engineers what happened. One of them says: "I was tasked with opening port 8080 on Friday night. I accidentally typed `ufw disable` instead of `ufw allow 8080`. I realized my mistake and tried to SSH back in, but my SSH key didn't work, so I just went home for the weekend."
You check the SSH configuration (`/etc/ssh/sshd_config`) and see `PasswordAuthentication no`. 

## Assignment: Write the RCA
Create a new file called `rca_practice.md` and fill in the blanks based on the scenario above.

```markdown
# Root Cause Analysis: CRM Outage

**1. Incident Summary:**
(Briefly describe what happened and how long the system was down).

**2. Timeline of Events:**
* Friday Evening: 
* Monday 9:00 AM: 
* Monday 9:15 AM: 

**3. The 5 Whys:**
* **Why did the CRM website go offline?** 
  Because the server's firewall was completely disabled.
* **Why was the firewall disabled?**
  (Fill this in)
* **Why didn't the engineer immediately re-enable the firewall?**
  (Fill this in)
* **Why was the engineer unable to log back in using their SSH key?**
  (Think back to Chapter 12: What is the most common reason SSH ignores a key?)

**4. The Root Cause:**
(What is the actual, systemic issue here? Is it a lack of training on UFW? Is it a lack of a peer-review process for Friday night changes?)

**5. Preventative Action Items:**
(List two things your team must do this week to ensure this never happens again).
```

## Success Criteria
You have successfully completed this practice if you were able to trace the outage back to the junior engineer's command-line typo, their likely file permission issue, and proposed a concrete policy change (like banning Friday night deployments) to prevent a recurrence.
