# Practice Guide: Chapter 13 (Volume 2)

## Objective
To inspect the authentication logs and witness the automated botnets attempting to breach your server.

## Assignment 1: Finding the Log
When you connect a VM to the internet, it takes roughly 5 to 10 minutes for automated scanners to find its IP address and begin attacking Port 22.

1. Navigate to the `/var/log` directory.
2. If you are on Ubuntu/Debian, the file you want is `auth.log`.
3. If you are on RHEL/CentOS, the file you want is `secure`.

## Assignment 2: Grepping for Failures
Let's filter the noise and look specifically for authentication failures.

1. Run the `grep` command to search for failures:
   `sudo grep "Failed password" /var/log/auth.log` 
   *(Replace with `/var/log/secure` if on RHEL).*
2. **Observation:** You will likely see a massive wall of text. Look closely at the usernames the bots are trying to guess. You will see things like `root`, `admin`, `oracle`, `pi`, etc.

## Assignment 3: Counting the Attackers
Let's use some advanced piping to see exactly how many unique IP addresses are currently attacking your server.

1. Run this combined command:
   `sudo grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -nr`
2. **Result:** This command grabs all the failures, extracts the 11th column (which contains the IP address), sorts them, counts the unique instances, and orders them from highest to lowest. 
3. **Observation:** The output will show you a list of IP addresses and exactly how many times each IP has attempted to break into your server! This is exactly the data that `fail2ban` uses to trigger its firewall blocks.

## Success Criteria
You have successfully completed this practice if you were able to search your authentication logs and locate the IP addresses of the automated bots currently attacking your VM.
