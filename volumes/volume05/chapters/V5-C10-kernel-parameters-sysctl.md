# Chapter 10: Performance Tuning the Kernel Parameters (sysctl)

The Linux Kernel ships with default parameters designed to work reasonably well on a 2GB laptop, a 32-core database server, and a Raspberry Pi. These universal defaults are safe, but they are rarely optimal for high-performance enterprise workloads.

When you spin up a server with 256GB of RAM and a 100Gbps network card to handle a million concurrent TCP connections, the default kernel parameters will artificially strangle your hardware. The server will drop connections and exhaust memory queues long before the hardware breaks a sweat.

As a Senior Engineer, you must know how to tune the kernel.

## The `/proc/sys/` Interface

The Linux kernel exposes its internal configuration variables through a virtual filesystem mounted at `/proc/sys/`. 

You can view a current setting by reading the file:
```bash
$ cat /proc/sys/net/ipv4/tcp_max_syn_backlog
2048
```

You can change a setting temporarily by writing to the file (requires root):
```bash
$ echo 8192 > /proc/sys/net/ipv4/tcp_max_syn_backlog
```

However, any changes made directly in `/proc/sys/` will be lost when the server reboots.

## The `sysctl` Command

To make kernel tuning permanent, Linux uses the `sysctl` utility and the `/etc/sysctl.conf` configuration file (or the `/etc/sysctl.d/` directory).

To view all thousands of available parameters:
```bash
$ sysctl -a
```

To apply the changes saved in `/etc/sysctl.conf` immediately without rebooting:
```bash
$ sysctl -p
```

## Essential Tunables for High Performance

### 1. The TCP Network Stack
By default, the Linux networking stack uses small buffers. This is great for minimizing RAM usage on a desktop, but terrible for high-bandwidth server applications.

* `net.core.somaxconn`: The maximum number of connections allowed to queue up for an application socket before the kernel drops them. Default is often 128 or 4096. For heavy web servers, set this to `65535`.
* `net.ipv4.tcp_max_syn_backlog`: The maximum number of half-open connections (SYN received, ACK not yet returned). Increase this to protect against SYN floods and handle massive bursts of traffic.
* `net.core.rmem_max` and `net.core.wmem_max`: The maximum size of the TCP receive and send buffers. If you have a 10Gbps or 100Gbps link, you must dramatically increase these limits (e.g., to `16777216` or 16MB) to saturate the bandwidth.

### 2. Ephemeral Ports
When a server makes an outbound connection (e.g., an NGINX proxy connecting to a backend database), it needs an ephemeral port.
* `net.ipv4.ip_local_port_range`: Defines the range of ports available for outbound connections. The default is `32768 60999` (allowing about 28,000 connections). If you are running a high-traffic proxy, you will run out of ports (Port Exhaustion). Change this to `1024 65535` to maximize capacity.

### 3. Swappiness
We discussed the OOM killer in Chapter 4. The kernel's preference for moving memory from fast RAM to slow Disk is controlled by the "swappiness" parameter.
* `vm.swappiness`: An integer from 0 to 100. The default is usually 60. This means the kernel is fairly aggressive about swapping data to disk. For database servers (like PostgreSQL or Cassandra), you want to avoid disk swapping at almost all costs. Set `vm.swappiness=1` (or `10`) to instruct the kernel to only swap as a last resort before invoking the OOM Killer.

---

## Scenario-Based Troubleshooting

### Scenario A: The API Gateway Bottleneck

