# Practice Guide: Chapter 16 (Volume 4)

## Objective
To conceptually design a Troubleshooting Matrix for a complex, multi-tier web application failure, utilizing the "Divide and Conquer" methodology.

## Assignment 1: The Architecture
Imagine the following architecture:

1. **User Browser** -> 2. **Cloudflare CDN** -> 3. **AWS Application Load Balancer (ALB)** -> 4. **NGINX Web Server** -> 5. **PostgreSQL Database**

## Assignment 2: The Incident
The alert fires: `URGENT: All customers receiving a 502 Bad Gateway when trying to load the website.`

## Assignment 3: Creating the Matrix
Instead of guessing, we will create a matrix of tests to bisect the architecture. We start by cutting the architecture in half.

**Test 1: The Mid-Point Cut**
* **Action:** You bypass Cloudflare and the User Browser. You SSH into a bastion host in AWS and use `curl -I https://internal-alb.aws.com`.
* **If it SUCCEEDS:** The problem is *upstream* (Cloudflare is misconfigured, or the User's DNS is poisoned). You can completely ignore the Web Servers and Database.
* **If it FAILS (Returns 502):** The problem is *downstream*. The Load Balancer, Web Server, or Database is broken.

**Test 2: The Downstream Cut**
*(Assuming Test 1 Failed)*
* **Action:** You bypass the Load Balancer. You SSH directly into the NGINX Web Server and run `curl -I http://localhost`.
* **If it SUCCEEDS:** The web server is fine! The Load Balancer is the culprit (perhaps its health checks are failing or its SSL certificate expired).
* **If it FAILS:** The Web Server or Database is broken.

**Test 3: The Final Cut**
*(Assuming Test 2 Failed)*
* **Action:** You check the NGINX logs (`/var/log/nginx/error.log`). 
* **If the log says:** `Connection refused to 10.0.1.55:5432` (The Postgres Port).
* **Conclusion:** The Web Server is fine, but it cannot talk to the Database. The Database is the Root Cause.

## Success Criteria
You have successfully completed this practice if you understand how we took a massive 5-tier architecture and found the exact point of failure using only 3 logical `curl` commands, rather than rebooting all 5 systems and praying it fixed the issue.
