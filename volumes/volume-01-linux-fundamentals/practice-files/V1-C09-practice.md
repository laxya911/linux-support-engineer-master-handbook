# Practice Guide: Chapter 9

## Objective
To understand how the Linux Kernel enforces file permissions by intentionally locking out a standard user.

## Assignment 1: The Setup
1. Log in to your VM as your primary standard user.
2. Elevate to root: `sudo su -`
3. Create a sensitive file: `echo "SuperSecretDatabasePassword123" > /tmp/db_pass.txt`
4. Run `ls -l /tmp/db_pass.txt`.
   *Notice the file is owned by `root`, but the permissions are likely `-rw-r--r--` (644).*

## Assignment 2: The Vulnerability
1. Type `exit` to drop out of root and return to your standard user account.
2. Attempt to read the file: `cat /tmp/db_pass.txt`
3. **Result:** You successfully read the file! 
   *Why? Because the "Other" category in `644` has read (`r`) permissions. This is a massive security risk.*

## Assignment 3: Locking It Down
1. Elevate back to root: `sudo su -`
2. Strip away permissions for Group and Other: `chmod 600 /tmp/db_pass.txt`
3. Run `ls -l /tmp/db_pass.txt` and verify it now says `-rw-------`.
4. Type `exit` to return to your standard user.
5. Attempt to read the file again: `cat /tmp/db_pass.txt`
6. **Result:** You receive a "Permission denied" error. The kernel has successfully blocked you based on the octal permissions.

## Assignment 4: Transferring Ownership
1. Use `sudo` to change the owner of the file from `root` to your standard user (replace `username` with your actual username):
   `sudo chown username:username /tmp/db_pass.txt`
2. Run `ls -l /tmp/db_pass.txt` to verify the ownership change.
3. Attempt to read the file again: `cat /tmp/db_pass.txt`
4. **Result:** Success. You are now the Owner of the file, and the Owner has `6` (Read/Write) permissions.

## Success Criteria
You have successfully completed this practice if you were able to read the file, lock yourself out of the file using `chmod 600`, and then regain access by assigning yourself as the owner using `chown`.
