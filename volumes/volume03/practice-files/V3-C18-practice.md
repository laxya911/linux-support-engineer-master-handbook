# Practice Guide: Chapter 18 (Volume 3)

## Objective
To install the `prometheus-node-exporter` daemon and manually interact with its raw metrics endpoint using `curl`.

## Assignment 1: Installation
We need to install the agent that exposes our Linux hardware numbers to the network.

1. Install the exporter package:
   * **Ubuntu/Debian:** `sudo apt update && sudo apt install prometheus-node-exporter`
   * *(RHEL users usually download the binary directly from GitHub, but for this lab, try: `sudo dnf install golang-github-prometheus-node_exporter`)*
2. Verify the daemon is running and listening on Port 9100:
   `sudo ss -tulpn | grep 9100`

## Assignment 2: The Manual Scrape
Prometheus scrapes this port every 15 seconds. Let's pretend to be Prometheus and do a manual scrape!

1. Use `curl` to fetch the raw metrics page:
   `curl http://localhost:9100/metrics`
2. **Observation:** Your terminal will explode with thousands of lines of text! This is exactly what Prometheus downloads.

## Assignment 3: Finding the Needle
The raw output is overwhelming. Let's use `grep` to find specific metrics.

1. How many seconds has your VM been powered on? Let's check the boot time metric:
   `curl -s http://localhost:9100/metrics | grep node_boot_time_seconds`
   *(It will return a massive Unix timestamp).*
2. How much free RAM does your VM have right now?
   `curl -s http://localhost:9100/metrics | grep node_memory_MemFree_bytes`
   *(It will return the raw number in bytes, e.g., 2147483648 for 2GB).*

## Assignment 4: The Formatting 
Look closely at the output from the previous step. Notice the `# HELP` and `# TYPE` lines?

```text
# HELP node_memory_MemFree_bytes Memory information field MemFree_bytes.
# TYPE node_memory_MemFree_bytes gauge
node_memory_MemFree_bytes 3.14159e+08
```
This is the standard Prometheus exposition format. It tells the central server exactly what the metric is, what type of metric it is (a `gauge` goes up and down, a `counter` only goes up), and the current numeric value.

## Success Criteria
You have successfully completed this practice if you installed the `node-exporter` daemon, verified it was listening on Port 9100, and used `curl` combined with `grep` to manually extract your VM's free RAM in bytes.
