# Chapter 11: Capacity Planning & Auto-Scaling

In Volume 4, we learned how to dynamically provision cloud servers using Terraform. But *when* should you provision them?

If you provision 100 servers and your application only uses 10, you are wasting thousands of dollars a month in cloud costs. If you provision 10 servers and 100,000 users log in, your application crashes under the load.

In the past, organizations bought physical hardware based on 5-year projections. Today, Senior Engineers design systems to scale elastically, expanding and shrinking automatically in response to real-time traffic. This is the domain of **Capacity Planning and Auto-Scaling**.

## The Two Dimensions of Scaling

When a server runs out of capacity (CPU, Memory, or Network), there are only two ways to fix it:

### 1. Vertical Scaling (Scaling Up)
Vertical scaling means making the existing server bigger. If your 4-core database server is maxed out, you shut it down and resize it to a 16-core server.
* **Pros:** Extremely easy. Requires no changes to application architecture. Perfect for monolithic relational databases (like MySQL or Postgres) that do not natively distribute data across multiple servers.
* **Cons:** Hard limits. You can only buy a server so big. Furthermore, vertical scaling usually requires downtime to upgrade the hardware.

### 2. Horizontal Scaling (Scaling Out)
Horizontal scaling means adding *more* servers. Instead of one 16-core server, you deploy sixteen 1-core servers and put a Load Balancer in front of them.
* **Pros:** Infinite scalability. Highly resilient (if one server dies, the other 15 keep working). No downtime required to add or remove servers.
* **Cons:** Architecturally complex. The application must be "stateless" (it cannot store user sessions locally, because the next request might hit a different server). Databases must be designed for replication and sharding (like Cassandra or MongoDB).

## The Auto-Scaling Group (ASG)

In cloud environments (AWS, GCP, Azure) and container orchestrators (Kubernetes), horizontal scaling is managed by an Auto-Scaling Group (ASG).

An ASG is a logical grouping of identical servers. You define three parameters:
1. **Minimum Size:** (e.g., 3 servers). The ASG will *never* allow the pool to drop below 3. If a server crashes, the ASG automatically detects the failure and launches a replacement to maintain the minimum.
2. **Maximum Size:** (e.g., 20 servers). A hard limit to prevent runaway cloud bills if a bug causes the scaling metric to spike artificially.
3. **Desired Capacity:** The current number of servers running. 

## The Scaling Metric

How does the ASG know when to change the Desired Capacity? It relies on a scaling metric and an alarm.

The most common scaling metric is **Average CPU Utilization**. 
You configure a rule: *If the average CPU of all servers in the ASG exceeds 70% for 5 minutes, add 2 servers. If the average CPU drops below 30% for 15 minutes, remove 1 server.*

### The Danger of CPU Scaling
Scaling based solely on CPU is dangerous. If your application is I/O bound (waiting on the database), the CPU might sit at 10% while requests pile up in the socket queue. The server will crash, but the ASG will never scale up because the CPU threshold (70%) was never reached.

For complex microservices, it is often better to scale based on **Request Queue Length** (how many users are waiting) or **Active Concurrent Connections**.

---

## Scenario-Based Troubleshooting

### Scenario A: The Flapping Auto-Scaler

