# Practice Guide: Chapter 14 (Volume 3)

## Objective
To verify that your Linux Virtual Machine is properly synchronized with a global time server using `chrony`.

## Assignment 1: Verification
Your cloud provider likely installed a time synchronization daemon for you. Let's find out.

1. Check if the `chrony` daemon is running:
   `systemctl status chronyd` OR `systemctl status chrony`
   *(If it is not installed, install it: `sudo apt install chrony` or `sudo dnf install chrony`)*

## Assignment 2: Tracking the Time
Let's see exactly how accurate your clock is right now.

1. Run the chrony tracking command:
   `chronyc tracking`
2. **Observation:** Look at the output. 
   * **Reference ID:** This tells you the IP address or hostname of the Stratum 2 server you are currently pulling time from.
   * **Stratum:** This should say `3` (meaning you are 3 hops away from an atomic clock).
   * **System time:** This tells you how far off your clock is. It will likely say something like `0.000034123 seconds slow of NTP time`.

## Assignment 3: Viewing the Sources
Chrony doesn't just trust one server. It asks multiple servers and averages out the network delay!

1. Run the sources command:
   `chronyc sources -v`
2. **Observation:** You will see a list of 4 or 5 different IP addresses (usually from `pool.ntp.org`). 
   * The server with the `^*` symbol next to it is the primary server Chrony has currently selected as the most accurate.
   * The `^+` symbol indicates fallback servers that Chrony agrees with, but isn't actively using.

## Success Criteria
You have successfully completed this practice if you verified the `chrony` service is running, used `chronyc tracking` to view your system's Stratum level, and used `chronyc sources` to identify your active upstream NTP provider.
