# Practice Guide: Chapter 26

## Objective
To audit your virtual machine for silent boot failures and familiarize yourself with the boot log interface.

## Assignment 1: Auditing for Silent Failures
Let's see if your VM booted cleanly.

1. Run the failed service check command:
   `systemctl --failed`
2. **Result:**
   * If your system is healthy, it will output `0 loaded units listed.`
   * If it outputs a list of services highlighted in red, those services are currently broken.

## Assignment 2: Reading the Boot Log
When a server boots, hundreds of messages are generated in seconds. Let's look at them.

1. Run the journal command to show only the logs from this specific boot:
   `journalctl -b`
2. You are now inside the pager (similar to the `less` command).
3. Use the **Spacebar** to page down.
4. Use the **B** key to page backward (up).
5. Type `/error` and press **Enter** to search the boot logs for the word "error".
6. Press **N** to jump to the next match.
7. Press **q** to quit the log viewer.

## Assignment 3: Re-reading the Dmesg Ring Buffer
The Kernel has its own special log just for hardware detection during boot.

1. Run the Kernel Ring Buffer command:
   `dmesg | less`
2. Look at the timestamps on the left (e.g., `[ 0.000000]`). This is the number of seconds since the kernel woke up. 
3. Page through the log. You will see the kernel detecting your CPUs, your RAM, your network card, and your hard drive. This is exactly what is happening under the hood during Stage 3 of the boot process!
4. Press **q** to quit.

## Success Criteria
You have successfully completed this practice if you verified your system had 0 failed services, successfully navigated the `journalctl -b` interface, and viewed the raw hardware detection logs using `dmesg`.
