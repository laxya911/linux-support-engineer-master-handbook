# Practice Guide: Chapter 15

## Objective
To generate a cryptographic keypair, observe the keys locally, and harden the SSH daemon by disabling root login.

## Assignment 1: Generating the Keys
Usually, you do this on your laptop, but for this lab, we will generate them directly on the VM.

1. Open a terminal on your virtual machine.
2. Run the key generator:
   `ssh-keygen -t rsa -b 4096`
3. It will ask where to save the file. Press **Enter** to accept the default (`/home/username/.ssh/id_rsa`).
4. It will ask for a passphrase. Leave it blank for this lab and press **Enter** twice.
5. Your keys are generated.

## Assignment 2: Inspecting the Keys
1. Use `ls -l` to view the hidden `.ssh` directory:
   `ls -l ~/.ssh/`
2. You will see two files:
   * `id_rsa` (Your Private Key. Note the permissions are `600` so nobody else can read it).
   * `id_rsa.pub` (Your Public Key. Permissions are `644`).
3. Use `cat` to view your Public Key:
   `cat ~/.ssh/id_rsa.pub`
   *(It will be a massive string of random characters ending with your username).*

## Assignment 3: Hardening the Server
Let's lock down the SSH daemon so it no longer accepts direct `root` logins.

1. Open the daemon configuration file using `sudo`:
   *Ubuntu/RHEL:* `sudo nano /etc/ssh/sshd_config`
2. Scroll down until you find the line that says `PermitRootLogin`. It may be commented out with a `#`, or it might say `yes` or `prohibit-password`.
3. Change the line to look exactly like this (ensure there is no `#` at the beginning):
   `PermitRootLogin no`
4. Save the file and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).
5. Restart the SSH daemon to apply the changes:
   *Ubuntu:* `sudo systemctl restart ssh`
   *RHEL:* `sudo systemctl restart sshd`

## Success Criteria
You have successfully completed this practice if you generated an RSA keypair, verified the restrictive `600` permissions on your private key, modified `sshd_config`, and restarted the daemon.
