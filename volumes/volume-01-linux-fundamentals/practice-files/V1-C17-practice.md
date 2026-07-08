# Practice Guide: Chapter 17

## Objective
To map the physical layout of your virtual machine and practice the recursive hunting technique used to find large files.

## Assignment 1: Mapping the Hardware
Let's see what physical disks are attached to your VM.

1. Run the block device list command:
   `lsblk`
2. Look at the output tree.
   * You will likely see `sda` or `vda` representing your primary hard drive.
   * Underneath it, you will see partitions like `sda1`, `sda2`.
   * Look at the far right column (Mount Point). Notice how the main partition is mounted to `/`.

## Assignment 2: The Health Check
Let's verify how much space you have left on your VM.

1. Check your free space:
   `df -h`
2. Look for the row where the `Mounted on` column says `/`. 
3. Look at the `Use%` column. As long as it is below `90%`, your server is healthy.

## Assignment 3: The Hunt
Imagine your disk is full. We are going to practice hunting down large folders.

1. Navigate to the root of the filesystem:
   `cd /`
2. Run the summarize command using `sudo` (so it doesn't complain about permission denied errors on system folders):
   `sudo du -sh *`
3. Wait a few seconds for it to calculate. Look at the output. 
   *(Notice that the `/usr` and `/var` directories are likely the largest, taking up gigabytes of space).*
4. Navigate into the `/var` directory:
   `cd /var`
5. Run the hunt command again:
   `sudo du -sh *`
6. Look at the output. Notice how the `/var/log` and `/var/lib` folders are taking up the most space within the `/var` directory.

## Success Criteria
You have successfully completed this practice if you used `lsblk` to see your block devices, verified your free space percentage using `df -h`, and successfully executed a multi-level hunt using `du -sh *`.
