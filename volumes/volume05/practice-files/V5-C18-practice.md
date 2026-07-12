# Practice Guide: Chapter 18 (Volume 5)

## Objective
To write a "3:00 AM Runbook" that is concise, action-oriented, and foolproof.

## Assignment 1: The Bad Runbook
Review this terrible runbook written by a junior engineer:

> **Alert: Redis Cache Full**
> When Redis fills up, the application gets really slow because it has to fall back to the main MySQL database. Redis uses RAM, so if the server only has 16GB of RAM, and the `maxmemory` setting in the `redis.conf` file is reached, it will start evicting keys based on the LRU policy. If the policy isn't set, it just rejects writes. You need to log into the server, restart the service to clear the cache, or maybe use the `redis-cli` to flush it if restarting is too risky.

**Why it fails:** At 3:00 AM, the on-call engineer doesn't care *why* Redis uses RAM. They just need to know exactly what commands to type to stop the website from crashing!

## Assignment 2: Writing the Good Runbook
Rewrite the runbook using the "Action-Oriented" format.

> # RUNBOOK: Redis Cache Full (Alert ID: #882)
> 
> **Symptoms:** Web servers are returning HTTP 500s. User sessions are dropping.
> 
> ## Step 1: Verify the Issue
> Log into the Redis server and check memory utilization:
> ```bash
> redis-cli info memory | grep used_memory_human
> ```
> *If usage is > 95%, proceed to Step 2.*
> 
> ## Step 2: Immediate Mitigation (Safe)
> We must clear the cache. This will temporarily spike database load but will restore website functionality. Do NOT restart the `redis-server` process, as it will break active TCP connections.
> 
> Run the flush command via CLI:
> ```bash
> redis-cli FLUSHALL ASYNC
> ```
> *Note: The `ASYNC` flag is critical to prevent blocking the thread.*
> 
> ## Step 3: Verification
> Verify the memory has dropped:
> ```bash
> redis-cli info memory | grep used_memory_human
> ```
> Check the Grafana dashboard to confirm HTTP 500s have stopped.
> 
> ## Escalation
> If the command fails or the database crashes from the subsequent load spike, page the DBA On-Call via PagerDuty (Escalation Policy #2).

## Success Criteria
You have successfully completed this practice if you can see why the second runbook is infinitely superior. It tells the panicked engineer exactly what to type, what the expected output is, and exactly what to do if it fails.
