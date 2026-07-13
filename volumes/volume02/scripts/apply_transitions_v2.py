import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(os.path.dirname(script_dir), "chapters")

transitions = {
    "V2-C01": "You now have administrative access, but how do you verify who is logging in? It's time to explore Pluggable Authentication Modules.",
    "V2-C02": "Local authentication is fine for one server, but what happens when you have a thousand? You need a central authority.",
    "V2-C03": "With users authenticated, we must give them storage. But physical partitions are inflexible. We need a dynamic solution.",
    "V2-C04": "Logical volumes give us flexibility, but what happens when the underlying physical disk dies? We need hardware redundancy.",
    "V2-C05": "In this chapter, you learned how to protect data stored on local disks. But what happens when the storage isn't local anymore?",
    "V2-C06": "We have storage connected over the network, but how do we optimize the filesystem itself to handle millions of tiny files?",
    "V2-C07": "To connect to external storage and users, the server must exist on a network. We must master IP configuration.",
    "V2-C08": "A static IP gets you on the local network, but how do you reach the outside world? We need to understand routing.",
    "V2-C09": "When routing fails and packets disappear, how do you prove it's the network and not the application? You must capture the packets.",
    "V2-C10": "Now that we can see every packet, how do we block the malicious ones? We need to build a firewall.",
    "V2-C11": "Firewalls block external ports, but attackers will try to break through the front door via SSH. We must harden it.",
    "V2-C12": "SSH keys are secure, but what about brute force attacks on other services? We need automated intrusion prevention.",
    "V2-C13": "Even with the perimeter secured, what happens if an attacker compromises a web application? We need Mandatory Access Control.",
    "V2-C14": "With SELinux enforcing policies, how do we track exactly what users and processes are doing? We must audit the system.",
    "V2-C15": "Monitoring and auditing generate massive amounts of data and routine tasks. It's time to script our operations with Bash.",
    "V2-C16": "Scripts are powerful, but they shouldn't require manual execution. We need the server to run them on a schedule.",
    "V2-C17": "Automated tasks are great, but the most important scheduled task of all is protecting our data. We need automated backups.",
    "V2-C18": "You have backups, but what do you do when a real disaster strikes? You need a forensic incident response methodology.",
    "V2-C19": "Incidents are resolved, but how do we handle massive traffic spikes without going down again? We need an advanced web server.",
    "V2-C20": "The web tier is scaled, but the application is only as fast as its database. We must master database replication.",
    "V2-C21": "Managing complex dependencies across servers is a nightmare. What if we could package the application and its environment together?",
    "V2-C22": "Docker containers solve dependency issues, but how do you manage them in a production environment?",
    "V2-C23": "With containers, databases, and networks running together, failures become complex. We need a universal troubleshooting model.",
    "V2-C24": "You have the theory. You have the tools. Now, it's time for the ultimate test of your skills.",
    "V2-C25": "Congratulations on completing Volume 2. Next up: Volume 3 - Automation & Infrastructure."
}

