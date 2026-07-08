# Practice Guide: Chapter 17 (Volume 4)

## Objective
To enable the Magic SysRq key and intentionally force a Linux kernel to panic (do NOT do this on a production server).

## Assignment 1: Enabling SysRq
The "Magic SysRq Key" is a mechanism built directly into the Linux kernel that allows you to send low-level commands regardless of the system's state, even if it is completely frozen.

1. **WARNING:** This practice will instantly crash your system. Save all your work, and only perform this on a disposable Virtual Machine!
2. By default, most modern distributions disable the dangerous SysRq commands. We must enable them.
3. Open the `sysctl` configuration file:
   `sudo nano /etc/sysctl.d/99-sysrq.conf`
4. Add the following line to enable all SysRq functions:
   `kernel.sysrq = 1`
5. Save and exit, then reload the configuration:
   `sudo sysctl -p /etc/sysctl.d/99-sysrq.conf`

## Assignment 2: Forcing the Panic
Now we will write a character to a special `/proc` file to trigger the panic.

1. We will use the `echo` command to send the letter `c` (for "Crash") to the `sysrq-trigger` file. This must be done as the absolute root user (not just `sudo echo`).
2. Run the command:
   `echo c | sudo tee /proc/sysrq-trigger`
3. **Observation:** Your SSH session will instantly freeze. The terminal will stop responding to your keyboard.
4. If you have access to the physical console of the Virtual Machine (e.g., via VirtualBox or AWS Console Screenshot), you will see the classic Linux Kernel Panic screen. It will say `Kernel panic - not syncing: sysrq triggered crash`.
5. Below that, you will see a "Call Trace" (the backtrace) showing exactly which functions led to the crash (in this case, `sysrq_handle_crash`).

## Assignment 3: Recovery
1. Because we did not configure `kdump` in this quick practice, the server will remain frozen forever. 
2. Go to your hypervisor (VirtualBox/VMware) or Cloud Console (AWS/GCP) and issue a Hard Reset / Force Reboot to the Virtual Machine.
3. When it boots back up, check `/var/log/syslog`. You will see a gap in time, and absolutely no record of the panic, proving the theory from the chapter!

## Success Criteria
You have successfully completed this practice if you enabled the SysRq triggers, forced a kernel crash, and verified that standard logging mechanisms fail to capture the event.
