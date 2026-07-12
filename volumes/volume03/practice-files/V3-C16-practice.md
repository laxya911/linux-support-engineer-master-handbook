# Practice Guide: Chapter 16 (Volume 3)

## Objective
To install the Samba daemon, configure a Public read/write share, and test the connection locally using the `smbclient` utility.

## Assignment 1: Installation and Preparation
We must install the service and create the directory we want to share.

1. Install Samba and the client tools:
   * **Ubuntu/Debian:** `sudo apt update && sudo apt install samba smbclient`
   * **RHEL/CentOS:** `sudo dnf install samba samba-client`
2. Create a folder to act as our shared drive:
   `sudo mkdir -p /var/shares/public`
3. Because this is a "Public" guest share, we must grant the Linux `nobody` user (which Samba uses for guests) permission to write to it:
   `sudo chmod 777 /var/shares/public`

## Assignment 2: The Configuration
Now we must tell Samba about this directory.

1. Open the main Samba configuration file:
   `sudo nano /etc/samba/smb.conf`
2. Scroll to the absolute bottom of the file, and define your new share by pasting this block:
   ```text
   [Public]
      comment = Our Public Test Share
      path = /var/shares/public
      browseable = yes
      read only = no
      guest ok = yes
   ```
3. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).
4. Restart the Samba daemon to apply the changes:
   `sudo systemctl restart smbd` (Ubuntu) OR `sudo systemctl restart smb` (RHEL)

## Assignment 3: The Connection
Let's pretend we are a Windows user connecting from across the network. We will use `smbclient` to simulate this.

1. Connect to the local share as an anonymous guest (`-U %` means no password):
   `smbclient //localhost/Public -U %`
2. **Observation:** Your terminal prompt will change to `smb: \>`. You are now connected to the share via the SMB protocol!
3. Create a test file on the share using the `put` command (we will just upload our `.bashrc` file as a test):
   `put .bashrc test_upload.txt`
4. Verify the file uploaded successfully:
   `ls`
5. Exit the SMB prompt:
   `exit`

## Assignment 4: The Proof
Did the file actually get written to the physical Linux hard drive?

1. Look inside the directory we created in Assignment 1:
   `ls -l /var/shares/public`
2. **Result:** You will see `test_upload.txt` sitting on the physical disk! Samba successfully translated the SMB network request into a standard Linux file write!

## Success Criteria
You have successfully completed this practice if you installed Samba, configured a `[Public]` block in `smb.conf`, connected using `smbclient`, and successfully uploaded a file via the protocol.
