# Practice Guide: Chapter 11 (Volume 5)

## Objective
To understand the mathematics behind Site Reliability Engineering by calculating SLIs and understanding the reality of "The Nines" of uptime.

## Assignment 1: Calculating the SLI
Your company processes 5,000,000 HTTP API requests every day. 

1. **The Scenario:** Today, your backend database experienced a brief 2-minute outage. During that outage, the API returned `HTTP 500 Internal Server Error` to 12,500 requests. 

2. **The Calculation:** What is your exact SLI (Service Level Indicator) for today, expressed as a percentage of successful requests?
   * *Total Requests:* 5,000,000
   * *Failed Requests:* 12,500
   * *Successful Requests:* 4,987,500
   * *Math:* `(4,987,500 / 5,000,000) * 100` = **99.75%**

3. **The Result:** Your SLI for the day is 99.75%.

## Assignment 2: The Reality of "The Nines"
When a CEO demands "100% Uptime," an SRE laughs. 100% is statistically impossible in distributed systems. Instead, SREs talk in "Nines" (e.g., 99.9% is "Three Nines").

Let's calculate exactly how much downtime you are legally allowed to have per month (30 days) based on different SLAs.

1. **Two Nines (99.0% SLA)**
   * Total minutes in a month: 43,200
   * Allowed downtime: 1.0%
   * Calculation: `43,200 * 0.01` = **432 Minutes (7.2 Hours) per month.**
   * *Analysis:* Very easy to achieve. You can have a massive 7-hour outage every single month and still meet this SLA.

2. **Three Nines (99.9% SLA)**
   * Allowed downtime: 0.1%
   * Calculation: `43,200 * 0.001` = **43.2 Minutes per month.**
   * *Analysis:* The industry standard. If your database crashes, you have less than 45 minutes to detect the alert, log in, diagnose the issue, and restart the database before you start losing money.

3. **Four Nines (99.99% SLA)**
   * Allowed downtime: 0.01%
   * Calculation: `43,200 * 0.0001` = **4.32 Minutes per month.**
   * *Analysis:* Impossible to achieve with human intervention. If a server dies, the auto-scaling and failover mechanisms must detect it and replace it completely automatically in under 4 minutes.

4. **Five Nines (99.999% SLA)**
   * Allowed downtime: 0.001%
   * Calculation: `43,200 * 0.00001` = **26 Seconds per month!**
   * *Analysis:* Only required for hyper-critical systems (like pacemakers or aviation software). Achieving this requires massive global redundancy, active-active multi-region databases, and millions of dollars in engineering costs.

## Success Criteria
You have successfully completed this practice if you can logically explain to a Product Manager why demanding "Five Nines" of reliability for an internal HR blog is a massive waste of engineering resources!
