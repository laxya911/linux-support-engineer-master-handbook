# Practice Guide: Chapter 25 (Volume 3)

## Objective
To conceptually analyze a traditional single-node deployment and identify the Single Points of Failure (SPOFs) that Orchestration solves.

## Assignment 1: The Architectural Audit
Imagine you are hired as a consultant for a mid-sized e-commerce company. They show you their current production architecture:

**The Architecture:**
* They rent one massive physical server in a datacenter (256GB RAM, 64 Cores).
* They use Docker Compose to run:
  * 1 NGINX Load Balancer Container
  * 10 Node.js API Containers
  * 1 PostgreSQL Database Container (using a Bind Mount to `/var/lib/pg_data`)

## Assignment 2: Identifying the Risks
On a blank piece of paper (or in a text file), write down what happens to the e-commerce website in the following scenarios:

1. **Scenario 1:** The Node.js developer writes bad code that creates an infinite loop. The 10 Node.js containers consume 100% of the server's CPU. 
   *(Analysis: Because they are all on the same server, the CPU maxes out. The NGINX and PostgreSQL containers cannot get CPU cycles, and the entire server locks up. A SPOF!)*
2. **Scenario 2:** The motherboard on the physical server catches fire. 
   *(Analysis: All 12 containers die instantly. The bind-mounted data on the hard drive might be recoverable, but the website is completely offline until a new physical server is purchased and configured. A SPOF!)*

## Assignment 3: The Orchestration Solution
How would Kubernetes (Volume 4) solve Scenario 2?

1. Instead of one massive 256GB server, you would provision five 32GB servers and cluster them.
2. The Database would have its data stored on an external Network Attached Storage (NAS) device, not a local hard drive.
3. If Server #2 catches fire, Kubernetes instantly detects it. The 2 Node.js containers that were running on Server #2 are automatically spun up on Server #3 within seconds. The customer barely notices a hiccup!

## Success Criteria
You have successfully completed this practice if you can clearly explain why relying on a single, massive Docker Compose server is fundamentally dangerous for an enterprise business.

---

### Congratulations!
You have completed the final practice guide of **Volume 3: Enterprise Linux Services**. Take a well-deserved rest. You are now prepared to tackle the complexities of true Enterprise Infrastructure!
