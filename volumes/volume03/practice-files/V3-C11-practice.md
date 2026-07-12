# Practice Guide: Chapter 11 (Volume 3)

## Objective
To master the `dig` utility to query DNS records, bypass local caches, and inspect the Time-To-Live (TTL).

## Assignment 1: Basic Resolution
Let's see how your VM resolves standard websites.

1. Install the DNS utilities if you don't have them:
   * **Ubuntu:** `sudo apt install dnsutils`
   * **RHEL:** `sudo dnf install bind-utils`
2. Query the A Record for a common website:
   `dig google.com`
3. **Observation:** Look at the `ANSWER SECTION`. You will see `google.com.`, a number (the TTL), `IN A`, and the IPv4 address.
4. Run the exact same command again immediately:
   `dig google.com`
5. **Observation:** Look at the TTL number. It has decreased! Your local DNS resolver is counting down the seconds until it clears its cache.

## Assignment 2: Finding Mail Servers
Let's find out who handles email for a company.

1. Query the MX (Mail Exchange) records for Microsoft:
   `dig MX microsoft.com`
2. **Observation:** The ANSWER section will list servers like `microsoft-com.mail.protection.outlook.com`. This is how an email from your server knows where to go when you send an email to `bill@microsoft.com`.

## Assignment 3: Bypassing the Cache
Let's pretend your local router is giving you a bad, cached IP address. We can ask a different server for a second opinion.

1. Query Cloudflare's public DNS server (`1.1.1.1`):
   `dig @1.1.1.1 amazon.com`
2. Query Google's public DNS server (`8.8.8.8`):
   `dig @8.8.8.8 amazon.com`
3. **Observation:** By using the `@` symbol, you force `dig` to ignore your local `/etc/resolv.conf` and speak directly to a specific server over Port 53.

## Assignment 4: Finding the Authoritative Server
Who actually owns the records for `netflix.com`?

1. Query the NS (Name Server) records for Netflix:
   `dig NS netflix.com`
2. **Observation:** You will see a list of Amazon Route53 (`awsdns`) servers. Netflix pays AWS to act as their Authoritative DNS provider!

## Success Criteria
You have successfully completed this practice if you used `dig` to find an A record, watched a TTL count down, requested an MX record, and bypassed your local resolver by querying `8.8.8.8` directly.
