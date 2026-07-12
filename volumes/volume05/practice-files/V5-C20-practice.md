# Practice Guide: Chapter 20 (Volume 5)

## Objective
To conceptually synthesize everything you have learned across all 5 Volumes of this handbook into a single, cohesive Capstone architecture.

## Assignment 1: The Capstone Prompt
You are the Lead Platform Engineer at a rapidly growing startup. The CEO asks you to design the complete technological stack and engineering culture for the company. 

Review the architectural decisions below, and mentally map them to the specific Volume and Chapter where you learned the concept.

1. **The Operating System (Volumes 1 & 2):**
   * You standardize the company on Ubuntu LTS for web servers and RHEL/CentOS for databases.
   * You enforce strict `chmod` permissions, ensuring no application ever runs as `root`.
   * You configure `systemd` to automatically restart critical applications if they crash.

2. **The Network (Volume 3):**
   * You design a VPC with Public and Private subnets.
   * The databases sit in the Private subnet, completely inaccessible from the public internet.
   * You configure the AWS Application Load Balancer to terminate SSL/TLS connections, protecting the internal network from encrypted malicious payloads.

3. **The Deployment (Volume 4):**
   * You ban SSH access to production. "Click-Ops" is forbidden.
   * You write all infrastructure as Terraform (`.tf`) files.
   * You package the application code into a Docker container and orchestrate it using Kubernetes, ensuring the system can survive the loss of any single physical node.

4. **The Automation & Observability (Volume 5):**
   * You implement a strict Error Budget (99.9% SLO).
   * You use Prometheus and Grafana to build hierarchical dashboards focusing on Customer Latency, rather than just CPU usage.
   * You build an Internal Developer Platform, allowing developers to self-service their own infrastructure via API calls.

## Final Word
If you understand the prompt above, you are no longer a Junior SysAdmin. You possess the theoretical knowledge of a Senior Cloud Engineer. 

Your next step is to put down the handbook, open a terminal, and start building. Good luck!