> [!IMPORTANT]  
> **Incident Report: The Flapping Auto-Scaler**  
> **Reporter:** Cloud Billing Alert  
> **SOP execution:**
> 
> 1. **14:00 PM — Incident Receipt:** AWS billing alerts the SRE team that the EC2 auto-scaling group for the frontend web application has executed 400 scaling events in the last two hours.
> 
> 2. **14:05 PM — Triage & Containment:** The engineer checks the AWS console. The ASG is constantly spinning up 5 new servers, waiting 2 minutes, and then immediately terminating them. This is called "flapping."
> 
> 3. **14:10 PM — Investigation:** The engineer examines the scaling policies. 
>    * Scale Up Rule: Add 5 servers if Average CPU > 60%.
>    * Scale Down Rule: Remove 5 servers if Average CPU < 55%.
>    
>    During the marketing push, the base traffic naturally drove the CPU to 62%. The ASG added 5 servers. The new servers diluted the traffic, dropping the average CPU to 50%. The Scale Down rule instantly triggered, removing the 5 servers. The CPU immediately shot back up to 62%, triggering the Scale Up rule again in an endless, expensive loop.
> 
> 4. **14:15 PM — Resolution:** The engineer edits the scaling policy to introduce a wider "dead zone" (hysteresis) and a cooldown period.
>    * Scale Up Rule: Add 2 servers if Average CPU > 75%.
>    * Scale Down Rule: Remove 1 server if Average CPU < 40%.
>    * Cooldown: Wait 5 minutes after a scaling event before evaluating metrics again.
> 
> 5. **14:20 PM — Verification:** The flapping stops entirely. The ASG stabilizes at a desired capacity of 8 servers with an average CPU of 65%.
> 
> 6. **Post-Mortem:** Discuss the math behind proportional scaling policies.
> 
> 7. **Documentation:** Add a hard requirement to the Terraform CI/CD pipeline: All ASG Scale Down thresholds must be at least 30% lower than the Scale Up thresholds.

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Setting the "Scale Down" cooldown too aggressively. If you scale up to handle a massive traffic spike, you want those servers online instantly. But when the spike ends, you should wait 15 to 30 minutes before terminating the extra servers. Traffic often comes in secondary waves. If you scale down immediately, you'll be caught off-guard by the second wave. Scale up fast, scale down slow.

> [!TIP] Pro-Tip
> Kubernetes has two auto-scalers: The HPA (Horizontal Pod Autoscaler) scales the *containers* inside the cluster. The Cluster Autoscaler scales the *physical EC2 instances* underneath the cluster. If you configure the HPA to spin up 100 new pods, but forget to configure the Cluster Autoscaler, those pods will sit in a `Pending` state forever because there are no physical servers to host them.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 11 Practice Guide](../practice-files/V5-C11-practice.md) to mathematically calculate the required minimum ASG size for an application with a known TPS (Transactions Per Second) and latency target!

## Interview Questions

### Question 1: What is the difference between Horizontal Scaling and Vertical Scaling?
* **Target Answer**: "Vertical scaling (scaling up) involves increasing the physical resources (CPU, RAM) of an existing server. It is simple but requires downtime and has a hard hardware limit. Horizontal scaling (scaling out) involves adding more identical servers behind a load balancer. It provides infinite, dynamic scalability and high availability, but requires a stateless application architecture."

### Question 2: Why is "flapping" dangerous in an Auto-Scaling Group, and how do you prevent it?
* **Target Answer**: "Flapping occurs when an ASG rapidly provisions and terminates servers in an endless loop because the scale-up and scale-down thresholds are too close together. It degrades performance and generates massive cloud bills. You prevent it by creating a wide hysteresis (dead zone) between the thresholds—for example, scaling up at 80% CPU but not scaling down until it hits 40%—and by implementing a Cooldown period (e.g., 5 minutes) after every scaling event to let metrics stabilize."

### Question 3: Why might CPU utilization be a terrible metric for auto-scaling a Node.js microservice?
* **Target Answer**: "Node.js is single-threaded and heavily relies on asynchronous I/O. If the microservice is waiting on a slow backend database to return queries, the CPU will sit idle (at 5% utilization) while thousands of incoming user requests pile up in the memory queue. The server will crash from memory exhaustion or connection limits long before the CPU reaches the 70% threshold required to trigger the auto-scaler. Scaling on concurrent requests or socket queue length is much safer."



**Chapter Transition**
> We have planned capacity, but a sudden viral traffic spike will overwhelm it regardless. We must aggressively drop traffic with Rate Limiting.

---

## Navigation

⬅ Previous:
[Chapter 10: Performance Tuning the Kernel Parameters (sysctl)](V5-C10-kernel-parameters-sysctl.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 12: Rate Limiting and Load Shedding](V5-C12-rate-limiting.md)
