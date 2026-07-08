# Practice Guide: Chapter 19

## Objective
To master the redirection of standard output (`stdout`) and standard error (`stderr`), and to understand the danger of the overwrite operator.

## Assignment 1: Overwrite vs Append
1. Open your terminal.
2. Create a file using the `echo` command and the overwrite operator:
   `echo "This is line one." > practice.txt`
3. Read the file:
   `cat practice.txt`
4. Now, try to add line two using the overwrite operator again:
   `echo "This is line two." > practice.txt`
5. Read the file:
   `cat practice.txt`
   *(Notice that line one was destroyed! This is why `>` is dangerous).*
6. Let's do it correctly. Add line three using the append operator:
   `echo "This is line three." >> practice.txt`
7. Read the file. Both lines are now there.

## Assignment 2: Splitting Streams
We are going to run a command that outputs both normal text and an error simultaneously.

1. Ensure you are a normal user (not root). 
2. Run this command, which tries to list a folder you own (`~`) and a folder you don't have access to (`/root`):
   `ls ~ /root`
3. Notice the output on your screen. You see your home directory files (`stdout`), but you also see a "Permission denied" error (`stderr`).
4. Now, redirect normal output to a file:
   `ls ~ /root > my_files.txt`
5. Notice the output on your screen. You *only* see the error. Why? Because you redirected Stream 1 (`stdout`) into the file, but Stream 2 (`stderr`) still hit your screen.

## Assignment 3: The Black Hole
Let's make the error disappear.

1. Run the same command, but redirect the error to `/dev/null`:
   `ls ~ /root 2> /dev/null`
2. Notice the output. You only see your home directory files. The error vanished into the black hole.
3. Clean up your practice file:
   `rm practice.txt my_files.txt`

## Success Criteria
You have successfully completed this practice if you accidentally destroyed data using `>`, successfully appended data using `>>`, and routed a "Permission denied" error into `/dev/null`.
