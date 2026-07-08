# Practice Guide: Chapter 6

## Objective
To develop muscle memory for file manipulation and understand the behavior of symbolic links.

## Assignment 1: Directory Scaffolding
In Linux, you often have to manually create the directory structure for new applications.

1. Navigate to your home directory (`cd ~`).
2. Run the following command to create a nested directory structure in one shot:
   `mkdir -p test-app/logs test-app/config`
3. Navigate into the `test-app/config` directory.
4. Use `touch app.conf` to create an empty configuration file.

## Assignment 2: The Broken Symlink
1. While still inside `test-app/config`, type `pwd` and note your absolute path (e.g., `/home/username/test-app/config`).
2. Navigate to the `/tmp` directory (`cd /tmp`).
3. Create a symbolic link pointing back to your configuration file:
   `ln -s /home/username/test-app/config/app.conf my_shortcut.conf`
   *(Replace 'username' with your actual username)*
4. Type `ls -l my_shortcut.conf`. You should see it pointing to the target file.
5. Now, navigate back to your home directory, and delete the original file:
   `rm ~/test-app/config/app.conf`
6. Return to `/tmp` and try to read the shortcut using `cat my_shortcut.conf`.

*What error did you receive? This is what a "broken symlink" looks like in production.*

## Assignment 3: Live Log Monitoring
1. Run this command to watch your system logs in real-time:
   * **Debian/Ubuntu 26.04**: `tail -f /var/log/syslog`
   * **RHEL 10 / CentOS**: `tail -f /var/log/messages`
2. Open a *second* terminal window (or SSH session) into your VM.
3. In the second terminal, run this command to generate a fake error log:
   `logger "EMERGENCY: The warp core is failing!"`
4. Look back at your first terminal. You should see the message instantly appear at the bottom of the log stream.
5. Press `Ctrl + C` in the first terminal to exit `tail`.

## Success Criteria
You have successfully completed this practice if you were able to create a nested directory structure, intentionally break a symbolic link, and observe a real-time log injection using `tail -f`.
