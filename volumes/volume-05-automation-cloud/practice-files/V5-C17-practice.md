# Practice Guide: Chapter 17 (Volume 5)

## Objective
To practice the "Verbal Troubleshooting" methodology required to pass Senior Engineering interviews.

## Assignment 1: The "No Space Left on Device" Error
**The Prompt:** The interviewer asks: "A developer's script fails with the error `No space left on device`. You log into the server, run `df -h`, and see that the root filesystem (`/`) is only 40% full. There is plenty of space. Explain exactly how this is possible, and how you fix it."

1. **Step 1: Don't Panic.** Acknowledge the complexity. 
   * *You say:* "That's an interesting scenario. If the disk has gigabytes of free physical space, but the Kernel is throwing a 'no space' error, it means we have exhausted a different, hidden storage limit."

2. **Step 2: State the Hypothesis.** 
   * *You say:* "In Linux, every file requires two things: data blocks to store the actual contents, and an 'inode' to store the metadata (permissions, file name). If a server creates millions of tiny 1-byte files (like caching files or session tokens), it will consume all the available inodes before it consumes the physical disk space."

3. **Step 3: Prove the Hypothesis (The Commands).**
   * *You say:* "To verify this, I would run `df -i`. This command displays inode usage instead of block usage. If it shows 100% inode utilization on `/`, my hypothesis is correct."

4. **Step 4: The Resolution.**
   * *You say:* "To fix it, I need to find the directory containing millions of tiny files. Since standard `du` or `find` might crash or take hours on a massive directory, I would use a specialized script or `find / -xdev -type f | cut -d "/" -f 2 | sort | uniq -c | sort -n` to locate the culprit directory (often `/var/lib/php/sessions` or `/tmp`), and then delete the useless files to free up the inodes."

## Assignment 2: The Silent SSH Failure
**The Prompt:** "You try to `ssh user@10.0.0.5`. It hangs for 60 seconds, and then says 'Connection Timed Out'. The server is definitely online. How do you troubleshoot this without having console access to the server?"

1. **The Verbose Output:**
   * *You say:* "First, I would run SSH in verbose mode: `ssh -vvv user@10.0.0.5`. This will tell me exactly where the connection is failing. If it fails immediately, the TCP port is blocked. If it hangs at 'expecting SSH2_MSG_KEXINIT', it's an MTU or packet fragmentation issue."

2. **The Network Check:**
   * *You say:* "If I can't reach the port at all, I would run `traceroute 10.0.0.5` to see if a router in the middle is dropping the packets. If the packets make it to the destination subnet, it's highly likely a local firewall rule (like `iptables` or an AWS Security Group) is blocking port 22 inbound."

## Success Criteria
You have successfully completed this practice if you understand that the interviewer cares far more about *how you thought through the problem* (using verbose flags, understanding inodes) than whether you instantly guessed the correct answer.
