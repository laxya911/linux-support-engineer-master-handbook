# Practice Guide: Chapter 8

## Objective
To safely provision a new user account, grant it administrative privileges, and verify its ability to escalate using `sudo`.

## Assignment 1: User Provisioning
*Note: You must run these commands as root or prefix them with `sudo`.*

1. Create a new user named `junioradmin`:
   `useradd -m -s /bin/bash junioradmin` 
   *(The `-m` creates their home directory, and `-s` assigns their default shell).*
2. Assign a password to the new user:
   `passwd junioradmin`
3. Verify the user was created by inspecting the passwd file:
   `cat /etc/passwd | grep junioradmin`
   *You should see their username, UID, GID, and home directory path.*

## Assignment 2: Privilege Escalation
Currently, `junioradmin` is a standard user with no power. Let's fix that.

1. Add the user to the administrative group:
   * **Debian/Ubuntu 26.04**: `usermod -aG sudo junioradmin`
   * **RHEL 10 / CentOS**: `usermod -aG wheel junioradmin`
2. Switch your current session to the new user:
   `su - junioradmin`
3. Verify your identity by typing `whoami`.
4. Try to read the highly restricted shadow file *without* privileges:
   `cat /etc/shadow`
   *You should receive a "Permission denied" error.*
5. Now, borrow root's power:
   `sudo cat /etc/shadow`
6. Enter the password you created in Assignment 1.
   *Because junioradmin is in the admin group, `sudo` will execute the command and display the password hashes.*

## Assignment 3: Cleanup
1. Type `exit` to log out of the `junioradmin` account and return to your original user.
2. Delete the test user and wipe their home directory:
   `userdel -r junioradmin`

## Success Criteria
You have successfully completed this practice if you were able to create a user, grant them `sudo` access, successfully read `/etc/shadow` as that user, and cleanly delete the account afterward.
