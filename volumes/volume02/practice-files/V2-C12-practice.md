# Practice Guide: Chapter 12 (Volume 2)

## Objective
To generate a modern SSH keypair and inspect the master SSH configuration file.

## Assignment 1: Generating the Keys
Historically, engineers generated RSA keys. Today, the modern standard for speed and security is the Elliptic Curve `ed25519` algorithm.

1. Generate a new keypair on your VM:
   `ssh-keygen -t ed25519 -C "practice_key"`
2. Press `ENTER` to accept the default file location (`/home/user/.ssh/id_ed25519`).
3. Press `ENTER` twice to skip creating a passphrase (for the sake of this practice lab).
4. List the contents of your `.ssh` directory to prove the files were created:
   `ls -la ~/.ssh/`
5. **Observation:** You will see the Private Key (`id_ed25519`) and the Public Key (`id_ed25519.pub`). Notice that the Private Key has stricter permissions!

## Assignment 2: Inspecting the Padlock
Let's look at the Public Key you just generated. This is the text you would safely paste onto other servers to grant yourself access.

1. Output the contents of the Public Key:
   `cat ~/.ssh/id_ed25519.pub`
2. **Result:** You will see a long string of random text ending in `"practice_key"`. This text is completely safe to share. 

## Assignment 3: The Master Configuration
Let's look at how the cloud provider hardened your VM before they handed it to you.

1. View the SSH daemon configuration file:
   `cat /etc/ssh/sshd_config`
2. Look for the `PermitRootLogin` setting. 
3. Look for the `PasswordAuthentication` setting.
4. **Observation:** Because you are using a modern cloud VM, the provider has almost certainly already set `PasswordAuthentication no` to protect you from automated botnets!

## Success Criteria
You have successfully completed this practice if you generated an `ed25519` keypair, safely viewed your Public Key, and located the security settings inside the `sshd_config` file.
