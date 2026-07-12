# Practice Guide: Chapter 11

## Objective
To simulate a frozen application, locate its PID using filters, and execute a surgical termination using POSIX signals.

## Assignment 1: The Rogue Process
We will create a dummy process that runs for a very long time, locking up the terminal.

1. Type `sleep 3600` and press Enter.
   *(This tells the system to do nothing for 3,600 seconds/1 hour).*
2. Try typing other commands like `ls`. 
   *Notice how the terminal is locked. The process is running in the **Foreground**.*
3. Press `Ctrl + C` to kill the foreground process. You have your terminal back.

## Assignment 2: The Background
1. Let's run it again, but this time in the background so we can keep working:
   `sleep 3600 &`
2. You will see an output like `[1] 10543`. The number on the right is the Process ID (PID).
3. Type `ls` or `pwd`. Notice how your terminal works perfectly while `sleep` runs silently in the background.

## Assignment 3: The Hunt and Kill
Imagine you forgot the PID, and you need to stop the `sleep` process.

1. Run the ultimate hunting command:
   `ps aux | grep sleep`
2. Look at the output. Find the line that shows `sleep 3600`. 
3. Look at the second column of that line. That is your PID.
4. Attempt a graceful shutdown:
   `kill <PID>` *(Replace `<PID>` with your actual number)*.
5. Verify it is dead by running the hunt command again:
   `ps aux | grep sleep`
   *If it is gone, the kill was successful!*

## Assignment 4: The Force Quit
Sometimes processes ignore the polite `kill` command.

1. Launch it again: `sleep 3600 &`
2. Find its new PID using `ps aux | grep sleep`.
3. Terminate it with extreme prejudice:
   `kill -9 <PID>`
4. You will likely see an immediate message in your terminal stating the process was `Killed`.

## Success Criteria
You have successfully completed this practice if you were able to launch a background process using `&`, hunt down its PID using `ps aux | grep`, and destroy it using both `kill` and `kill -9`.