mistakes_dict = {
    "V2-C01": ("Editing `/etc/sudoers` with `nano` instead of `visudo`, breaking syntax and locking everyone out.", "`chmod -R 777 /etc/` (What goes wrong? You destroy the strict permissions required by services like SSH and sudo, permanently breaking the system.)"),
    "V2-C02": ("Locking out `root` without having a secondary administrative backdoor open.", "`pam_tally2 --user admin` (Are you checking lockouts or resetting them? Know the flags!)"),
    "V2-C03": ("Relying entirely on remote authentication without a local fallback user for emergency access.", "`systemctl stop sssd` (If LDAP goes down, how will you log back in?)"),
    "V2-C04": ("Expanding a filesystem without expanding the underlying Logical Volume first.", "`lvremove /dev/vg0/data` (Are you sure the volume is unmounted and empty?)"),
    "V2-C05": ("Assuming RAID is a backup solution. It protects against hardware death, not human deletion.", "`mdadm --fail /dev/md0 /dev/sdb` (Did you verify `sdb` is the correct failing drive?)"),
    "V2-C06": ("Running `df -h` on a server with a disconnected NFS mount. It will hang indefinitely!", "`mount -a` (Are you sure your `/etc/fstab` syntax is correct?)"),
    "V2-C07": ("Running out of inodes because of millions of tiny cache files, even when disk space shows 50% free.", "`rm -rf /var/cache/*` (Will the application crash if the directory structure disappears?)"),
    "V2-C08": ("Forgetting to `netplan apply` after making changes, leaving the old config running in memory.", "`systemctl restart NetworkManager` (Are you connected via SSH? You might lose connection!)"),
    "V2-C09": ("Adding a static route but forgetting to make it persistent across reboots.", "`ip route del default` (How will your SSH packets get back to you?)"),
    "V2-C10": ("Capturing all traffic without filters, instantly filling up the local hard drive with a massive `.pcap` file.", "`tcpdump -w trace.pcap` (Did you forget to specify a filter?)"),
    "V2-C11": ("Enabling `ufw` without explicitly allowing port 22 first, instantly locking yourself out of SSH.", "`ufw enable` (Are you absolutely sure SSH is allowed?)"),
    "V2-C12": ("Disabling password authentication before verifying that your SSH keys actually work.", "`systemctl restart sshd` (Did you test the config with `sshd -t` first?)"),
    "V2-C13": ("Whitelisting `0.0.0.0/0` by accident or failing to whitelist the corporate office IP, resulting in mass lockouts.", "`fail2ban-client set sshd banip ...` (Did you just ban the CEO?)"),
    "V2-C14": ("Blindly running `setenforce 0` to 'fix' a permission issue instead of checking the audit logs.", "`restorecon -R /var/www/` (Will this overwrite custom contexts you manually set?)"),
    "V2-C15": ("Logging everything blindly without configuring log rotation, eventually crashing the server when `/var/log` fills up.", "`auditctl -D` (Did you just delete all active audit rules?)"),
    "V2-C16": ("Using variables without quotes (e.g., `rm -rf $DIR/`), which deletes the root directory if `$DIR` is empty!", "`for i in $(ls); do` (What happens if a filename contains a space?)"),
    "V2-C17": ("Assuming Cron scripts have the same `$PATH` environment variables as your interactive shell. They don't!", "`crontab -r` (Did you mean `crontab -e`? You just deleted all your jobs!)"),
    "V2-C18": ("Running `rsync` without the trailing slash on the source directory, accidentally nesting directories.", "`rsync --delete` (Are you absolutely sure you have the source and destination in the correct order?)"),
    "V2-C19": ("Rebooting a compromised server immediately, which destroys all volatile memory (RAM) evidence needed for forensics.", "`reboot` (Have you captured memory dumps and network connections first?)"),
    "V2-C20": ("Forgetting a trailing semicolon in the config, breaking the entire web cluster on reload.", "`nginx -s reload` (Did you run `nginx -t` to test the syntax first?)"),
    "V2-C21": ("Backing up the database without locking tables or using transactions, resulting in corrupted backups.", "`DROP DATABASE prod;` (Are you on the staging server or the production server?)"),
    "V2-C22": ("Treating a container like a VM and running SSH inside it, defeating the purpose of microservices.", "`docker kill $(docker ps -q)` (Did you mean to kill *all* running containers?)"),
    "V2-C23": ("Storing persistent data inside the container filesystem. When the container stops, the data is gone forever!", "`docker system prune -a` (Are you ready to redownload all those images?)"),
    "V2-C24": ("Assuming the application is broken when the DNS server is actually down. Always start at Layer 1!", "`ping 8.8.8.8` (If this works but `ping google.com` fails, what is the real issue?)"),
    "V2-C25": ("Rushing to fix symptoms without understanding the root cause, leading to cascading failures.", "`echo \"\" > /var/log/syslog` (Why are you deleting the logs before reading them?)"),
}

