# Practice Guide: Chapter 15 (Volume 2)

## Objective
To configure the Linux Audit Daemon, place a watch on a file, and extract forensic data when the file is modified.

## Assignment 1: Installation and Setup
First, we must ensure the `auditd` service is installed and running on your VM.

1. Install the audit daemon:
   * **Ubuntu:** `sudo apt install auditd`
   * **RHEL/CentOS:** `sudo dnf install audit`
2. Create an empty text file that we are going to monitor:
   `touch ~/top_secret.txt`

## Assignment 2: Placing the Tripwire
Let's tell the kernel to watch this specific file. 

1. Use `auditctl` to place a Write/Attribute watch on the file, tagged with the key `secret_watch`:
   `sudo auditctl -w ~/top_secret.txt -p wa -k secret_watch`
2. Verify the watch is active by listing all rules:
   `sudo auditctl -l`
3. **Observation:** You should see your rule listed in the output. The Kernel is now watching!

## Assignment 3: Triggering the Alarm
Let's act like a rogue employee and modify the file.

1. Write some text into the file:
   `echo "I am stealing this data" > ~/top_secret.txt`
2. Change the permissions of the file:
   `chmod 777 ~/top_secret.txt`

## Assignment 4: Forensic Retrieval
The incident has occurred. Now we put on our detective hats and pull the security tapes.

1. Use `ausearch` to query the audit logs for our specific key:
   `sudo ausearch -k secret_watch`
2. **Observation:** The output will be dense, but look closely! 
   * You will see two massive blocks of text (one for the Write, one for the `chmod` Attribute change).
   * Look for `exe=`. It will show `/usr/bin/bash` (for the echo) and `/usr/bin/chmod`.
   * Look for `uid=`. It will log the exact user ID of the person who ran the command!

## Success Criteria
You have successfully completed this practice if you placed a watch on `top_secret.txt`, intentionally modified it, and successfully extracted the forensic proof of the modification using `ausearch`.
