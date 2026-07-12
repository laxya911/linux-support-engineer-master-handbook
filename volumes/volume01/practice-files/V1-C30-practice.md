# Practice Guide: Chapter 30

## Objective
To perform a self-assessment of the critical skills learned in Volume 1.

## Assignment 1: The Command Line Checklist
You do not need to type these commands. Just read them. If you cannot explain what these commands do, you must review the corresponding chapter before moving to Volume 2.

1. **Navigation (Chapter 4 & 5)**
   * `cd /var/log`
   * `ls -la`
   * `pwd`
2. **Permissions (Chapter 9)**
   * `chmod 755 script.sh`
   * `chown root:root config.txt`
3. **Services & Logs (Chapter 11 & 12)**
   * `systemctl restart sshd`
   * `systemctl enable nginx`
   * `journalctl -u mysql`
   * `tail -f /var/log/syslog`
4. **Networking (Chapter 14, 24, 25)**
   * `ip a`
   * `ping 8.8.8.8`
   * `ss -tulpn`
   * `ufw allow 22/tcp` (or `firewall-cmd --add-port=22/tcp --permanent`)
5. **Diagnostics (Chapter 17, 23, 26)**
   * `df -h`
   * `uptime`
   * `free -h`
   * `top`
   * `systemctl --failed`

## Assignment 2: The Cleanup
Over the last 29 chapters, you have created many fake files, fake users, and fake scripts on your practice Virtual Machine. 

You have two choices:
1. **The Engineer's Choice**: Keep the VM as it is. It is now a customized, messy, real-world server. This is the exact type of server you will inherit from customers in the real world.
2. **The Clean Slate**: Destroy your Virtual Machine and spin up a brand new, fresh instance of Ubuntu or RHEL to use for Volume 2.

## Success Criteria
You have successfully completed this practice—and Volume 1—if you can confidently define the commands in the checklist above. Congratulations!
