# Practice Guide: Chapter 29

## Objective
To simulate hunting for the OOM (Out of Memory) Killer in the system logs.

## Assignment 1: The OOM Hunt
When an application crashes and leaves absolutely no error logs behind, it was likely assassinated by the Linux Kernel to prevent a total system failure.

1. First, search the system logs for the exact phrase:
   `grep -i "Out of memory" /var/log/syslog`
   *(If you are on RHEL/CentOS, check `/var/log/messages` instead).*
2. **Result:** If your VM is healthy, the output will be blank.
3. Next, check the raw Kernel ring buffer for the OOM keyword:
   `dmesg | grep -i oom`
4. **Result:** Again, if your VM is healthy, the output will be blank.

*(Note: In the real world, if the OOM Killer triggered, these commands would return lines looking like: `Out of memory: Killed process 1234 (mysqld) total-vm:456789kB`).*

## Assignment 2: Configuration Geography
You must memorize where database configurations live depending on your operating system.

1. If you are on Ubuntu, navigate here:
   `ls -l /etc/mysql/`
2. If you are on RHEL/CentOS, list this file:
   `ls -l /etc/my.cnf`

*(Note: Depending on how your cloud provider configured your base VM image, these files might not exist until you actually install MySQL. The goal is simply to memorize the paths!)*

## Success Criteria
You have successfully completed this practice if you learned the `grep` commands to hunt for the Linux OOM Killer in the system logs and the kernel ring buffer.