sops = {
    "V2-C01": {
        "title": "Syntax Error in /etc/sudoers",
        "triage": "Charlie confirms P1 impact: No administrators can execute privileged commands. SLA requires 15-minute response.",
        "discovery": "Charlie attempts `sudo -l` and immediately sees a parse error at line 25. He checks the audit log and sees Bob recently modified the file using nano instead of visudo.",
        "containment": "Since sudo is completely broken, standard operations are halted. Charlie announces a temporary freeze on administrative tasks while he restores access.",
        "resolution": "Charlie leverages an out-of-band management console to log in directly as root (which bypasses sudo). He uses `visudo` to correct the syntax error on line 25.",
        "verification": "Charlie logs back in as a standard user and runs `sudo -l`. The command succeeds.",
        "closure": "Charlie documents the fix: 'Corrected syntax in sudoers via root console'. Resolves the incident.",
        "followup": "Charlie updates the SOP to strictly require `visudo` for all future sudoers edits to prevent syntax lockouts.",
        "escalation": "If the root password was lost and out-of-band management was unavailable, Charlie would have escalated to the Data Center team to boot into Single User Mode."
    },
    "V2-C04": {
        "title": "Root Filesystem at 100% Capacity",
        "triage": "Charlie receives a P2 alert: `/` is at 100%. Web applications are failing to write temporary files. SLA requires 30-minute response.",
        "discovery": "Charlie runs `df -h` and confirms `/` is full. He runs `vgs` and sees 50GB of free space remaining in the Volume Group.",
        "containment": "Charlie clears out old `/var/log` archives to free up 500MB immediately, allowing the web apps to resume functioning while he executes the permanent fix.",
        "resolution": "Charlie uses `lvextend -L +10G /dev/vg0/root` to add 10GB from the VG to the LV, and then runs `resize2fs /dev/vg0/root` to expand the filesystem online.",
        "verification": "Charlie runs `df -h` and confirms `/` now shows 10GB of free space. Monitoring alerts clear.",
        "closure": "Charlie documents the LVM expansion and resolves the ticket.",
        "followup": "Charlie adjusts the monitoring thresholds to alert at 85% instead of 95% to allow more reaction time in the future.",
        "escalation": "If the VG had 0 free space, Charlie would escalate to the Storage team to provision a new physical LUN."
    },
    "V2-C07": {
        "title": "No Space Left on Device (Inodes)",
        "triage": "Charlie takes a P2 ticket: Users cannot upload profile pictures. Error: 'No space left on device'.",
        "discovery": "Charlie runs `df -h` and sees the disk is only 40% full. He remembers to check inodes and runs `df -i`. The inode usage is at 100%.",
        "containment": "Charlie identifies a misconfigured PHP session directory containing 5 million tiny session files. He stops the web service briefly to prevent more files from being created.",
        "resolution": "Charlie uses `find /var/lib/php/sessions -type f -delete` (after confirming it's safe) to purge the millions of files, freeing up the inodes.",
        "verification": "Charlie runs `df -i` and sees inode usage drop to 2%. He successfully uploads a test image.",
        "closure": "Charlie logs the root cause (inode exhaustion) and the cleanup command.",
        "followup": "Charlie creates a Cron job to automatically prune PHP session files older than 24 hours.",
        "escalation": "If the inodes were exhausted by legitimate files that could not be deleted, he would escalate to the OS team to format a new partition with a higher inode ratio."
    },
    "V2-C10": {
        "title": "Mysterious Network Latency",
        "triage": "Charlie receives a P3 ticket: The billing API is intermittently timing out when talking to the payment gateway.",
        "discovery": "Charlie runs a packet capture using `tcpdump -i eth0 host gateway.corp.local`. He analyzes the PCAP in Wireshark and notices a massive number of TCP Retransmissions.",
        "containment": "Charlie notifies the Billing team that transactions may be delayed and to hold off on bulk processing.",
        "resolution": "The packet capture proves the network switch is dropping packets. Charlie provides the PCAP to the Network Engineering team, who identify a faulty SFP module on the switch.",
        "verification": "After the Network team replaces the module, Charlie runs another `tcpdump` and confirms the TCP Retransmissions have stopped.",
        "closure": "Charlie attaches the PCAP analysis to the ticket and resolves it, crediting the Network team for the physical fix.",
        "followup": "Charlie writes a KB article on how to identify TCP Retransmissions using tcpdump.",
        "escalation": "Charlie correctly escalated to the Network team once he had hard evidence (the PCAP) that the issue was Layer 2/3 packet loss."
    },
    "V2-C13": {
        "title": "Massive Brute Force Attack",
        "triage": "Charlie gets a P1 Security Alert: Excessive failed SSH logins detected from multiple foreign IPs.",
        "discovery": "Charlie checks `/var/log/auth.log` and sees thousands of `Failed password for root` entries. The server is wasting CPU cycles processing the attempts.",
        "containment": "Charlie immediately stops the SSH service on the public interface, restricting it to the internal management VPN.",
        "resolution": "Charlie installs and configures `fail2ban`. He configures the `sshd` jail to ban IPs after 3 failed attempts.",
        "verification": "Charlie restarts SSH on the public interface and tails the fail2ban log. He watches fail2ban dynamically add iptables rules to drop the attacking IPs.",
        "closure": "Charlie documents the implementation of fail2ban and the drop in CPU usage.",
        "followup": "Charlie schedules a project to disable password authentication entirely and switch to SSH Keys only.",
        "escalation": "If the attack was a massive DDoS saturating the network pipe, Charlie would have escalated to the ISP or Cloud Provider for upstream mitigation."
    },
    "V2-C16": {
        "title": "Runaway Automation Script",
        "triage": "Charlie takes a P2 ticket: The nightly backup script has consumed all CPU and memory, crashing the server.",
        "discovery": "Charlie checks the script and finds a `while` loop that doesn't increment its counter. It's an infinite loop spawning child processes.",
        "containment": "Charlie runs `killall -9 backup.sh` to forcefully terminate the runaway processes and stabilize the server.",
        "resolution": "Charlie edits the Bash script, fixes the logic error in the loop, and adds `set -e` so the script exits immediately if any command fails.",
        "verification": "Charlie manually triggers the script with a small test dataset and verifies it completes successfully and exits.",
        "closure": "Charlie notes the logic error and the addition of `set -e` in the resolution summary.",
        "followup": "Charlie institutes a peer-review policy for all Bash scripts deployed to production.",
        "escalation": "If the script had corrupted production data before crashing, Charlie would escalate to the Database team for a point-in-time restore."
    },
    "V2-C19": {
        "title": "Ransomware Detected",
        "triage": "Charlie receives a P1 Critical alert: Antivirus has flagged a known ransomware binary executing in `/tmp/`.",
        "discovery": "Charlie logs in and immediately checks active network connections using `ss -antp`. He sees the binary attempting to connect to an external Command & Control server.",
        "containment": "Charlie does NOT reboot the server. Instead, he isolates it by disabling its network interfaces (`ip link set eth0 down`), preventing the ransomware from spreading or encrypting network shares.",
        "resolution": "Charlie captures a memory dump for the Security team. Since the system is compromised, he powers it down and deploys a fresh VM from a known-good template.",
        "verification": "Charlie mounts the backups to the new VM and verifies data integrity before allowing it back onto the network.",
        "closure": "Charlie attaches the incident timeline and forensic evidence to the Security Incident ticket.",
        "followup": "Charlie updates the Incident Response playbook to explicitly forbid rebooting compromised servers.",
        "escalation": "Charlie immediately escalated to the Information Security Officer as soon as malware was confirmed."
    },
    "V2-C22": {
        "title": "Application Dependency Hell",
        "triage": "Charlie takes a P3 ticket: Developers complain that the Node.js application runs on their laptops but crashes on the staging server.",
        "discovery": "Charlie checks the server and realizes it has Node.js v14 installed, but the developers are using features from v18.",
        "containment": "Charlie holds off on upgrading the host server's Node.js, as other legacy applications depend on v14.",
        "resolution": "Charlie writes a `Dockerfile` to package the application with its own isolated Node.js v18 environment.",
        "verification": "Charlie runs the container (`docker run ...`). The application launches successfully without affecting the host OS.",
        "closure": "Charlie provides the `Dockerfile` to the developers and closes the ticket.",
        "followup": "Charlie begins migrating all legacy applications to Docker containers to eliminate future dependency conflicts.",
        "escalation": "If Docker was not approved for use in this environment, Charlie would have to escalate to Architecture to request a dedicated VM for the new app."
    },
    "V2-C25": {
        "title": "The Cascading Failure (Capstone)",
        "triage": "Charlie takes a P1 Critical ticket: 'Everything is down.' Users cannot reach the web app, and the database is unreachable.",
        "discovery": "Charlie follows the OSI model. Layer 1/2/3: The network is up. Layer 4: Port 80 is open. Layer 7: Nginx returns a 502 Bad Gateway. He checks the backend app logs and sees 'Cannot connect to database.' He checks the database and sees 'No space left on device.'",
        "containment": "Charlie cleans up old database transaction logs to free up enough space for the database engine to start running again.",
        "resolution": "With the database running, Charlie restarts the backend application, which reconnects to the database. Nginx immediately begins serving traffic.",
        "verification": "Charlie confirms 200 OK responses in the Nginx access logs and verifies the application UI.",
        "closure": "Charlie documents the full chain: Disk full -> DB crash -> App crash -> 502 Gateway.",
        "followup": "Charlie implements strict monitoring on the database disk volume.",
        "escalation": "If the database had corrupted its tables due to the crash, Charlie would have escalated to the DBA team for a repair."
    }
}

