# Practice Guide: Chapter 20 (Capstone Project)

## Mission Briefing
You have just been hired as the sole Linux Support Engineer for a startup. On your first day, the CEO hands you the keys to their only production server. 
"It's completely broken," the CEO says. "The previous admin made a bunch of changes on a Friday night and then quit. We need the web server online, secured, and backed up by noon."

## Phase 1: The Boot Loop (Storage)
**The Symptom:** You attempt to boot the VM, but it drops into "Emergency Mode" and fails to load the OS. 
**The Objective:**
* Recall Chapter 6: What file dictates how disks are mounted on boot?
* Access the emergency console, find the typo in that file, and fix it so the server can boot normally.

## Phase 2: The Network Blackout (Networking)
**The Symptom:** The server boots, but you cannot SSH into it. 
**The Objective:**
* Recall Chapter 8 and 9: How are static IPs assigned, and how does traffic leave the subnet?
* Log in via the Cloud Provider's virtual console.
* Check the IP address (`ip a`) and the routing table (`ip route`).
* You will discover the Default Gateway is missing from the Netplan/NetworkManager configuration. Fix it so the server can ping `8.8.8.8`.

## Phase 3: The Security Lockout (Hardening)
**The Symptom:** The server is online, but you *still* cannot SSH into it. It prompts for a password, but the CEO gave you an SSH Key (`id_ed25519`). 
**The Objective:**
* Recall Chapter 12: Why is the server prompting for a password when you have a key?
* Investigate the `~/.ssh/authorized_keys` file on the server. You will find it has `777` permissions. 
* Fix the permissions to satisfy SSH paranoia.
* Edit `/etc/ssh/sshd_config` to explicitly disable `PasswordAuthentication`.

## Phase 4: The Storage Crisis (LVM)
**The Symptom:** You start the web server (`systemctl start nginx`), but it crashes immediately, complaining there is no disk space.
**The Objective:**
* Recall Chapter 4: How does LVM work?
* Run `df -h` and confirm the `/var/www` partition is 100% full.
* Run `vgs` and confirm there is 50GB of free space remaining in the Volume Group.
* Use `lvextend -r` to dynamically expand the web partition without rebooting the server.
* Restart Nginx.

## Phase 5: The Automation Guarantee (Operations)
**The Business Requirement:** The CEO demands that the website data is backed up every night at 2:00 AM, and that the server actively blocks automated hackers.
**The Objective:**
* Recall Chapter 13: Install and configure `fail2ban` to protect the SSH service.
* Recall Chapters 16, 17, and 18: Write a Bash script (`/opt/backup.sh`).
* The script must use `rsync -avz` to copy the `/var/www/html` directory to a `/backups` directory.
* The script must use `set -e` to fail fast, and utilize an Exit Code check to send a success/failure message to a log file.
* Use `crontab -e` to schedule this script to run at `0 2 * * *`.

## Success Criteria
You pass the Capstone Project if:
1. The server boots without errors.
2. You can SSH into the server using a cryptographic key (and passwords are disabled).
3. The LVM partition has been successfully expanded.
4. `fail2ban` is actively monitoring your authentication logs.
5. `cron` successfully executes your `rsync` backup script at 2:00 AM. 

Congratulations, Engineer. You are ready.
