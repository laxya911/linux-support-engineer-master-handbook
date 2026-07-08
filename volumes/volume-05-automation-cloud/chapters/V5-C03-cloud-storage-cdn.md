---
volume: 5
chapter: 3
part: 1
id: V5-C03
title: Cloud Storage & CDN Optimization
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Intermediate
estimated_time: 1.5 Hours
reading_time: 25 Minutes
labs: 1
interview_questions: 3
prerequisites: None
last_updated: 2026-07
status: In Progress
---

# Chapter 3 — Cloud Storage & CDN Optimization

* **Difficulty:** Intermediate
* **Estimated Time:** 1.5 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

By the end of this chapter, you will be able to:
* Differentiate between Block Storage (EBS) and Object Storage (S3).
* Utilize AWS S3 Storage Classes to dramatically reduce costs.
* Define a Content Delivery Network (CDN) like CloudFront.
* Explain the concept of Cache Invalidation.

## Visual Architecture: The Edge Cache

Serving large static files (like 4K videos or high-res images) directly from your primary Web Server in Virginia is expensive and slow. A customer in Sydney, Australia will experience terrible buffering as the video crosses the Pacific Ocean.
**CDNs (Content Delivery Networks)** solve this by placing "Edge Locations" in hundreds of cities worldwide. When the Sydney customer requests the video, the CDN checks if it has a cached copy in Sydney. If it does, the video loads instantly, and your Virginia server never even knows the request happened!

```mermaid
flowchart TD
    A[Customer in Sydney] -->|Requests Video| B{CDN Edge Node \n (Sydney, AU)}
    
    B -->|Cache HIT| A
    B -.->|Cache MISS| C[(S3 Origin Bucket \n Virginia, USA)]
    
    C -.->|Returns Video to Cache| B
    
    style A fill:#0984e3,stroke:#74b9ff,color:#fff
    style B fill:#8e44ad,stroke:#9b59b6,color:#fff
    style C fill:#f39c12,stroke:#f1c40f,color:#000
```

## Theory & Concepts

### 1. Object Storage vs Block Storage
* **Block Storage (AWS EBS):** Functions like a physical hard drive plugged into a server. It is extremely fast, allows you to edit a single byte of a file, but can only be attached to one server at a time.
* **Object Storage (AWS S3):** A flat, infinite storage pool accessed via REST APIs (HTTP). You cannot edit a single byte of a file; you must overwrite the entire object. However, it is infinitely scalable and can be accessed by thousands of servers simultaneously.

### 2. S3 Storage Classes & Lifecycle Policies
If you store 100 Terabytes of compliance logs that you never look at, you should not pay top dollar for them. S3 offers storage tiers:
* **S3 Standard:** Expensive, millisecond retrieval. Used for active website images.
* **S3 Standard-IA (Infrequent Access):** Cheaper storage, but you pay a penalty fee every time you access the file. Used for monthly backups.
* **S3 Glacier Deep Archive:** Extremely cheap storage ($1 per Terabyte/month), but it takes 12 hours to retrieve the file. Used for legal compliance logs.
You use **Lifecycle Policies** to automate the transition. (e.g., "After 30 days, move Standard files to IA. After 365 days, move to Glacier.")

### 3. CDN Caching & Time To Live (TTL)
When a CDN fetches a file from S3, it holds it in the Edge Cache. The **TTL (Time to Live)** determines how long it holds it. If TTL is 24 hours, the CDN will serve the cached copy to all users for 24 hours without checking S3. 

## Scenario-Based Troubleshooting

### Scenario A: The Stubborn Logo Update
**The Incident:** The marketing team launches a massive rebranding campaign. They replace the old company logo (`logo.png`) in the AWS S3 bucket with the new logo. They announce the rebrand on Twitter. Five minutes later, angry executives call the Support Engineer: "The website is still showing the old logo! We replaced the file in S3, but it didn't update on the live site!"

