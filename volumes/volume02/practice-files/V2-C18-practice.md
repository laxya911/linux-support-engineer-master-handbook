# Practice Guide: Chapter 18 (Volume 2)

## Objective
To use `rsync` to synchronize two local directories and observe how it handles new and modified files.

## Assignment 1: The Initial Sync
We will create a "source" directory (our production data) and a "destination" directory (our backup drive).

1. Create the two directories:
   `mkdir ~/production_data`
   `mkdir ~/backup_drive`
2. Create three dummy files in the production directory:
   `touch ~/production_data/file1.txt`
   `touch ~/production_data/file2.txt`
   `touch ~/production_data/file3.txt`
3. Run the `rsync` command to synchronize them:
   `rsync -avz ~/production_data/ ~/backup_drive/`
4. **Observation:** Look at the output. `rsync` will explicitly list `file1.txt`, `file2.txt`, and `file3.txt` because it had to copy all of them.

## Assignment 2: The Delta Sync
Now, let's see why `rsync` is so powerful.

1. Run the exact same `rsync` command again:
   `rsync -avz ~/production_data/ ~/backup_drive/`
2. **Observation:** The output is completely blank (except for the summary)! `rsync` instantly realized the files were identical and transmitted zero bytes.
3. Now, let's modify just *one* file. Add some text to `file2.txt`:
   `echo "Updating the database" > ~/production_data/file2.txt`
4. Run the `rsync` command a third time:
   `rsync -avz ~/production_data/ ~/backup_drive/`
5. **Result:** `rsync` will only print `file2.txt`. It ignored the other two files completely, saving massive amounts of time!

## Success Criteria
You have successfully completed this practice if you synchronized two directories, proved that `rsync` ignores identical files, and verified that it only transfers files that have been modified.
