# Practice Guide: Chapter 3 (Volume 2)

## Objective
To understand the difference between querying local files (`/etc/passwd`) and querying the entire authentication database using `getent`.

## Assignment 1: Local vs. Global Queries
When you look at the `/etc/passwd` file, you are *only* seeing local users. If a Linux server is joined to an Active Directory domain, the domain users will NOT appear in the `/etc/passwd` file!

To query all users (both local and Active Directory), you must use the `getent` command. `getent` asks the system (and SSSD) for the complete list.

1. First, search the local password file for your user:
   `grep $USER /etc/passwd`
   *(This searches the physical file on the hard drive).*
2. Next, search the global database for your user:
   `getent passwd $USER`
   *(This asks the operating system to query all known authentication sources).*

## Assignment 2: The SSSD Config Check
If you are ever dropped onto a server and need to know if it is connected to Windows Active Directory, you should check the SSSD configuration file.

1. Try to view the SSSD configuration:
   `sudo cat /etc/sssd/sssd.conf`
2. **Result:** If your practice VM is not joined to a domain, this file will not exist (or the directory won't exist). 
3. **Real-World Context:** In a production environment, if this file exists, you will see lines like `id_provider = ad`, which instantly tells you the Linux server is bridging to Windows Active Directory!

## Success Criteria
You have successfully completed this practice if you understand that `cat /etc/passwd` only shows local users, while `getent passwd` will show both local users and remote LDAP/Active Directory users.
