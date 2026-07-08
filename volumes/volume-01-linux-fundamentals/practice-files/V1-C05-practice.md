# Practice Guide: Chapter 5

## Objective
To navigate the Filesystem Hierarchy Standard (FHS) and extract real-time hardware and kernel information from virtual filesystems.

## Assignment 1: Exploring Persistent Data
Boot up your virtual machine and log in. You will use three commands for this lab:
* `pwd` (Print Working Directory): Tells you exactly where you are in the tree.
* `cd <path>` (Change Directory): Moves you to a new location.
* `ls` (List): Shows you the files inside the directory.

1. Type `cd /etc` and press Enter.
2. Type `pwd` to confirm your location.
3. Type `ls` to view the configuration files. 
   * *Notice how many directories exist just for configuring the system.*
4. Type `cd /var/log`.
5. Type `ls`. 
   * *Can you identify any log files related to authentication or system events?*

## Assignment 2: Extracting Live Hardware Data
The kernel exposes hardware information in plain text through the `/proc` directory. You will use the `cat` command (which prints the contents of a file to the screen).

1. **CPU Information**: 
   * Type `cat /proc/cpuinfo`.
   * Find the line that says `model name`. What processor is your virtual machine using?
2. **Memory Information**:
   * Type `cat /proc/meminfo`.
   * Look at the very first line: `MemTotal`. How much RAM (in kilobytes) does your virtual machine have?

## Success Criteria
You have successfully completed this practice if you were able to navigate to `/etc` and `/var/log`, and if you successfully identified your CPU model and total RAM directly from the kernel's virtual `/proc` filesystem.
