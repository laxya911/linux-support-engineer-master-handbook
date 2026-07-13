# Chapter 14: Distributed Consensus (Raft & Paxos)

If you have one database server, finding the truth is easy. You ask the database: "Did user Alice transfer $50 to Bob?" and it says "Yes."

If you have 5 database servers scattered across the globe for high availability, finding the truth becomes the hardest problem in computer science. What if Server A says "Yes," but Server B says "No," and Server C is disconnected due to a cut fiber optic cable? Who is right? If the servers cannot agree on a single source of truth, Bob gets the $50 and Alice keeps her $50, destroying the integrity of the bank.

To prevent this, distributed systems rely on **Consensus Algorithms**.

## The Split-Brain Problem

We briefly touched on Split-Brain in earlier volumes. A Split-Brain occurs when a network partition severs communication between nodes in a cluster. The cluster splits into two isolated halves, and both halves elect a primary master node. 

Both masters start accepting writes independently. When the network reconnects, the data is hopelessly divergent and cannot be merged safely.

### The Quorum Solution
To prevent Split-Brain, distributed systems use a concept called **Quorum**. A Quorum dictates that a cluster can only function if a strict majority (more than 50%) of its nodes are healthy and can communicate with each other.

If a cluster has 5 nodes, the Quorum size is 3. If the network splits the cluster into a group of 2 and a group of 3, the group of 3 has Quorum and continues to operate. The group of 2 realizes it does not have Quorum and completely shuts itself down (or goes into Read-Only mode) to protect data integrity.

This is why distributed systems *always* require an odd number of nodes (3, 5, or 7).

## Consensus Algorithms: Paxos and Raft

Quorum dictates *how many* nodes must agree. Consensus Algorithms dictate *how* they agree. 

When a client wants to write data to a distributed database (like etcd, Consul, or CockroachDB), the cluster must use an algorithm to ensure that the data is safely replicated and ordered.

### 1. Paxos
Invented by Leslie Lamport in 1989, Paxos was the first mathematically proven consensus algorithm. It is notoriously complex and difficult to understand. For two decades, it was the only reliable way to achieve consensus, utilized heavily by Google in their internal systems (like Spanner and Chubby).

### 2. Raft
Raft was created in 2013 specifically to be understandable. It achieves the exact same mathematical safety as Paxos but structures the logic into three distinct, easy-to-manage subproblems. It is the algorithm that powers `etcd` (the brain of Kubernetes).

**The Raft Process:**
1. **Leader Election:** The nodes start as "Followers." If a follower doesn't hear from a Leader, it becomes a "Candidate" and requests votes. The nodes vote, and the Candidate with the majority of votes becomes the Leader. 
2. **Log Replication:** All clients must send their write requests to the Leader. The Leader appends the request to its log and forwards it to the Followers.
3. **Commitment:** The Leader does *not* acknowledge the write to the client yet. It waits until a majority of the Followers confirm they have written the log. Only then does the Leader "Commit" the data and return success to the client.

If the Leader crashes, the Followers instantly detect the silence and hold a new election to appoint a new Leader.

---

## Scenario-Based Troubleshooting

### Scenario A: The etcd Quorum Loss

