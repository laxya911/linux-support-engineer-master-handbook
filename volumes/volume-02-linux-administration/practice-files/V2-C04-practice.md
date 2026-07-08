# Practice Guide: Chapter 4 (Volume 2)

## Objective
To map out the storage architecture of your Virtual Machine using standard LVM diagnostic tools.

## Assignment 1: The Block List
The quickest way to see if your server is using LVM is to look at the raw block devices.

1. Run the list block command:
   `lsblk`
2. **Observation:** Look at the tree output. If you see a hard drive (like `sda` or `vda`), and beneath it you see a partition (like `sda3`), and beneath *that* you see items with the type `lvm`, your server was installed using LVM!

## Assignment 2: Exploring the 3 Layers
Let's look at the three tiers of LVM on your machine.

1. Check your Physical Volumes:
   `sudo pvs`
   *(This shows the actual hard drives plugged into the server that LVM controls).*
2. Check your Volume Group:
   `sudo vgs`
   *(Look at the `VFree` column. Does your server have any free space sitting in the pool?)*
3. Check your Logical Volumes:
   `sudo lvs`
   *(This shows the flexible partitions you have carved out of the pool).*

## Assignment 3: Finding the Mapper Path
When you run commands like `lvextend`, you cannot use standard `/dev/sda` paths. You must use the LVM "mapper" paths.

1. Run the disk free command:
   `df -h`
2. **Observation:** Look for your root partition (`/`). On the far left, you will likely see a path that looks like `/dev/mapper/ubuntu--vg-root` or `/dev/mapper/rl-root`. This is the absolute path to your Logical Volume. This is the path you would use if you ever needed to resize it!

## Success Criteria
You have successfully completed this practice if you were able to run `lsblk`, `pvs`, `vgs`, and `lvs`, and identify the `/dev/mapper/` path for your root filesystem.