> [!IMPORTANT]  
> **Incident Report: The Port Exhaustion**  
> **Reporter:** External Uptime Monitor  
> **SOP execution:**
> 
> 1. **14:00 PM — Incident Receipt:** An API Gateway server starts failing intermittent requests with HTTP 502 Bad Gateway during a high-traffic marketing event.
> 
> 2. **14:02 PM — Triage & Containment:** The engineer logs in and checks NGINX error logs. The logs are flooded with: `connect() to 10.0.0.5:8080 failed (99: Cannot assign requested address)`.
> 
> 3. **14:05 PM — Investigation:** The CPU and Memory are perfectly healthy. The error `Cannot assign requested address` indicates the server cannot find a free local port to initiate the outbound connection to the backend. The engineer checks `sysctl net.ipv4.ip_local_port_range` and sees the default `32768 60999`. They also check `ss -s` and see over 28,000 active and `TIME_WAIT` connections. The server has exhausted all 28,000 ephemeral ports.
> 
> 4. **14:10 PM — Root Cause:** The default kernel port range is too narrow for the massive influx of traffic. Furthermore, TCP connections stay in the `TIME_WAIT` state for 60 seconds after closing, tying up ports long after the transaction is finished.
> 
> 5. **14:15 PM — Resolution:** The engineer edits `/etc/sysctl.conf` and adds:
>    `net.ipv4.ip_local_port_range = 1024 65535`
>    `net.ipv4.tcp_tw_reuse = 1` (Allows the kernel to safely reuse `TIME_WAIT` ports for new outgoing connections).
>    They apply the changes with `sysctl -p`.
> 
> 6. **14:17 PM — Verification:** The NGINX error logs instantly clear up. HTTP 502 errors drop to zero.
> 
> 7. **Post-Mortem:** Discuss the limits of default kernel parameters for edge proxies.
> 
> 8. **Documentation:** Update the Terraform provisioning scripts to apply these kernel tunings automatically to all future API Gateways.

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Blindly copying `sysctl.conf` files from the internet. A tuning parameter that drastically improved performance for an Oracle database in 2012 might completely crash a modern Redis cache in 2026. Never apply a kernel parameter to production unless you fully understand what it does and have benchmarked it in a staging environment.

> [!TIP] Pro-Tip
> When tuning `net.core.somaxconn` (the TCP listen backlog), changing the kernel parameter is only half the battle. The application (e.g., NGINX, Redis, Tomcat) also has its own internal configuration file defining the backlog size. If the kernel allows 65535 connections, but NGINX is configured with `backlog=512`, you will still drop connections. You must tune both the kernel and the application to match.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 10 Practice Guide](../practice-files/V5-C10-practice.md) to intentionally trigger Port Exhaustion using a load testing tool, and fix it using `sysctl`!

## Interview Questions

### Question 1: What is the purpose of the `/proc/sys/` directory, and how does it relate to `sysctl`?
* **Target Answer**: "The `/proc/sys/` directory is a virtual filesystem that exposes the Linux kernel's internal configuration variables in real-time. Writing directly to these files changes the kernel behavior instantly, but the changes do not survive a reboot. `sysctl` is the command-line utility used to manage these parameters persistently by reading from the `/etc/sysctl.conf` file and applying them during the boot sequence."

### Question 2: Why would you lower the `vm.swappiness` value on a database server?
* **Target Answer**: "Databases like PostgreSQL and Cassandra rely heavily on caching data in fast RAM to maintain high performance. The default swappiness value (usually 60) instructs the kernel to aggressively swap memory pages to the disk to keep free RAM available. Swapping database pages to a physical disk introduces massive latency. Lowering `vm.swappiness` to 1 tells the kernel to avoid swapping at all costs, ensuring the database stays entirely in RAM."

### Question 3: What causes Port Exhaustion, and how do you mitigate it?
* **Target Answer**: "Port Exhaustion occurs when a server (usually a load balancer or proxy) makes so many outbound connections to backend servers that it runs out of ephemeral TCP ports. To mitigate it, you can widen the available port range (`net.ipv4.ip_local_port_range`), and enable `tcp_tw_reuse` so the kernel can safely reuse ports that are stuck in the `TIME_WAIT` state rather than waiting 60 seconds for them to fully close."

---

## Navigation

⬅ Previous:
[Chapter 9 – eBPF for Security (Cilium)](V5-C09-ebpf-security-cilium.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 11 – Capacity Planning & Auto-Scaling](V5-C11-capacity-planning.md)
