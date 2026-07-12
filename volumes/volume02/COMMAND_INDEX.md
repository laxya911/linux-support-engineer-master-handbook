# Command Index: Volume 2 (Linux System Administration)

This is a comprehensive index of the primary CLI tools and commands introduced in Volume 2.

### Core Administration
* `systemctl` - Control the systemd system and service manager.
* `journalctl` - Query the systemd journal logs.
* `chattr` - Change file attributes on a Linux file system (e.g., immutability).
* `lsattr` - List file attributes on a Linux second extended file system.
* `setfacl` - Set file access control lists (ACLs).
* `getfacl` - Get file access control lists (ACLs).
* `usermod` - Modify a user account.
* `chage` - Change user password expiry information.

### Process & Memory Management
* `top` - Display Linux processes (dynamic real-time view).
* `htop` - Interactive process viewer.
* `ps` - Report a snapshot of the current processes.
* `kill` - Send a signal to a process (e.g., SIGTERM, SIGKILL).
* `killall` - Kill processes by name.
* `pkill` - Look up or signal processes based on name and other attributes.
* `free` - Display amount of free and used memory in the system.
* `vmstat` - Report virtual memory statistics.

### Networking
* `ip` - Show / manipulate routing, network devices, interfaces, and tunnels.
* `ss` - Another utility to investigate sockets.
* `netstat` - Print network connections, routing tables, interface statistics.
* `iptables` - Administration tool for IPv4 packet filtering and NAT.
* `nft` - Command line tool for nftables (firewall).
* `ping` - Send ICMP ECHO_REQUEST to network hosts.
* `traceroute` - Print the route packets trace to network host.

### Storage & LVM
* `lsblk` - List block devices.
* `blkid` - Locate/print block device attributes.
* `pvcreate` / `pvdisplay` - Manage Physical Volumes.
* `vgcreate` / `vgdisplay` / `vgextend` - Manage Volume Groups.
* `lvcreate` / `lvdisplay` / `lvextend` - Manage Logical Volumes.
* `resize2fs` - Resize ext2/ext3/ext4 file systems.
* `xfs_growfs` - Expand an XFS filesystem.
* `mount` / `umount` - Mount and unmount filesystems.

### Backup & Sync
* `rsync` - A fast, versatile, remote (and local) file-copying tool.
* `tar` - An archiving utility.

### Performance Profiling
* `strace` - Trace system calls and signals.
* `lsof` - List open files.
* `iostat` - Report Central Processing Unit (CPU) statistics and input/output statistics for devices and partitions.
* `dmesg` - Print or control the kernel ring buffer.
