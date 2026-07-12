# Practice Guide: Chapter 8 (Volume 2)

## Objective
To safely inspect the network interfaces of your practice VM without modifying them. 

*(Note: We will not be editing the IP address of your practice VM. Because your VM is hosted in the cloud, changing its IP address will instantly and permanently sever your SSH connection!)*

## Assignment 1: Finding Your IP and MAC Address
The first step in any networking ticket is mapping out the physical (or virtual) network cards.

1. Run the IP address command:
   `ip a`
2. **Observation:** 
   * Interface `lo` is your loopback interface (127.0.0.1). You can ignore it.
   * Look for your primary interface (usually named `eth0`, `ens33`, or `enp0s3`).
   * Find the word `inet`. The number next to it is your server's IPv4 address.
   * Find the word `link/ether`. The 6-part hexadecimal number next to it is your MAC Address (the physical hardware address of the network card).

## Assignment 2: Viewing the Configuration
Let's see how your specific Linux distribution is generating that IP address.

**If you are on Ubuntu:**
1. Look inside the Netplan directory:
   `ls /etc/netplan/`
2. Read the YAML file you found (e.g., `cat /etc/netplan/50-cloud-init.yaml`).
3. **Result:** You will likely see `dhcp4: true`. This means the Cloud Provider is automatically assigning your VM its public IP address via DHCP. 

**If you are on RHEL/CentOS:**
1. Use the NetworkManager command line tool to view active connections:
   `nmcli con show`
2. View the specific settings for your primary interface (replace `eth0` with your interface name):
   `nmcli con show eth0`
3. **Result:** This will output a massive list of settings determining how your server connects to the network.

## Success Criteria
You have successfully completed this practice if you used `ip a` to locate your server's IPv4 address and its physical MAC address, and located the configuration file that controls it.