spotlights = {
    "V2-C05": """## Industry Incident Spotlight: The GitLab Database Incident

> [!CAUTION] **What Happens When RAID Gives a False Sense of Security?**
> In 2017, GitLab experienced a major database outage that resulted in the loss of production data. 
>
> **The Timeline:**
> - An engineer accidentally deleted a production database directory.
> - The team attempted to restore from backups, only to discover that multiple backup mechanisms had been silently failing for days.
> - They also realized that disk replication (which they were relying on) faithfully and instantly replicated the *deletion* to the standby servers.
>
> **The Root Cause:**
> A combination of human error and untested backup procedures. More importantly, the incident highlighted a fundamental truth: replication and mirroring (like RAID 1) protect against *hardware failure*, not *human error*. 
>
> **The Business Impact:**
> Hours of downtime and a massive, public effort to restore the database from a fragile LVM snapshot, resulting in the permanent loss of several hours of customer data.
>
> **The Lessons Learned:**
> 1. **RAID is not a backup.** If you delete a file, RAID deletes it twice as fast.
> 2. Always test your backup restoration procedures. A backup is worthless if it cannot be restored.
""",
    "V2-C10": """## Industry Incident Spotlight: The Cloudflare Cloudbleed Leak

> [!CAUTION] **When Packets Reveal Too Much**
> In 2017, Cloudflare disclosed a severe vulnerability dubbed "Cloudbleed" that leaked sensitive customer data (including passwords, cookies, and tokens) into random HTTP responses.
>
> **The Timeline:**
> - A Google Project Zero researcher noticed corrupted data in HTTP responses from sites hosted behind Cloudflare.
> - By analyzing the raw packets, they discovered that the corrupted data wasn't just garbage—it contained sensitive memory from other Cloudflare customers.
>
> **The Root Cause:**
> A buffer overrun vulnerability in Cloudflare's HTML parser. The edge servers were reading past the end of a buffer and returning the contents of the server's memory in the HTTP response packets.
>
> **The Business Impact:**
> Sensitive data from millions of websites was potentially exposed and cached by search engines, requiring a massive coordinated effort to purge the leaked data from caches worldwide.
>
> **The Lessons Learned:**
> 1. **Packets don't lie.** Packet capture and analysis were crucial in proving that the server was transmitting data it shouldn't have been.
> 2. What happens in memory often leaks onto the wire if an application is compromised.
""",
    "V2-C12": """## Industry Incident Spotlight: The Heartbleed Bug

> [!CAUTION] **The Vulnerability that Shook the Internet**
> In 2014, the Heartbleed vulnerability (CVE-2014-0160) in OpenSSL was publicly disclosed, affecting an estimated 17% of all secure web servers on the internet.
>
> **The Timeline:**
> - A bug was introduced in the OpenSSL codebase in 2012, affecting the TLS heartbeat extension.
> - For two years, the vulnerability went unnoticed by the open-source community.
> - Security researchers discovered that the bug allowed attackers to read up to 64 kilobytes of server memory per heartbeat request.
>
> **The Root Cause:**
> A missing bounds check in the heartbeat implementation. When a client sent a heartbeat request, they could lie about the payload size, causing the server to respond with its own memory contents (which often included private SSL keys, passwords, and session cookies).
>
> **The Business Impact:**
> Global panic. Companies worldwide had to revoke and reissue their SSL certificates, patch their servers, and advise millions of users to change their passwords.
>
> **The Lessons Learned:**
> 1. **Open source does not automatically mean secure.** Even widely scrutinized code can harbor devastating bugs.
> 2. Hardening a server means keeping packages updated and rotating cryptographic keys in response to massive vulnerabilities.
""",
    "V2-C15": """## Industry Incident Spotlight: The Equifax Data Breach

> [!CAUTION] **The Cost of Ignoring Audits and Updates**
> In 2017, Equifax suffered one of the largest data breaches in history, exposing the personal information of 147 million people.
>
> **The Timeline:**
> - Attackers exploited a known vulnerability in Apache Struts (CVE-2017-5638).
> - They maintained access to Equifax's network for 76 days, moving laterally and extracting data.
> - The breach was eventually discovered by suspicious network traffic, long after the initial intrusion.
>
> **The Root Cause:**
> The initial vector was an unpatched vulnerability. However, the *systemic* root cause was a failure in security auditing and monitoring. A certificate used to monitor encrypted traffic had expired months earlier, blinding their intrusion detection systems.
>
> **The Business Impact:**
> Billions of dollars in settlements, massive reputational damage, and the resignation of top executives.
>
> **The Lessons Learned:**
> 1. **Auditing is not optional.** You must know exactly what software is running in your environment and whether it is vulnerable.
> 2. If your monitoring tools silently fail (like an expired certificate), you are flying blind. Always audit the auditors.
""",
    "V2-C20": """## Industry Incident Spotlight: The Fastly Outage

> [!CAUTION] **When a Configuration Change Takes Down the Internet**
> In June 2021, the Fastly CDN experienced a global outage that brought down major websites including Reddit, Amazon, Twitch, and the New York Times.
>
> **The Timeline:**
> - A single customer updated their CDN configuration with a valid, but edge-case setting.
> - This specific setting triggered a hidden bug in Fastly's VCL (Varnish Configuration Language) compiler.
> - 85% of Fastly's network immediately returned 503 errors.
>
> **The Root Cause:**
> A latent software bug was triggered by a valid customer configuration change, causing the edge proxy servers to crash globally. 
>
> **The Business Impact:**
> A massive chunk of the global internet was inaccessible for approximately 49 minutes, resulting in millions of dollars in lost e-commerce revenue and significant disruption.
>
> **The Lessons Learned:**
> 1. **Reverse proxies are single points of failure.** A bug in the caching layer can bring down the entire infrastructure behind it.
> 2. Configuration rollouts must be staggered. Deploying a change globally in seconds means breaking things globally in seconds.
"""
}

