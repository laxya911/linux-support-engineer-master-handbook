# Practice Guide: Chapter 15 (Volume 4)

## Objective
To configure the Linux `auditd` daemon to actively monitor the `/etc/shadow` file (which contains user password hashes) and generate an alert whenever it is read or modified.

## Assignment 1: Installation and Status
`auditd` is standard on most enterprise Linux distributions, but we will ensure it is installed.

1. **Ubuntu:**
   `sudo apt update && sudo apt install auditd audispd-plugins`
2. **RHEL/CentOS:**
   `sudo dnf install audit`
3. Verify the daemon is running:
   `sudo systemctl status auditd`

## Assignment 2: Creating a Watch Rule
We will use the `auditctl` command to dynamically add a rule to the running kernel.

1. Add a "watch" (`-w`) on the `/etc/shadow` file. We want to log any time the file is read (`r`), written to (`w`), executed (`x`), or has its attributes changed (`a`). Finally, we attach a custom key (`-k`) named `shadow_file_access` so we can easily search for this event later in the logs:
   `sudo auditctl -w /etc/shadow -p rwxa -k shadow_file_access`
2. Verify the rule was successfully added to the kernel:
   `sudo auditctl -l`

## Assignment 3: Triggering the Rule
Now, we will act like a malicious user (or a nosy application) trying to read the password hashes.

1. Attempt to view the shadow file. (This will fail if you aren't root, but the *attempt* will still be logged!):
   `cat /etc/shadow`
2. Run a command that requires reading the shadow file (like attempting to change your own password, or just using `sudo`):
   `sudo cat /etc/shadow`

## Assignment 4: Forensic Analysis
We will use the `ausearch` tool to parse the massive `/var/log/audit/audit.log` file and find our specific event.

1. Search the audit logs for our custom key:
   `sudo ausearch -k shadow_file_access`
2. **Observation:** You will see a block of text detailing the event. Look closely at the fields!
   * `time->`: The exact timestamp.
   * `syscall=openat` or `syscall=read`: The kernel system call that was executed.
   * `success=yes` (or `no`): Did the hacker actually get the data, or were they blocked by permissions?
   * `exe="/usr/bin/cat"`: The exact binary the attacker used to access the file.
   * `auid=1000`: The Audit User ID. Even if the user ran `sudo` to become root (UID 0), `auditd` tracks their original `auid`, proving exactly which human was behind the keyboard!

## Assignment 5: Cleanup
1. Remove the dynamic rule from the kernel:
   `sudo auditctl -W /etc/shadow -p rwxa -k shadow_file_access`

## Success Criteria
You have successfully completed this practice if you added a watch rule to `auditd`, triggered an access event, and successfully parsed the logs using `ausearch` to identify the `auid` of the user who touched the file.
