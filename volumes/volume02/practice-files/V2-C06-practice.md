# Practice Guide: Chapter 6 (Volume 2)

## Objective
To safely inspect the `/etc/fstab` file to identify how a server's filesystems are mounted at boot.

## Assignment 1: Reading the FSTAB
The File System Table (`fstab`) is the blueprint for how a Linux server attaches storage when it turns on.

1. Display the contents of your fstab file:
   `cat /etc/fstab`
2. **Observation:** Ignore the lines starting with `#` (comments). Look at the active configuration lines.
3. Every active line has 6 columns:
   1. **Device:** (e.g., `/dev/sda1`, or a UUID, or an IP address like `10.0.0.50:/share`)
   2. **Mount Point:** Where the drive is attached (e.g., `/`, or `/mnt/data`)
   3. **Filesystem Type:** (e.g., `ext4`, `xfs`, `nfs`, `cifs`)
   4. **Options:** (e.g., `defaults`, `ro` for read-only)
   5. **Dump:** (Legacy backup setting, usually `0`)
   6. **Pass:** (Filesystem check order. `1` for root, `2` for others, `0` to skip).

## Assignment 2: Identifying the Target
Look closely at the 3rd column (Filesystem Type) in your output.

1. Does your server have any lines with `nfs` or `cifs`?
2. **Result:** Because this is a practice VM, you almost certainly only have `ext4` or `xfs`. This means your VM relies entirely on local block storage and has no Network Attached Storage configured.

## Assignment 3: The Danger of FSTAB
> [!CAUTION]  
> If you make a typo in the `/etc/fstab` file, your server will completely fail to boot. 

1. When engineers edit this file, they **always** run the following command immediately after saving it:
   `sudo mount -a`
2. Run this command now. 
3. **Result:** The `mount -a` command tells the system to mount everything listed in `/etc/fstab`. If you made a typo, it will print an error *right now* while the server is still running, allowing you to fix it before you reboot and destroy the server!

## Success Criteria
You have successfully completed this practice if you successfully read your `/etc/fstab` file, identified your filesystem types (ext4/xfs), and learned the critical safety habit of running `mount -a` after any edits.