**The Investigation & Fix:**
1. The Support Engineer checks the S3 bucket. The new logo is indeed there.
2. The engineer opens the website in their browser. The old logo appears.
3. The engineer uses `curl -I https://www.company.com/logo.png`. 
4. **The Observation:** The HTTP headers returned by the server include `X-Cache: Hit from cloudfront` and `Cache-Control: max-age=86400`. 
5. **The Analysis:** The website is fronted by AWS CloudFront (CDN). The TTL (max-age) for images is set to 86400 seconds (24 hours). Even though the marketing team changed the file in the S3 "Origin," the CloudFront Edge nodes around the world still have the old logo cached in memory, and they will stubbornly serve the old logo for another 23 hours!
6. **The Resolution:** The engineer logs into the AWS Console and issues a **CloudFront Cache Invalidation** for the path `/logo.png`. 
7. The invalidation forcefully purges the old logo from all Edge nodes globally. 
8. The next time a user visits the site, CloudFront registers a "Cache Miss," reaches back to the S3 bucket, fetches the new logo, and caches it. The executives are happy.

> [!CAUTION]  
> **Best Practice: Cache Busting via Filenames**  
> Running manual Cache Invalidations across a global CDN is slow (it can take 5-10 minutes) and AWS charges you money for it! Modern frontend frameworks solve this using "Cache Busting." Instead of overwriting `logo.png`, the build system creates `logo-v2.png` and updates the HTML file. Because the URL changed, the CDN instantly recognizes it as a new file, completely bypassing the need for manual invalidations.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 3 Practice Guide](../practice-files/V5-C03-practice.md) to conceptually design an S3 Lifecycle Policy using Terraform!

## Interview Questions

### Question 1: What is the architectural difference between Block Storage (EBS) and Object Storage (S3)?
* **Target Answer**: "Block storage (EBS) operates at the operating system level, appearing as a raw, mountable hard drive that supports high-speed, random read/write operations on individual blocks of a file. Object storage (S3) is a flat namespace accessed via HTTP APIs. Objects are immutable—you cannot edit a single byte of an S3 object; you must replace the entire file. S3 is designed for infinite scalability and highly concurrent access across thousands of distributed systems."

### Question 2: How does a CDN improve latency for global users and reduce costs for the business?
* **Target Answer**: "A CDN distributes cached copies of static assets (images, videos, CSS) to Edge Locations physically located near the end users. When a user in Tokyo requests an image, they download it from the Tokyo Edge Node rather than the primary server in New York, massively reducing latency. This reduces costs because the primary web server (or S3 bucket) only has to serve the file once to the CDN, rather than serving it a million times to a million individual users, saving massive amounts of compute and egress bandwidth."

### Question 3: A developer updates a Javascript file on the origin server, but users are reporting they are not seeing the new feature. Explain the likely cause and two ways to fix it.
* **Target Answer**: "The cause is that the CDN has cached the old Javascript file based on its Time to Live (TTL) and is serving the stale cache to the users. The first way to fix it is to issue a manual Cache Invalidation on the CDN for that specific file path, forcing it to fetch the new version. The second, better way is to use 'Cache Busting' (e.g., renaming the file to `script-v2.js`), which alters the URL and inherently forces the CDN to treat it as a brand-new asset."

## Chapter Summary

Storage is no longer just "buying a bigger hard drive." By combining the tiered, infinite capacity of S3 with the global distribution of a CDN, you can serve petabytes of data to millions of global users with near-zero latency, all while optimizing your monthly cloud bill.

## Completion Checklist

- [ ] I can differentiate between S3 and EBS.
- [ ] I understand the purpose of S3 Storage Classes (Standard, IA, Glacier).
- [ ] I can explain what a Cache Invalidation does.

---

## Navigation

⬅ Previous:
[Chapter 2 – Auto-Scaling & Load Distribution](V5-C02-auto-scaling.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 4 – Hybrid Cloud Connectivity](V5-C04-hybrid-connectivity.md)
