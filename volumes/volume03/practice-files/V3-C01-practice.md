# Practice Guide: Chapter 1 (Volume 3)

## Objective
To utilize the `curl` command to interact directly with web servers, and use the `ss` command to view your local listening ports.

## Assignment 1: Being the Client
Normally, your web browser hides the raw HTTP communication from you. Let's use `curl` to act as a raw client.

1. Fetch the raw HTML of a website:
   `curl http://example.com`
2. **Observation:** Your terminal will be flooded with the raw HTML code of the page. This is exactly what your browser downloads and renders into a visual webpage!
3. Now, fetch *only* the HTTP Headers (the metadata):
   `curl -I https://google.com`
4. **Observation:** You will see a `HTTP/2 200` status code, indicating success. You will also see a `server: gws` header, meaning Google uses its own proprietary "Google Web Server" software!

## Assignment 2: Checking Local Ports
Let's see what ports your own Linux VM is currently listening on.

1. Run the Socket Statistics command (requires `sudo` to see the process names):
   `sudo ss -tulpn`
2. **Observation:** Look at the `Local Address:Port` column. 
   * Do you see `0.0.0.0:22`? That is your SSH daemon (`sshd`) waiting for you to connect to it!
   * Look at the `Process` column on the far right. It explicitly tells you which program owns which port.

## Assignment 3: Creating a Port Conflict
Let's purposely break things by trying to listen on a port that is already taken.

1. We are going to use the `nc` (netcat) tool to manually open a port. Try to open Port 22 (which is currently owned by SSH):
   `sudo nc -l -p 22`
2. **Observation:** You will receive an error: `nc: Address already in use`. The Linux kernel protected the SSH service by refusing to let netcat steal its port!
3. Now, open a high-numbered port that isn't being used:
   `sudo nc -l -p 8080`
4. **Observation:** The command will hang. It is successfully listening! Press `Ctrl+C` to cancel it.

## Success Criteria
You have successfully completed this practice if you used `curl -I` to fetch headers from a public website, verified your local SSH port using `ss`, and successfully caused an "Address already in use" error by trying to bind to Port 22.
