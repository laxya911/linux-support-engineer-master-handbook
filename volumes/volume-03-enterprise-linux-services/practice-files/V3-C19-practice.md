# Practice Guide: Chapter 19 (Volume 3)

## Objective
To conceptually design a Grafana dashboard and understand how PromQL translates hardware metrics into visualizations.

## Assignment 1: Dashboard Design
Imagine you are tasked with building the primary NOC (Network Operations Center) dashboard for a fleet of 5 Web Servers and 1 Database Server.

1. Open a blank text file:
   `nano ~/grafana_design.txt`
2. Sketch out the panels you want on your dashboard. You have space for 4 main panels.
   * *What is the absolute most important metric for the Database?* (Hint: Disk space!)
   * *What is the most important metric for the Web Servers?* (Hint: CPU or Network Traffic).
3. Write down the 4 panels you would create, and specify whether you would use a "Line Graph" or a "Gauge" (like a speedometer).

## Assignment 2: The PromQL Logic
Grafana needs to know what math to execute. Let's write the conceptual PromQL for your panels.

1. Add the PromQL logic to your text file.
2. For the **Database Disk Space** panel, you want a Gauge showing the percentage of free space. The math would be:
   `(node_filesystem_free_bytes / node_filesystem_size_bytes) * 100`
3. For the **Web Server Network Traffic** panel, you want a Line Graph showing bandwidth. The raw metric is just a counter of total bytes downloaded since the server booted. You need to use the `rate()` function to calculate how fast it is growing over a 5-minute window:
   `rate(node_network_receive_bytes_total[5m])`

## Assignment 3: Alerting Strategy
The final step of Dashboard design is setting thresholds.

1. In your text file, write down at what percentage you would trigger a Slack alert for the Database Disk Space.
2. *Remember the Best Practice!* If you alert at 80%, you might wake up at 3:00 AM for an issue that can wait until Monday. If you alert at 99%, the server might crash before you can log in. A common threshold is 90%.

## Success Criteria
You have successfully completed this practice if you conceptually designed a 4-panel monitoring dashboard, documented the theoretical PromQL required to generate the visualizations, and defined a logical alerting threshold to avoid Alert Fatigue.