> [!IMPORTANT]  
> **Incident Report: The Stalled Kubernetes Cluster**  
> **Reporter:** DevOps Engineering  
> **SOP execution:**
> 
> 1. **09:00 AM — Incident Receipt:** Engineers report they cannot deploy any new pods or modify existing configurations in the production Kubernetes cluster. The `kubectl apply` command just hangs indefinitely.
> 
> 2. **09:05 AM — Triage & Containment:** The engineer checks the worker nodes. Existing applications are running perfectly fine and serving customer traffic. However, the Control Plane is completely unresponsive to new changes.
> 
> 3. **09:10 AM — Investigation:** The engineer logs into the master nodes to check `etcd` (the Raft-based database that stores all Kubernetes state). 
>    The cluster was architected with 3 `etcd` nodes.
>    The engineer runs `etcdctl endpoint status`. 
>    * Node 1: Unreachable.
>    * Node 2: Unreachable.
>    * Node 3: Healthy, but reports `Error: context deadline exceeded`.
>    
>    The engineer checks AWS EC2 and discovers that two of the three Control Plane instances were accidentally terminated by a rogue Terraform script.
> 
> 4. **09:15 AM — Root Cause:** With 2 out of 3 nodes dead, the cluster lost Quorum. The sole surviving node mathematically cannot form a majority (it needs 2 votes, but only has 1). To prevent Split-Brain, the Raft algorithm forced the surviving node to halt all write operations, protecting the integrity of the database at the cost of availability.
> 
> 5. **09:30 AM — Resolution:** Because Quorum was lost, the cluster cannot self-heal (it cannot elect a leader to process the addition of new nodes). The engineer must perform a manual Disaster Recovery from a backup snapshot. They restore the `etcd` snapshot to a fresh 3-node cluster and point the API servers to it.
> 
> 6. **10:00 AM — Verification:** `kubectl get nodes` responds instantly. Deployments resume.
> 
> 7. **Post-Mortem:** Discuss the vulnerability of running only 3 Control Plane nodes across 3 Availability Zones.
> 
> 8. **Documentation:** Upgrade the production architecture to 5 `etcd` nodes. A 5-node cluster has a Quorum of 3, meaning it can survive the loss of 2 simultaneous nodes without grinding to a halt.

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Building a 4-node cluster. An even number of nodes provides absolutely no additional fault tolerance over the odd number below it, but significantly increases latency. A 3-node cluster requires 2 votes for Quorum (survives 1 failure). A 4-node cluster requires 3 votes for Quorum (still only survives 1 failure). Never use even numbers for consensus clusters.

> [!TIP] Pro-Tip
> Because Raft requires the Leader to wait for network acknowledgments from the Followers before committing a write, disk I/O and network latency are the ultimate enemies of `etcd`. Always place `etcd` data directories on ultra-fast NVMe SSDs, and ensure the nodes have single-digit millisecond network latency between them. Do not spread a single `etcd` cluster across continents!

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 14 Practice Guide](../practice-files/V5-C14-practice.md) to manually break a 3-node `etcd` cluster and observe how Raft Leader Election behaves when Quorum is lost!

## Interview Questions

### Question 1: Why do distributed consensus systems (like Zookeeper or etcd) always require an odd number of nodes?
* **Target Answer**: "Distributed systems rely on strict majorities (Quorum) to prevent Split-Brain scenarios and ensure data consistency. If you have an even number of nodes (e.g., 4) and a network partition splits them precisely in half (2 and 2), neither side can form a strict majority, and the entire cluster halts. With an odd number (e.g., 5), a split guarantees that one side will always have the majority (3 vs 2), allowing the cluster to continue operating."

### Question 2: In the Raft algorithm, what happens if the current Leader node suddenly loses power?
* **Target Answer**: "The Follower nodes expect regular heartbeat messages from the Leader. When the Leader loses power, the heartbeats stop. After a randomized timeout period, the Followers recognize the silence, transition their state to 'Candidate', and request votes from the remaining healthy nodes. The node that receives the majority of votes is instantly promoted to the new Leader, and the cluster resumes normal operations."

### Question 3: Existing read queries are succeeding, but all write queries to your distributed database are failing. What is the most likely cause?
* **Target Answer**: "The cluster has likely lost Quorum. In this state, the remaining nodes recognize they do not have the mathematical majority required by the consensus algorithm to safely commit new data. To protect data integrity and prevent a Split-Brain, the cluster automatically demotes itself to a Read-Only state."

---

## Navigation

⬅ Previous:
[Chapter 13 – Service Mesh and Circuit Breakers](V5-C13-service-mesh.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 15 – SLOs and Error Budgets](V5-C15-slos-error-budgets.md)
