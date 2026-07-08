# Practice Guide: Chapter 7 (Volume 2)

## Objective
To investigate Inode capacity and view the exact metadata stored inside an Inode.

## Assignment 1: The Inode Audit
Let's see how many "index cards" your server was assigned when it was formatted.

1. Check your physical disk space:
   `df -h`
2. Now, check your Inode capacity:
   `df -i`
3. **Observation:** Look at your root (`/`) partition. 
   * The `Inodes` column shows the absolute maximum number of files you can create on this server.
   * The `IUsed` column shows how many files currently exist.
   * The `IFree` column shows how many index cards you have left. 
   * If `IUse%` ever reaches 100%, your server will crash, even if `df -h` says you have 500GB of free space!

## Assignment 2: Viewing Raw Inode Metadata
The `ls -l` command formats metadata so it looks pretty for humans. But we can use the `stat` command to look at the raw Inode data directly.

1. Create a dummy file:
   `touch /tmp/hello.txt`
2. Run the stat command on the file:
   `stat /tmp/hello.txt`
3. **Observation:** Look at the output. 
   * You will literally see `Inode: [some number]`. This is the file's unique ID on the hard drive.
   * You will see the Access, Modify, and Change timestamps.
   * You will see the Uid (Owner) and Gid (Group).
4. Remove the dummy file:
   `rm /tmp/hello.txt`

## Success Criteria
You have successfully completed this practice if you used `df -i` to calculate how many files you are legally allowed to create on your VM, and if you used the `stat` command to view the raw metadata of a single Inode.
