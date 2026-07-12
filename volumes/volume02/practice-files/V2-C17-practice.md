# Practice Guide: Chapter 17 (Volume 2)

## Objective
To schedule a basic task using your user crontab and observe it running automatically.

## Assignment 1: Editing the Crontab
We are going to tell `cron` to write the current date and time to a file every single minute.

1. Open your personal crontab editor:
   `crontab -e`
   *(If it asks you to select an editor, press `1` to choose nano).*
2. Scroll to the very bottom of the file (past all the commented `#` lines).
3. Type the following line exactly:
   `* * * * * /usr/bin/date >> /tmp/cron_practice.log`
4. Save the file and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).
5. **Observation:** The terminal should output `crontab: installing new crontab`.

## Assignment 2: Observing the Output
Now, we simply wait.

1. Run the `cat` command to view the file we told `cron` to create:
   `cat /tmp/cron_practice.log`
2. **Result:** If you run this immediately, you might get a "No such file or directory" error. Why? Because a minute hasn't passed yet!
3. Wait 60 seconds.
4. Run the `cat` command again. You should see a single line with the date and time.
5. Wait another 60 seconds and run it again. You should see two lines!

## Assignment 3: Cleanup
If you don't delete this cronjob, your server will write to that file every single minute for the rest of eternity. Let's clean up.

1. Open your crontab again:
   `crontab -e`
2. Delete the line you added.
3. Save and exit.
4. Delete the log file:
   `rm /tmp/cron_practice.log`

## Success Criteria
You have successfully completed this practice if you edited your `crontab`, successfully forced the server to automate a task in the background, and verified the output by reading the log file.
