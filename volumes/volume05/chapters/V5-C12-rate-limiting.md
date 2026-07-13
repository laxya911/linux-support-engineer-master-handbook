# Chapter 12: Rate Limiting and Load Shedding

In Chapter 11, we learned how to Auto-Scale our infrastructure to handle traffic spikes. 

But what happens when the traffic spike is instantaneous? If 100,000 users log in within one second (e.g., during a Super Bowl ad or a sneaker drop), an Auto-Scaling Group is useless. It takes 3 to 5 minutes to boot a new EC2 instance, install the application, and attach it to the load balancer. By the time the new servers are online, the existing servers have already crashed under the thundering herd.

Senior Engineers know that you cannot scale your way out of a catastrophic spike. You must gracefully reject traffic *before* it destroys your system.

## The Thundering Herd

A system is like a restaurant. If the restaurant has 100 seats, it can comfortably serve 100 customers. If 150 customers show up, the waiters are overwhelmed, the kitchen falls behind, and *nobody* gets their food.

The goal of reliability engineering is to ensure that even if 150 customers show up, the 100 customers inside still receive perfect service, while the 50 extra customers are told to wait outside. 

If you do not protect your system, it will attempt to serve all 150 customers simultaneously, exhaust its memory queues, and crash, serving 0 customers.

We protect the system using **Rate Limiting** and **Load Shedding**.

## Rate Limiting (Protecting against Abuse)

Rate limiting is enforced at the edge of the network (e.g., at the NGINX Reverse Proxy, the API Gateway, or the WAF). It tracks the identity of the incoming user (usually via IP address or API token) and sets a hard limit on how many requests they can make.

* **Example:** "API Token X is allowed 100 requests per minute. If they make 101 requests, return an HTTP `429 Too Many Requests` error."
* **The Goal:** Prevent a single bad actor (or a buggy client script) from monopolizing the server's resources.

### Algorithms
* **Token Bucket:** The most common algorithm. Imagine a bucket that holds 100 tokens. Every second, 10 new tokens are added. Every request removes 1 token. If the bucket is empty, the request is rejected. This allows for short bursts of traffic while maintaining a steady average rate.

## Load Shedding (Protecting against Death)

Rate Limiting protects against *individual* abuse. But what if 10,000 completely legitimate, unique users all log in at exactly the same time? No individual user is violating their rate limit, but the aggregate traffic will still crash the database.

This is where **Load Shedding** comes in.

Load Shedding is enforced deep inside the application or proxy. It does not care *who* is making the request. It only cares about the health of the server. 

* **Example:** "If the internal queue of the application reaches 500 pending requests, instantly reject all new incoming requests with an HTTP `503 Service Unavailable` error, regardless of who is asking."
* **The Goal:** Protect the core components (like the database) from catastrophic failure, ensuring the system stays online to process the requests it has already accepted.

### Graceful Degradation
Load Shedding is often paired with Graceful Degradation. If the system is overwhelmed, instead of returning an error, you return a "dumb" response.
* If the recommendation engine is overloaded, don't crash the homepage. Just shed the recommendation traffic and show the user a static list of "Top 10 Global Movies."

---

## Scenario-Based Troubleshooting

### Scenario A: The Retry Storm

> [!IMPORTANT]  
> **Incident Report: The Retry Storm**  
> **Reporter:** Database Administration Team  
> **SOP execution:**
> 
> 1. **20:00 PM — Incident Receipt:** The primary PostgreSQL database suddenly hits 100% CPU and 100% Disk I/O. API response times spike from 200ms to 15 seconds.
> 
> 2. **20:05 PM — Triage & Containment:** The engineer checks the application logs. The frontend mobile application is experiencing a network glitch. When the mobile app fails to connect to the backend API, the developer's code immediately attempts to reconnect in a tight `while` loop with no delay.
> 
> 3. **20:10 PM — Investigation:** Because the API was slightly slow, 50,000 mobile clients dropped their connections and immediately retried. Now, the backend is receiving 500,000 requests per second. The Postgres database is paralyzed trying to process the massive backlog of queries. The system is in a "Retry Storm" (also known as a cascading failure).
> 
> 4. **20:15 PM — Resolution:** The engineer cannot fix the mobile app instantly (it requires an App Store update). To save the database, they implement an emergency NGINX configuration block.
>    They configure `limit_req_zone` in NGINX, restricting each IP address to 5 requests per second. 
> 
> 5. **20:20 PM — Verification:** NGINX instantly begins shedding the retry storm, returning HTTP `429` errors to the aggressive mobile clients. The database traffic normalizes. CPU drops to 30%. The API recovers for legitimate users.
> 
> 6. **Post-Mortem:** Discuss the lack of backoff logic in the mobile client.
> 
> 7. **Documentation:** Mandate that all frontend applications implement "Exponential Backoff with Jitter." If a request fails, the client must wait 1 second, then 2 seconds, then 4 seconds, adding a random number of milliseconds (jitter) to prevent all clients from retrying at the exact same millisecond.

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Implementing Load Shedding inside the application code *after* the application has parsed the JSON payload. Parsing JSON requires CPU cycles. If you accept the request, parse the 5MB JSON payload, and *then* decide the server is too busy and return a 503, you have already wasted precious CPU cycles. Load Shedding must happen at the absolute earliest point possible—ideally in the Reverse Proxy (NGINX/HAProxy) before the application code even sees the request.

> [!TIP] Pro-Tip
> When configuring Rate Limiting in NGINX, use the `burst` and `nodelay` parameters. Setting `limit_req zone=myzone burst=20 nodelay;` allows a legitimate user to suddenly load a webpage containing 20 images simultaneously without being incorrectly rate-limited for a sudden burst of parallel requests.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 12 Practice Guide](../practice-files/V5-C12-practice.md) to configure NGINX rate limiting and simulate a DDoS attack using the `ab` (Apache Bench) tool!

## Interview Questions

### Question 1: What is the fundamental difference between Rate Limiting and Load Shedding?
* **Target Answer**: "Rate limiting protects against individual bad actors. It restricts traffic based on the identity of the client (IP or Token) to enforce quotas. Load Shedding protects the server from aggregate death. It ignores identity and simply drops all incoming traffic when the server's internal queues or CPU hit a critical threshold, ensuring the server survives the spike."

### Question 2: Why is 'Exponential Backoff with Jitter' critical for building resilient client applications?
* **Target Answer**: "If a server blips offline for 5 seconds, all connected clients will disconnect. If they all attempt to reconnect immediately, they will create a massive 'Retry Storm' that will instantly crash the recovering server. Exponential backoff forces clients to wait progressively longer between retries (1s, 2s, 4s). Adding 'Jitter' (randomized milliseconds) ensures that the clients don't accidentally synchronize their retries and hit the server simultaneously in waves."

### Question 3: How does the Token Bucket algorithm allow for traffic bursts?
* **Target Answer**: "The token bucket fills at a steady rate (e.g., 10 tokens per second), up to a maximum capacity (e.g., 100 tokens). If a user hasn't made a request recently, their bucket is full. This allows them to instantly fire off 100 rapid requests (a burst) before the bucket empties. Once empty, they are restricted to the steady refill rate of 10 requests per second. This perfectly models realistic human web browsing."



**Chapter Transition**
> Traffic is shaped, but managing rate limits across 500 microservices is impossible. We need a dedicated Service Mesh.

---

## Navigation

⬅ Previous:
[Chapter 11: Capacity Planning & Auto-Scaling](V5-C11-capacity-planning.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 13: Service Mesh and Circuit Breakers](V5-C13-service-mesh.md)
