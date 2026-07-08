# Practice Guide: Chapter 1 (Volume 2)

## Objective
To safely grant granular, limited administrative privileges to a specific user using the `visudo` command.

## Assignment 1: The Setup
First, we need to create a fake developer account.

1. Create a new user named `dbadmin`:
   `sudo useradd -m -s /bin/bash dbadmin`
2. Give the user a password (you can use "password123" for this lab):
   `sudo passwd dbadmin`

## Assignment 2: Identifying the Target Command
We only want `dbadmin` to be able to restart the MySQL database. We do not want them to be able to reboot the server or read our files.

1. We must find the absolute path to the `systemctl` command. Run:
   `which systemctl`
2. Note the output. (It is usually `/bin/systemctl` or `/usr/bin/systemctl`).

## Assignment 3: Editing Sudoers
Now we will use the safety tool to grant the permission.

1. Open the sudoers file safely:
   `sudo visudo`
2. Scroll to the very bottom of the file.
3. Add this exact line (replace the path if your `which` command output was different):
   `dbadmin ALL=(ALL) /bin/systemctl restart mysql`
4. Save and exit (If you are using Ubuntu, `visudo` likely opened using the `nano` interface, so press `Ctrl+O`, `Enter`, `Ctrl+X`).

## Assignment 4: Verification
Let's test if our granular permissions worked.

1. Switch to the `dbadmin` user:
   `su - dbadmin`
2. Try to run an unauthorized command (like viewing the shadow password file):
   `sudo cat /etc/shadow`
3. Enter `dbadmin`'s password. 
4. **Result:** You should receive a harsh warning: `Sorry, user dbadmin is not allowed to execute '/usr/bin/cat /etc/shadow' as root.` The system stopped you!
5. Now try the authorized command:
   `sudo /bin/systemctl restart mysql`
   *(Note: Even if mysql isn't installed on your VM, you should get a 'Unit mysql.service not found' error rather than a 'Sorry, user is not allowed' error, proving the sudoers file allowed the execution).*
6. Type `exit` to return to your normal user account.

## Success Criteria
You have successfully completed this practice if you were blocked from reading `/etc/shadow`, but allowed to execute the `systemctl restart mysql` command while logged in as the `dbadmin` user.