def build_sop_block(sop_dict, ticket_id):
    return f"""## Real-World Support Ticket

> [!IMPORTANT] ServiceNow Ticket: {ticket_id}
> **Title:** {sop_dict['title']}
> **Assigned To:** Charlie (L2 Support Engineer)
> **Status:** IN PROGRESS
> 
> **1) Ticket intake & triage**
> {sop_dict['triage']}
> 
> **2) Discovery & diagnosis**
> {sop_dict['discovery']}
> 
> **3) Immediate containment**
> {sop_dict['containment']}
> 
> **4) Resolution planning & execution**
> {sop_dict['resolution']}
> 
> **5) Verification**
> {sop_dict['verification']}
> 
> **6) Closure & documentation**
> {sop_dict['closure']}
> 
> **7) Post-resolution follow-up**
> {sop_dict['followup']}
> 
> **8) Escalation rules**
> {sop_dict['escalation']}
"""

for filename in os.listdir(base_dir):
    if not filename.startswith("V2-C") or not filename.endswith(".md"):
        continue
        
    chapter_id = filename.split('-')[0] + '-' + filename.split('-')[1]
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean up old blocks
    # Remove old Real-World Support Tickets
    content = re.sub(r"## Real-World Support Ticket.*?(?=## (Hands-on Lab|Industry Incident Spotlight|Common Mistakes))", "", content, flags=re.DOTALL)
    # Remove old Industry Incident Spotlights
    content = re.sub(r"## Industry Incident Spotlight.*?(?=## (Hands-on Lab|Real-World Support Ticket|Common Mistakes))", "", content, flags=re.DOTALL)
    # Remove old Common Mistakes
    content = re.sub(r"## Common Mistakes & Pro-Tips.*?(?=## Chapter Summary)", "", content, flags=re.DOTALL)
    # Remove old Volume Transitions
    content = re.sub(r"\*\*Volume Transition\*\*.*?(?=---(\s+)## Navigation)", "", content, flags=re.DOTALL)
    content = re.sub(r"> But what happens.*?(?=---(\s+)## Navigation)", "", content, flags=re.DOTALL)
    content = re.sub(r"> Securing the system.*?(?=---(\s+)## Navigation)", "", content, flags=re.DOTALL)
    content = re.sub(r"> With that resolved.*?(?=---(\s+)## Navigation)", "", content, flags=re.DOTALL)
    content = re.sub(r"> But a single server.*?(?=---(\s+)## Navigation)", "", content, flags=re.DOTALL)
    content = re.sub(r"> Now that we've mastered.*?(?=---(\s+)## Navigation)", "", content, flags=re.DOTALL)
    content = re.sub(r"> This works for one server.*?(?=---(\s+)## Navigation)", "", content, flags=re.DOTALL)
    content = re.sub(r"> But what if the network.*?(?=---(\s+)## Navigation)", "", content, flags=re.DOTALL)
    content = re.sub(r"> Storage is cheap.*?(?=---(\s+)## Navigation)", "", content, flags=re.DOTALL)

    # Clean up empty newlines near Navigation
    content = re.sub(r"\n{3,}---", "\n\n---", content)

    # 2. Inject SOP
    if chapter_id in sops:
        ticket_id = f"INC-2026{int(''.join(filter(str.isdigit, chapter_id)))}"
        sop_block = build_sop_block(sops[chapter_id], ticket_id)
        content = content.replace("## Hands-on Lab", sop_block + "\n\n## Hands-on Lab")

    # 3. Inject Spotlight
    if chapter_id in spotlights:
        spotlight_block = spotlights[chapter_id]
        if "## Real-World Support Ticket" in content:
            content = content.replace("## Real-World Support Ticket", spotlight_block + "\n\n## Real-World Support Ticket")
        else:
            content = content.replace("## Hands-on Lab", spotlight_block + "\n\n## Hands-on Lab")

    # 4. Inject Common Mistakes
    if chapter_id in mistakes_dict:
        mistake, think = mistakes_dict[chapter_id]
        features_block = f"""## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> {mistake}

> [!CAUTION] Think Before You Type
> {think}

"""
        content = content.replace("## Chapter Summary", features_block + "## Chapter Summary")

    # 5. Inject Transition
    if chapter_id in transitions:
        transition = transitions[chapter_id]
        trans_block = f"""**Chapter Transition**
> {transition}

"""
        content = re.sub(r"---(\s+)## Navigation", f"---\n\n{trans_block}---\n\\1## Navigation", content)

    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Applied unified script: 25 Unique Transitions, 8-Step SOPs, Spotlights, and Mistakes.")
