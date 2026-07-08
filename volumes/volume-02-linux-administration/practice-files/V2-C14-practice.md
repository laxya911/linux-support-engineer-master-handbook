# Practice Guide: Chapter 14 (Volume 2)

## Objective
To discover which Mandatory Access Control system your VM is running and practice viewing hidden security labels.

## Assignment 1: Identifying the MAC System
Ubuntu defaults to AppArmor. RHEL defaults to SELinux. Let's ask your server what it is running.

1. Try to run the SELinux status command:
   `sestatus`
2. Try to run the AppArmor status command:
   `sudo aa-status`
3. **Result:** Only one of these commands will succeed. 
   * If `sestatus` prints output, you are on an SELinux system (likely RHEL/CentOS).
   * If `aa-status` prints output, you are on an AppArmor system (likely Ubuntu/Debian).

## Assignment 2: The Secret `-Z` Flag
If you are running SELinux, every file has a hidden "Security Context" label. You can view these labels by appending a capital `Z` to your normal commands.

*(Note: If your system runs AppArmor, this flag will still work, but the output will simply say `?` or `unconfined` because AppArmor doesn't use file labels).*

1. Run a normal directory listing of your home folder:
   `ls -l /`
2. Now run it with the Z flag:
   `ls -lZ /`
3. **Observation:** Notice the massive extra column of text! You will see labels like `system_u:object_r:etc_t:s0`. This is the exact string that SELinux evaluates when deciding if an application is allowed to touch a file. 

## Assignment 3: Process Contexts
The `-Z` flag works for processes too! Let's look at the labels assigned to your running programs.

1. Run the process status command with the Z flag:
   `ps auxZ`
2. **Observation:** Look at the far left column. You will see the security context that each program is trapped inside. If an attacker compromises a program, they are trapped inside that same label!

## Success Criteria
You have successfully completed this practice if you successfully identified whether your VM uses AppArmor or SELinux, and you successfully used the `ls -lZ` command to view hidden security contexts.
