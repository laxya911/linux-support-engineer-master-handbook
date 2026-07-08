# Practice Guide: Chapter 9 (Volume 2)

## Objective
To read the kernel routing table and trace the path of a packet across the internet.

## Assignment 1: Reading the Routing Table
Let's see how your VM knows how to reach the internet.

1. Display the routing table:
   `ip route`
2. **Observation:**
   * You should see a line starting with `default via`.
   * The IP address listed after `via` is your Default Gateway (the router provided by your cloud host).
   * Notice the `dev` section. This tells you which physical network interface (`eth0`, `ens3`, etc.) the traffic will leave from.

## Assignment 2: Using Traceroute
The `ping` command tells you *if* a destination is reachable. The `traceroute` command tells you *how* you reached it.

*(Note: Depending on your VM, you may need to install this tool first via `sudo apt install traceroute` or `sudo dnf install traceroute`).*

1. Trace the path from your server to Google's DNS server:
   `traceroute 8.8.8.8`
2. **Observation:**
   * Watch the output build line by line.
   * **Hop 1** is your Default Gateway (the same IP address you saw in `ip route`).
   * Every line after that represents a physical router somewhere in the world that touched your packet. 
   * Notice the millisecond (ms) times. A massive jump in time indicates the packet just crossed an ocean or a major geographic distance!

## Success Criteria
You have successfully completed this practice if you identified your Default Gateway using `ip route` and mapped the network path to an external IP address using `traceroute`.
