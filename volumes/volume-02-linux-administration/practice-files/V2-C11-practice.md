# Practice Guide: Chapter 11 (Volume 2)

## Objective
To safely configure and enable the Uncomplicated Firewall (UFW) without locking yourself out of your VM.

## Assignment 1: The Safety Check
Before doing anything, we must secure our lifeline (SSH).

1. Check the current status of the firewall:
   `sudo ufw status`
   *(It will likely say `inactive`).*
2. **CRITICAL STEP:** Tell the firewall to allow SSH traffic:
   `sudo ufw allow ssh`
3. **Observation:** You should receive a `Rules updated` confirmation.

## Assignment 2: Enabling the Firewall
Now that SSH is safe, we can turn the firewall on.

1. Enable UFW:
   `sudo ufw enable`
2. **Observation:** You will receive the warning: `Command may disrupt existing ssh connections. Proceed with operation (y|n)?`. Because we performed Assignment 1, we know we are safe. Press `y` and `ENTER`.
3. Check the status again:
   `sudo ufw status numbered`
4. **Result:** You should see that UFW is `active` and that Port 22 (SSH) is explicitly `ALLOW`ed from `Anywhere`.

## Assignment 3: Adding and Deleting Rules
Let's practice opening a port for a web server, and then deleting that rule.

1. Allow HTTP traffic (Port 80):
   `sudo ufw allow 80/tcp`
2. Check the numbered status list again:
   `sudo ufw status numbered`
3. **Observation:** Notice that the rule for Port 80 has a number next to it (likely `[ 3]`).
4. Delete the rule using its number (replace `3` with your actual number):
   `sudo ufw delete 3`
5. Press `y` to confirm the deletion.

## Success Criteria
You have successfully completed this practice if you enabled UFW, verified that Port 22 is explicitly allowed, and practiced adding and deleting a rule using `ufw status numbered`.
