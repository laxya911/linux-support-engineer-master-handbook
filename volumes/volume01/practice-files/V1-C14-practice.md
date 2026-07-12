# Practice Guide: Chapter 14

## Objective
To master local network identification, execute the DNS troubleshooting sequence, and hunt down open ports.

## Assignment 1: Local Discovery
1. Find your IP address:
   `ip a`
   *(Look for an interface like `eth0` or `ens33`. Your IP will be listed next to the word `inet`, likely starting with 10.x.x.x or 192.168.x.x).*
2. Find your Default Gateway (your router):
   `ip r`
   *(Look at the first line that says `default via`. The IP address listed there is your router).*
3. Ping your router to prove local connectivity:
   `ping -c 4 <ROUTER_IP>`
   *(The `-c 4` flag tells ping to stop after sending 4 packets, so you don't have to press `Ctrl+C`).*

## Assignment 2: External Discovery
Let's verify that your virtual machine can talk to the outside world.

1. Test raw IP connectivity to the internet (Google's Public DNS):
   `ping -c 4 8.8.8.8`
   *(If this succeeds, your ISP and firewall are working).*
2. Test DNS resolution:
   `ping -c 4 google.com`
   *(If this succeeds, your DNS servers are working).*
3. Perform a manual DNS query to see exactly how the name translates to an IP:
   `dig google.com +short`
   *(This will output the raw IP addresses for Google's web servers).*

## Assignment 3: Port Hunting
Every time you connect to your server, you are using SSH (Port 22). Let's prove the daemon is actually listening.

1. Run the socket statistics command:
   `sudo ss -tulpn`
2. Look at the output.
   * Under the `Local Address:Port` column, you should see `0.0.0.0:22` or `*:22`.
   * This means the server is listening on Port 22 on all available network interfaces.
   * Because you used `sudo`, the far right column should say `"sshd"` along with its PID, proving the SSH daemon is the application controlling that port.

## Success Criteria
You have successfully completed this practice if you were able to locate your IP address, ping your default gateway, verify DNS resolution using `dig`, and visually confirm that the `sshd` process is bound to TCP Port 22.
