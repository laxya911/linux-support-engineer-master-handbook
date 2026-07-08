# Practice Guide: Chapter 5 (Volume 2)

## Objective
To read the raw Kernel array tracker to verify if Software RAID is configured on your server.

## Assignment 1: Checking MDSTAT
The fastest way to determine if a server is running Linux Software RAID (`mdadm`) is to ask the Kernel. 

1. Print the contents of the memory device status file:
   `cat /proc/mdstat`
2. **Result:**
   * If your practice VM is a standard, single-drive cloud instance, the output will look something like:
     ```text
     Personalities :
     unused devices: <none>
     ```
   * This confirms your server is **not** using Software RAID.

## Assignment 2: Interpreting Real-World Output
Since you cannot safely crash a hard drive on your practice VM, study the following real-world output block:

```text
Personalities : [raid1] [linear] [multipath] [raid0] [raid6] [raid5] [raid4] [raid10] 
md0 : active raid1 sda3[0] sdb3[1]
      2094080 blocks super 1.2 [2/2] [UU]
```

1. Identify the array name: `md0`
2. Identify the RAID level: `raid1` (Mirroring)
3. Identify the partitions participating in the array: `sda3` and `sdb3`
4. Identify the health: `[UU]` (Both drives are Up/Healthy)

## Success Criteria
You have successfully completed this practice if you learned how to query `/proc/mdstat` and can identify the difference between a `[UU]` healthy array and a `[U_]` degraded array.
