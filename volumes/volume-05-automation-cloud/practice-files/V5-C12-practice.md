# Practice Guide: Chapter 12 (Volume 5)

## Objective
To identify operational Toil within a theoretical company and conceptually design a Python automation solution to eliminate it.

## Assignment 1: Identifying Toil
You have just been hired as a Senior SRE at a mid-sized tech company. You review the internal ticketing system and find the following three tickets created this week:

1. **Ticket 1:** "Please update the NGINX configuration to support TLS 1.3 across the 5 web servers."

2. **Ticket 2:** "New employee onboarding: Please create an AWS IAM user for John Doe, assign him to the Developer group, and email him the temporary password."

3. **Ticket 3:** "Research and design a new highly available architecture for the billing microservice."

**Analysis:** Which of these tickets is Toil?
* Ticket 1 is *Engineering Work*. It is a one-time architectural upgrade that provides enduring security value.
* Ticket 2 is pure **Toil**. It is manual, it requires no creative thought, it is highly repetitive (you do it every time someone is hired), and it scales linearly (if they hire 100 people, it takes 100 times longer).
* Ticket 3 is *Engineering Work*.

## Assignment 2: Designing the Automation
As an SRE, you refuse to do Ticket 2 manually. You decide to spend 4 hours writing a Python script to automate it permanently.

1. **The Inputs:** The script needs the new employee's First Name, Last Name, and Department.

2. **The Process (The Python Logic):**
   * Use `boto3` to connect to AWS IAM.
   * Generate a username (`first.last`).
   * Call `iam.create_user(UserName="john.doe")`.
   * Call `iam.add_user_to_group(GroupName="Developers")`.
   * Call `iam.create_login_profile()` with an auto-generated random password.
   * Use the `requests` library to connect to the Slack API and automatically DM the new user their credentials on their first day.

3. **The Output:** Zero human intervention required.

## Assignment 3: The Business Value

1. The manual process took 15 minutes per employee.

2. The company plans to hire 200 engineers this year.

3. 200 * 15 minutes = **50 Hours of Toil**.
4. By spending 4 hours writing this Python script, you just gave the company back 46 hours of highly paid engineering time. 
5. *This* is why SREs are paid more than traditional SysAdmins. They do not just close tickets; they permanently destroy the system that generates the tickets.

## Success Criteria
You have successfully completed this practice if you can look at any daily operational task and instantly identify if it meets the definition of Toil (Manual, Repetitive, Automatable, Tactical).
