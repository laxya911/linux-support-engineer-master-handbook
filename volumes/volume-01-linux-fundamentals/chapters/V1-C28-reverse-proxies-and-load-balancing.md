---
volume: 1
chapter: 28
part: 1
id: V1-C28
title: Reverse Proxies & Load Balancing
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Advanced
estimated_time: 2 Hours
reading_time: 45 Minutes
labs: 1
interview_questions: 3
prerequisites: Chapter 27
last_updated: 2026-07
status: In Progress
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 28 — Reverse Proxies & Load Balancing

* **Difficulty:** Advanced
* **Estimated Time:** 2 Hours
* **Hands-on Labs:** 1
* **Interview Questions:** 3

## Learning Objectives

Have you ever wondered how Linux handles Reverse Proxies & Load Balancing? In this chapter, we dive deep into the mechanics, exploring the tools and strategies that separate a junior admin from a true Linux Support Engineer.

By the end of this chapter, you will be able to:
* Explain the difference between a Web Server and a Reverse Proxy.
* Understand why developers use `proxy_pass` to hide backend applications.
* Explain how a Load Balancer distributes traffic.
* Troubleshoot the "502 Bad Gateway" error.
* Troubleshoot "Sticky Session" logout loops.

## Visual Architecture: The Load Balancer

A single web server can only handle so much traffic. When a website gets popular, you must split the traffic across multiple servers. A Load Balancer sits at the front door and acts as a traffic cop.

```mermaid
flowchart TD
    A["Customer 1"] -->|"Visits shop.com"| B{"Nginx Load Balancer"}
    C["Customer 2"] -->|"Visits shop.com"| B
    
    B -->|"Routes Customer 1"| D["Backend Server A (Node.js)"]
    B -->|"Routes Customer 2"| E["Backend Server B (Node.js)"]
    
    style A fill:#0984e3,stroke:#74b9ff,color:#fff
    style C fill:#f39c12,stroke:#f1c40f,color:#000
    style B fill:#00b894,stroke:#55efc4,color:#000
```

## Theory & Concepts

### 1. What is a Reverse Proxy?
A web server (like we learned in Chapter 27) serves files directly from the hard drive (`/var/www/html`). 
A **Reverse Proxy** does *not* serve files. Instead, it takes the customer's request, turns around, hands the request to a completely different application running in the background, waits for the answer, and passes the answer back to the customer. 
Nginx is the undisputed king of Reverse Proxies.

### 2. Why hide the Backend? (The `proxy_pass`)
Most modern applications are built in Node.js, Python, or Ruby. These applications are terrible at handling raw internet traffic and SSL certificates.
Instead, developers run their Node.js app on a hidden internal port (e.g., `localhost:3000`). They use Nginx on Port 80 to act as the armored front door. Nginx uses the `proxy_pass http://localhost:3000;` directive to safely hand the traffic backward.

### 3. What is a Load Balancer?
If you add multiple backend servers to a Reverse Proxy configuration, it becomes a Load Balancer. Nginx will automatically send Request 1 to Server A, Request 2 to Server B, Request 3 to Server A, and so on (a "Round Robin" algorithm).

## Scenario-Based Troubleshooting

### Scenario A: The "502 Bad Gateway" Error
**The Incident:** A customer visits their web application and the browser shows a giant, unstyled `502 Bad Gateway (Nginx)` error.

**The Investigation & Fix:**
1. The engineer logs in. They know a 502 error means the Nginx front door is working perfectly, but when Nginx turned around to hand the traffic to the backend application, the backend application wasn't there.
2. The engineer runs `ss -tulpn | grep 3000` to see if the Node.js app is listening on its internal port. The output is empty.
3. The engineer runs `systemctl status node-app`. The output shows the application crashed due to a memory error 10 minutes ago.
4. The engineer fixes the code error and runs `systemctl start node-app`.
5. Nginx immediately detects that the backend is alive again, and the 502 error vanishes.

### Scenario B: The Sticky Session Logout Loop
**The Incident:** A customer upgrades to a 2-server Load Balancer. Immediately, their users complain that every time they log in to the website, they click a link and are instantly logged out again.

**The Investigation & Fix:**
1. The engineer understands how Load Balancing works: 
   * **Click 1:** User logs in. Load Balancer sends them to Server A. Server A saves their session in memory.
   * **Click 2:** User clicks "My Account". Load Balancer sends them to Server B. Server B has no idea who this user is, so it logs them out.
2. The engineer opens the Nginx Load Balancer configuration file: `nano /etc/nginx/nginx.conf`.
3. They add the `ip_hash;` directive to the backend server pool.
4. They run `nginx -t` to check syntax, then `systemctl restart nginx`.
5. **Result:** The `ip_hash` command forces "Sticky Sessions". Nginx calculates the user's IP address and guarantees that Customer 1 will *always* be sent to Server A. The logout loop is fixed.

## Hands-on Lab

> [!CAUTION]
> **Practice Assignment Available**
> Before moving on, complete the exercises in the [Chapter 28 Practice Guide](../practice-files/V1-C28-practice.md). You will practice identifying whether a backend application is actually running before blaming the proxy.

## Interview Questions

### Question 1: A customer reports a "502 Bad Gateway" error. Is the Nginx web server down?
* **Target Answer**: "No, Nginx is not down. A 502 Bad Gateway error proves that Nginx is actually running and accepting connections. However, it indicates that Nginx is acting as a reverse proxy, and the backend application it is trying to communicate with (such as a Node.js or Python app) is either offline, crashed, or unreachable."

### Question 2: In Nginx, what does the `proxy_pass` directive do?
* **Target Answer**: "The `proxy_pass` directive tells Nginx to act as a reverse proxy. Instead of serving files from the local filesystem, Nginx intercepts the incoming HTTP request and forwards it to a specified backend URL or local port (like `http://127.0.0.1:3000`), waits for the response, and then passes that response back to the client."

### Question 3: A website behind a round-robin load balancer keeps randomly logging users out as they browse the site. What is the cause and the solution?
* **Target Answer**: "The cause is that session data is being stored locally on the backend servers. When the load balancer routes the user's next request to a different backend server, that server doesn't recognize the session. The immediate solution is to configure 'Sticky Sessions' (such as using `ip_hash` in Nginx) to ensure a user is consistently routed to the same backend server."

## Chapter Summary

As a Support Engineer, the most valuable lesson in this chapter is understanding the 502 error. Whenever you see a 502, do not restart Nginx. Nginx is doing its job by reporting the failure. Focus entirely on finding out why the hidden backend application crashed.

## Completion Checklist

- [ ] I understand the difference between a Web Server and a Reverse Proxy.
- [ ] I know that a 502 error means the backend is down, not Nginx.
- [ ] I understand why Sticky Sessions (`ip_hash`) prevent logout loops.

---

## Navigation

⬅ Previous:
[Chapter 27 – Introduction to Web Servers](V1-C27-introduction-to-web-servers.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 29 – Database Fundamentals](V1-C29-database-fundamentals.md)
