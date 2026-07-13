# Chapter 9: eBPF for Security (Cilium)

In Chapter 2, we learned how eBPF can safely execute sandboxed code inside the Linux kernel to monitor performance. But eBPF's capabilities do not end at observation. Because eBPF programs run deep within the kernel, they have the power to intercept, modify, and drop network packets before the standard Linux networking stack even sees them.

This capability has sparked a revolution in Cloud-Native Security, completely bypassing `iptables` and traditional firewalls in favor of lightning-fast, kernel-level enforcement.

## The Problem with `iptables` in Kubernetes

In Volume 4, we built Kubernetes clusters. By default, Kubernetes uses `kube-proxy` backed by `iptables` (or IPVS) to route traffic between pods and enforce Network Policies.

`iptables` was designed in the 1990s as a sequential list of rules. If a packet arrives, `iptables` evaluates it against rule 1, then rule 2, then rule 3, and so on. In a modern Kubernetes cluster running thousands of microservices, `kube-proxy` generates tens of thousands of `iptables` rules. Evaluating a single packet against a 50,000-rule list introduces massive latency and CPU overhead.

Furthermore, `iptables` only understands IP addresses and Ports (Layer 3 and Layer 4). It has no concept of an HTTP request, a Kafka topic, or a gRPC method.

## Enter Cilium

Cilium is an open-source project (now the default networking standard for Google Kubernetes Engine and AWS EKS Anywhere) that replaces `kube-proxy` entirely by utilizing eBPF.

Instead of writing thousands of sequential `iptables` rules, Cilium compiles network and security policies directly into highly optimized eBPF programs and attaches them to the virtual network interfaces of your pods.

### The Power of eBPF Security
1. **Unmatched Performance:** Because eBPF uses hash tables rather than sequential lists, evaluating a packet against 10 rules takes exactly the same amount of CPU time as evaluating it against 100,000 rules. The complexity is O(1).
2. **Layer 7 Visibility:** Cilium can inspect the payload of the packets. You can write a security policy that allows Microservice A to make an HTTP `GET` request to Microservice B, but immediately drops an HTTP `POST` or `DELETE` request at the kernel level.
3. **Identity-Based Security:** IP addresses change constantly in Kubernetes. Traditional firewalls rely on static IPs. Cilium integrates with Kubernetes labels. It enforces security based on the cryptographic *identity* of the pod (e.g., `app=frontend`), entirely ignoring the ephemeral IP address.

## Hubble: The eBPF Microscope

Securing a cluster is impossible if you cannot see what is happening inside it. Hubble is the observability layer built on top of Cilium. 

Because Cilium's eBPF probes already sit in the kernel analyzing every packet for security enforcement, Hubble simply streams that data out. Without installing a single sidecar proxy or modifying your application code, Hubble can generate a live, interactive dependency map showing exactly which pods are talking to each other, their latency, and any dropped packets.

---

## Scenario-Based Troubleshooting

### Scenario A: The Cryptominer Compromise

> [!IMPORTANT]  
> **Incident Report: The Rogue Pod**  
> **Reporter:** Security Operations Center (SOC)  
> **SOP execution:**
> 
> 1. **11:00 AM — Incident Receipt:** AWS GuardDuty alerts the SOC that an EC2 instance in the production Kubernetes cluster is making outbound DNS requests to known cryptocurrency mining pools.
> 
> 2. **11:05 AM — Triage & Containment:** The engineer opens the Hubble UI. Because eBPF sees all kernel-level socket connections, the engineer instantly filters the network map for external connections. They identify a specific pod, `image-processing-worker-7b5f`, making continuous TCP connections to `stratum.slushpool.com`.
> 
> 3. **11:10 AM — Investigation:** The engineer looks at the default Kubernetes Network Policies. The cluster uses standard `iptables`, and the default policy allows all pods to have unrestricted egress to the internet. An attacker exploited a vulnerability in the image processing library to download and execute a cryptominer.
> 
> 4. **11:15 AM — Resolution:** The engineer deletes the compromised pod. To prevent recurrence, they deploy a Cilium Network Policy enforced by eBPF. The policy restricts the `image-processing-worker` to only allow outbound egress to the AWS S3 API endpoints on Port 443. All other outbound connections are dropped instantly by the kernel.
> 
> 5. **11:20 AM — Verification:** The engineer monitors Hubble. When the replacement pod boots up, it attempts to contact the cryptomining pool, but Hubble shows the packets being marked as `DROPPED` at Layer 3. The attack is thwarted.
> 
> 6. **Post-Mortem:** Discuss why unrestricted egress is dangerous in containerized environments.
> 
> 7. **Documentation:** Mandate a "Default Deny" egress policy using Cilium for all new namespaces in the cluster.

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Continuing to use `kube-proxy` and `iptables` for large-scale clusters. Once a cluster exceeds a few hundred nodes and thousands of services, `iptables` becomes a severe performance bottleneck. If your pod-to-pod latency is inexplicably high during scaling events, you are likely hitting the limits of `iptables` sequential rule evaluation. It is time to migrate to an eBPF-based CNI (Container Network Interface) like Cilium.

> [!TIP] Pro-Tip
> Cilium's eBPF architecture allows for "DSR" (Direct Server Return). Normally, when traffic hits a Kubernetes NodePort, it traverses the `kube-proxy`, goes to the pod, and the response must travel all the way back through the original node. DSR allows the pod's response packet to bypass the proxy entirely and return straight to the client, drastically reducing latency for bandwidth-heavy applications like video streaming.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 9 Practice Guide](../practice-files/V5-C09-practice.md) to install Cilium in Minikube and write a Layer 7 policy blocking an HTTP `DELETE` request!

## Interview Questions

### Question 1: Why does `iptables` scale poorly in large Kubernetes clusters?
* **Target Answer**: "`iptables` processes rules sequentially (a linked list). If a packet arrives, it must be evaluated against the first rule, then the second, and so on. In a massive cluster, `kube-proxy` can generate tens of thousands of rules for service routing and security. Evaluating packets against 50,000 rules adds significant CPU overhead and latency. eBPF solves this by using highly optimized hash maps, allowing O(1) constant-time lookups regardless of the number of rules."

### Question 2: How does Cilium enforce security without relying on IP addresses?
* **Target Answer**: "IP addresses in Kubernetes are ephemeral; pods are created and destroyed constantly, changing IPs. Cilium assigns a cryptographic security identity to each pod based on its Kubernetes labels (e.g., `role=database`). The eBPF policies are tied to the identity, not the IP. This ensures the security policy remains strictly enforced even as the cluster scales up and down."

### Question 3: What is the advantage of Layer 7 visibility in a Network Policy?
* **Target Answer**: "Traditional firewalls (Layer 4) can only block traffic based on IP and Port. If you allow Port 80 for web traffic, you allow *everything* on Port 80. With Layer 7 visibility, an eBPF policy can inspect the actual application payload. This allows you to write fine-grained security rules, such as allowing a microservice to read from an API (HTTP GET) but blocking it from modifying data (HTTP POST or DELETE)."

---

## Navigation

⬅ Previous:
[Chapter 8 – Advanced Filesystems (ZFS & Btrfs)](V5-C08-advanced-filesystems.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 10 – Performance Tuning the Kernel Parameters (sysctl)](V5-C10-kernel-parameters-sysctl.md)
