# Practice Guide: Chapter 22

## Objective
To write a "heartbeat" script, schedule it in cron, and prove that the server is executing it automatically.

## Assignment 1: The Heartbeat Script
We will write a script that simply prints the current time and appends it to a log file.

1. Create a script in your home directory:
   `nano ~/heartbeat.sh`
2. Write the following code. *(Notice we are using absolute paths like `/bin/echo` just like a real cron job requires!)*
   ```bash
   #!/bin/bash
   /bin/echo "The server is alive at $(/bin/date)" >> /home/YOUR_USERNAME/heartbeat.log
   ```
   *(Be sure to replace `YOUR_USERNAME` with your actual Linux username).*
3. Save and exit the file.
4. Make the script executable:
   `chmod +x ~/heartbeat.sh`
5. Test it manually once:
   `~/heartbeat.sh`
6. Check the log file to ensure it worked:
   `cat ~/heartbeat.log`

## Assignment 2: Scheduling the Automation
Now let's hand the script over to the cron daemon.

1. Open your user's crontab editor:
   `crontab -e`
   *(If it asks you to select an editor, choose `nano` or `vim`).*
2. Scroll to the very bottom of the file (past all the `#` comments).
3. Add the following line to schedule the job to run every single minute:
   `* * * * * /home/YOUR_USERNAME/heartbeat.sh`
4. Save and exit the file. You should see a message saying `crontab: installing new crontab`.

## Assignment 3: The Verification
1. Do not type anything. Just wait for 2 full minutes.
2. Check the log file:
   `cat ~/heartbeat.log`
3. **Result:** You should see multiple lines in the log file, proving that the cron daemon woke up and ran your script automatically in the background.

## Assignment 4: The Cleanup
Never leave test scripts running in cron.

1. Open the crontab editor again:
   `crontab -e`
2. Delete the line you added.
3. Save and exit.
4. Verify your crontab is empty:
   `crontab -l`

## Success Criteria
You have successfully completed this practice if you wrote a script with absolute paths, scheduled it with the `* * * * *` syntax, proved it ran automatically by checking the log, and successfully removed it from the crontab.
