# Practice Guide: Chapter 2 (Volume 2)

## Objective
To safely inspect the `/etc/pam.d/` directory and learn how to read modular authentication files. 

*(Note: We will not be editing these files. Breaking a PAM configuration file will instantly lock you out of your server permanently!).*

## Assignment 1: Exploring the PAM Directory
Let's look at how many services rely on PAM.

1. List the contents of the PAM directory:
   `ls -l /etc/pam.d/`
2. **Observation:** You should see files for `sshd` (remote logins), `sudo` (privilege escalation), `login` (local console logins), and `su` (switching users). 

## Assignment 2: Reading the Sudo PAM Stack
Let's see exactly what happens when you type the `sudo` command.

1. Open the file in a safe, read-only mode using `cat` or `less`:
   `cat /etc/pam.d/sudo`
2. Look at the lines that do not have a `#` (comment) symbol in front of them.
3. You will likely see a line that looks like this:
   `@include common-auth`
4. **Observation:** This means that the `sudo` file doesn't actually contain the password checking logic. It simply "includes" a generic file called `common-auth`. This is the beauty of PAM—modularity! If you add Fingerprint scanning to `common-auth`, every service that includes it (like `sudo`, `login`, and `sshd`) instantly gets Fingerprint scanning.

## Assignment 3: Reading the Common Password Logic
Let's look at the rules for changing passwords.

1. Open the common password file:
   `cat /etc/pam.d/common-password` (On Ubuntu/Debian)
   *(If you are on RHEL/CentOS, check `cat /etc/pam.d/system-auth` instead).*
2. Look for the `password` management group lines.
3. You will likely see references to `pam_pwquality.so` or `pam_cracklib.so`.
4. **Observation:** These are the modules that reject your password if it is too short, or if it is a dictionary word! 

## Success Criteria
You have successfully completed this practice if you successfully navigated the `/etc/pam.d/` directory and identified the modular `@include` structure that allows PAM to apply universal authentication rules across multiple applications.
