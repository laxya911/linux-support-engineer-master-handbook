# Practice Guide: Chapter 16

## Objective
To build muscle memory for the `tar` command by creating, deleting, and successfully extracting a compressed archive.

## Assignment 1: The Setup
We need to generate some dummy data to practice with.

1. Create a new directory in your home folder:
   `mkdir ~/backup_practice`
2. Move into the directory:
   `cd ~/backup_practice`
3. Generate 5 empty text files instantly using brace expansion:
   `touch file{1..5}.txt`
4. Run `ls` to verify the 5 files exist.

## Assignment 2: The Archive
Let's bundle and compress these files.

1. Move *out* of the directory so you can target the folder itself:
   `cd ~`
2. Run the creation command:
   `tar -czvf my_backup.tar.gz backup_practice/`
3. Look at your terminal output. Because you used the `v` (verbose) flag, `tar` printed the name of every file as it was added to the archive.
4. Run `ls -l`. You should now see both the original `backup_practice` directory AND the new `my_backup.tar.gz` file.

## Assignment 3: The Disaster and Recovery
Let's simulate a disaster where a user accidentally deletes the directory.

1. Delete the original directory permanently:
   `rm -rf backup_practice/`
2. Run `ls` to verify it is completely gone. Panic!
3. Recover the directory using your archive:
   `tar -xzvf my_backup.tar.gz`
4. Run `ls` again. The `backup_practice` directory has magically reappeared. 
5. `cd` into it and verify your 5 text files are safe and sound.

## Success Criteria
You have successfully completed this practice if you were able to create a `.tar.gz` file, completely delete the source data, and perfectly restore the directory using the `-xzvf` extraction flags.
