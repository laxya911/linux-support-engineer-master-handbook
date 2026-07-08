# Practice Guide: Chapter 25

## Objective
To read your server's DNS configuration, and to execute the "Override Trick" by hijacking a fake domain name.

## Assignment 1: The Global Resolver
Let's see who your virtual machine asks for directions.

1. Output the contents of the resolver file:
   `cat /etc/resolv.conf`
2. Look at the lines starting with `nameserver`.
   *(If you are running this VM on a home network or cloud provider, it will likely point to your home router like `192.168.1.1` or a cloud DNS server like `127.0.0.53`).*
3. Verify global DNS is working:
   `ping -c 2 google.com`

## Assignment 2: The Override Trick
We are going to make up a completely fake domain name that doesn't exist on the internet, and force our VM to resolve it.

1. Try to ping a completely fake domain:
   `ping -c 2 super-secret-internal-server.local`
2. **Result:** It should fail instantly with a `Name or service not known` error. Global DNS has no idea what that is.
3. Open the hosts file as root:
   `sudo nano /etc/hosts`
4. Add the following line to the bottom of the file (pointing the fake name to Google's public IP):
   `8.8.8.8 super-secret-internal-server.local`
5. Save and exit the file.
6. Try to ping the fake domain again:
   `ping -c 2 super-secret-internal-server.local`
7. **Result:** It works! Your ping succeeds, and the terminal explicitly shows that it is sending the packets to `8.8.8.8`.

## Assignment 3: The Cleanup
1. Open the file again:
   `sudo nano /etc/hosts`
2. Delete the fake entry you just added so it doesn't cause confusion later.
3. Save and exit.

## Success Criteria
You have successfully completed this practice if you observed your default nameservers, proved a fake domain couldn't be resolved, added it to `/etc/hosts`, and successfully hijacked the name resolution to point to a valid IP address.
