# Practice Guide: Chapter 13 (Volume 5)

## Objective
To understand the structure of raw Prometheus metrics and theoretically write PromQL (Prometheus Query Language) statements.

## Assignment 1: The Raw Metric Format
If you `curl http://localhost:9100/metrics` on a server running the Node Exporter, you will receive hundreds of lines of text.

1. **Review this sample output:**
   ```text
   # HELP node_load1 1m load average.
   # TYPE node_load1 gauge
   node_load1 0.75
   # HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
   # TYPE process_cpu_seconds_total counter
   process_cpu_seconds_total 12345.67
   # HELP http_requests_total Total HTTP requests
   # TYPE http_requests_total counter
   http_requests_total{method="GET", status="200"} 1500
   http_requests_total{method="POST", status="500"} 45
   ```
2. **Analysis:** 
   * A **Gauge** is a number that goes up and down (like a car speedometer, or current Load Average).
   * A **Counter** is a number that only *ever* goes up (like a car odometer, or total HTTP requests).

## Assignment 2: Writing PromQL Queries
Imagine you are sitting at the Prometheus web interface. Write the PromQL query to extract the following information.

1. **Goal:** You want to see the total number of HTTP requests that resulted in a Server Error (HTTP 500).
   * *Query:* `http_requests_total{status="500"}`
   * *Result:* 45

2. **Goal:** You want to calculate the Error Rate (Errors per second) over the last 5 minutes. Because `http_requests_total` is a Counter that only goes up, you cannot just look at the raw number. You must use the `rate()` function!
   * *Query:* `rate(http_requests_total{status="500"}[5m])`
   * *Result:* (Calculates the slope of the graph over the last 5 minutes to show how many errors are happening *right now* per second).

3. **Goal:** You want to see the total CPU time consumed, but only for servers located in the `us-east-1` region.
   * *Query:* `process_cpu_seconds_total{region="us-east-1"}`

## Success Criteria
You have successfully completed this practice if you can explain why applying the `rate()` function to a Gauge (like `node_load1`) makes absolutely no mathematical sense. (Answer: The `rate()` function calculates the per-second average increase of a continuously growing number. A Gauge goes up *and* down. You cannot calculate the 'growth rate' of a number that fluctuates randomly!).
