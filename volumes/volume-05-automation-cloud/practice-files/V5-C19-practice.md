# Practice Guide: Chapter 19 (Volume 5)

## Objective
To conceptually write a Blameless Post-Mortem document for a theoretical outage.

## Assignment 1: The Outage Scenario
* **The Event:** On Tuesday at 10:00 AM, the primary e-commerce website went offline for 45 minutes.
* **The Cause:** A junior developer, Dave, was trying to test a new CSS layout. He accidentally pushed his code to the `main` branch instead of his `feature` branch. The CI/CD pipeline immediately deployed it to production. The CSS file had a typo that crashed the frontend framework.

## Assignment 2: The Blame-Oriented Post Mortem (How NOT to do it)
If a traditional IT manager wrote the post-mortem, it would look like this:
> "Dave was careless and pushed untested code to production. He ignored the company policy that says you must test in staging first. Dave has been formally reprimanded and told to be more careful in the future."

*Why this fails:* "Be more careful" is not an engineering strategy. Dave will eventually make another mistake.

## Assignment 3: The Blameless Post-Mortem
Write the SRE version of the post-mortem.

1. **The Core Philosophy:** Assume Dave is a good developer who was trying to do his job.
2. **The 'Five Whys' Root Cause Analysis:**
   * *Why did the site crash?* Because bad CSS was deployed to production.
   * *Why was it deployed?* Because Dave pushed directly to the `main` branch.
   * *Why was he able to push to `main`?* Because Branch Protection rules were not enabled in GitHub.
   * *Why did the CI/CD pipeline deploy bad code?* Because we don't have automated syntax testing in the pipeline.

3. **The Action Items (The Real Fix):**
   * **Action 1 (High Priority):** Enable GitHub Branch Protection on the `main` branch. Force all code to require a Pull Request and a secondary review before merging. (Assigned to: DevOps Team).
   * **Action 2 (Medium Priority):** Add a CSS/JS Linter step to the Jenkins CI/CD pipeline. If the linter detects a syntax error, the build must automatically fail before reaching production. (Assigned to: QA Team).

## Success Criteria
You have successfully completed this practice if you understand that human error is inevitable. You cannot fix humans. You can only fix the systems that allow human errors to reach the customer.
