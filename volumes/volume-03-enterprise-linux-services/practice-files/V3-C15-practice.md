# Practice Guide: Chapter 15 (Volume 3)

## Objective
To install the WireGuard tools and generate the Cryptographic Keypair required to establish a secure tunnel.

## Assignment 1: Installation
We just need the command-line tools to generate the keys.

1. Install the WireGuard tools:
   * **Ubuntu/Debian:** `sudo apt update && sudo apt install wireguard-tools`
   * **RHEL/CentOS:** `sudo dnf install wireguard-tools`

## Assignment 2: Generating the Keys
WireGuard uses the exact same Public/Private key concept as SSH. Let's create the keys for a theoretical "Client Laptop".

1. First, we generate the Private Key (the secret you never share):
   `wg genkey > private.key`
2. Next, we feed the Private Key back into the `wg pubkey` command to mathematically derive the matching Public Key:
   `cat private.key | wg pubkey > public.key`
3. View the Private Key:
   `cat private.key`
   *(It will look like a random string of 44 characters, ending in an '=' sign).*
4. View the Public Key:
   `cat public.key`

## Assignment 3: Conceptual Configuration
If you were actually setting up this VPN, what would you do with these keys?

1. **The Private Key** stays on the employee's laptop. It is entered into their WireGuard application. If this key is stolen, the hacker can impersonate the employee.
2. **The Public Key** is emailed to the Support Engineer. The engineer opens the Linux Server's configuration file (`/etc/wireguard/wg0.conf`) and adds it under a `[Peer]` block, like this:
   ```text
   [Peer]
   PublicKey = <paste_public_key_here>
   AllowedIPs = 10.8.0.2/32
   ```
3. Now, whenever the server receives traffic mathematically signed by the Private Key, it knows the traffic is legitimately coming from that specific employee!

## Success Criteria
You have successfully completed this practice if you installed the WireGuard tools and successfully generated a matching cryptographic keypair.
