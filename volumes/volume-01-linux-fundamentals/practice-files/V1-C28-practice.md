# Practice Guide: Chapter 28

## Objective
To simulate diagnosing a "502 Bad Gateway" error by checking local listening ports.

## Assignment 1: The Port Audit
When you encounter a 502 Bad Gateway error on an Nginx proxy that forwards to Port 3000, your very first troubleshooting step is always to check if Port 3000 is actually active.

1. Run the network socket command to view all listening ports:
   `ss -tulpn`
2. **Result:** You will likely see `127.0.0.53` (your local DNS resolver) and `0.0.0.0:22` (your SSH server).
3. Now, let's pretend you are looking for a Node.js application running on Port 3000. Filter the output:
   `ss -tulpn | grep 3000`
4. **Result:** The output is completely blank.

## Assignment 2: The Diagnosis
Because the output is blank, you have successfully completed the diagnosis. 

If this were a real server, you have just proven beyond a shadow of a doubt that the Node.js application has crashed. You do not need to look at the Nginx configuration files, and you do not need to restart Nginx. 

You must now switch your focus to finding the `systemd` service name for the Node.js application (e.g. `systemctl status my-app`) and investigating why it died.

## Success Criteria
You have successfully completed this practice if you used the `ss -tulpn` command combined with `grep` to quickly audit internal backend ports.
