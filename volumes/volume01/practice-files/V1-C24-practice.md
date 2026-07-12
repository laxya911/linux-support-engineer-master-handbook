# Practice Guide: Chapter 24

## Objective
To safely view and manage the active firewall rules on your virtual machine.

> [!WARNING]  
> **READ CAREFULLY:** If you are connected to your VM via SSH, you must complete Step 2 perfectly. If you enable the firewall without allowing Port 22, you will disconnect yourself and lose access to the VM.

## Assignment (Ubuntu / Debian Users)
If you are using Ubuntu, follow these instructions to use `ufw`.

1. Check the current status:
   `sudo ufw status`
   *(It will likely say "Status: inactive").*
2. **CRITICAL STEP:** explicitly allow SSH traffic so you don't lock yourself out.
   `sudo ufw allow 22/tcp`
3. Let's pretend you are running a web server. Allow HTTP traffic:
   `sudo ufw allow 80/tcp`
4. Turn the firewall on:
   `sudo ufw enable`
   *(Press 'y' if it warns you about disrupting existing SSH connections).*
5. Check the status again:
   `sudo ufw status`
   *(You should now see the rules actively applied!).*

## Assignment (CentOS / RHEL / Rocky Users)
If you are using a Red Hat derivative, follow these instructions to use `firewalld`.

1. Check the current state:
   `sudo firewall-cmd --state`
   *(It should say "running").*
2. View your current rules:
   `sudo firewall-cmd --list-all`
   *(Notice that under the "services" line, "ssh" is likely already permitted by default).*
3. Let's pretend you are running a web server. Permanently open Port 80:
   `sudo firewall-cmd --add-port=80/tcp --permanent`
4. Notice that if you run `--list-all` again, Port 80 is NOT there. You must reload the firewall to pull the permanent rule from the disk into active memory:
   `sudo firewall-cmd --reload`
5. Check your rules one last time:
   `sudo firewall-cmd --list-all`
   *(Look under the "ports" line. You should now see `80/tcp`).*

## Success Criteria
You have successfully completed this practice if you identified your distro's firewall, successfully added Port 80, and successfully viewed the active ruleset to confirm the port is open.
