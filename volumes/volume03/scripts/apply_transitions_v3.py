import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(os.path.dirname(script_dir), "chapters")

transitions = {
    "V3-C01": "We understand how the web works in theory. Now, let's deploy the server that powers half the internet.",
    "V3-C02": "Apache is robust, but for high-concurrency environments, we need an asynchronous alternative.",
    "V3-C03": "Having a web server is great, but exposing it directly to the internet is dangerous. We need a proxy.",
    "V3-C04": "The proxy is in place, but traffic is still transmitted in plaintext. It's time to secure the transport layer.",
    "V3-C05": "With the web tier secured, we must now focus on where the actual data lives: the database.",
    "V3-C06": "Concepts are fine, but our application needs a real relational database to store its data.",
    "V3-C07": "MariaDB is excellent for traditional apps, but complex analytical queries might require something more robust.",
    "V3-C08": "The database is running, but an exposed database is a compromised database. We must secure it.",
    "V3-C09": "Security is in place, but if the disk dies, the data is still lost. We need a backup strategy.",
    "V3-C10": "The data is safe, but how do users actually find our web application? They aren't going to type an IP address.",
    "V3-C11": "DNS resolves the names, but how do our internal servers get their IP addresses in the first place?",
    "V3-C12": "The network is fully routed and resolved, but our applications need to send notifications to users.",
    "V3-C13": "Logs from email, web, and database servers are scattered everywhere. We need to synchronize the timestamps to make sense of them.",
    "V3-C14": "Time is synchronized, but how do remote engineers securely access this infrastructure to read the logs?",
    "V3-C15": "Remote access is secured via VPN, but developers need a way to share files across the network.",
    "V3-C16": "With file sharing active, the number of logs being generated is overwhelming. We need a central location for them.",
    "V3-C17": "Logs tell us what happened *in the past*, but how do we know if the server is crashing *right now*?",
    "V3-C18": "Prometheus is collecting metrics, but staring at raw numbers is inefficient. We need dashboards.",
    "V3-C19": "We can see the traffic spikes in Grafana, and our database is struggling to keep up. We need a caching layer.",
    "V3-C20": "Redis solved our database load, but installing all these services manually is becoming a nightmare.",
    "V3-C21": "We understand containers, but how do we actually build our own custom application images?",
    "V3-C22": "Building one image is easy. Managing a stack of five interdependent containers is not. Enter Docker Compose.",
    "V3-C23": "The containers are running, but what happens to the database when the container stops? We need persistence.",
    "V3-C24": "We have persistent containers on a single host. But what happens when that host dies?",
    "V3-C25": "Congratulations on completing Volume 3. Next up: Volume 4 - Enterprise Infrastructure."
}

mistakes_dict = {
    "V3-C01": ("Ignoring HTTP status codes. A 200 OK doesn't mean the app works if the page is completely blank.", "`curl -I example.com` (Are you checking the headers or just the body?)"),
    "V3-C02": ("Leaving the default Apache index page active, exposing your server version to attackers.", "`systemctl reload apache2` (Did you run `apachectl configtest` first?)"),
    "V3-C03": ("Forgetting to pass the `X-Forwarded-For` header. Your backend app will think all traffic is coming from the NGINX server itself!", "`nginx -s reload` (Did you test the config?)"),
    "V3-C04": ("Creating an open proxy by accident, allowing attackers to route their malicious traffic through your server.", "`proxy_pass http://localhost:8080/` (Does the trailing slash matter? Yes, it changes the entire URI path!)"),
    "V3-C05": ("Letting an SSL certificate expire silently, causing every browser in the world to block your website.", "`certbot renew --force-renewal` (Are you sure? You might hit the Let's Encrypt rate limit and be blocked for a week.)"),
    "V3-C06": ("Assuming NoSQL is faster than SQL for everything, leading to unmaintainable data structures.", "`SELECT * FROM users` (Do you really need all 50 columns for a million rows?)"),
    "V3-C07": ("Running MariaDB without running `mysql_secure_installation`, leaving the root password blank.", "`DROP TABLE users;` (Do you have a backup from 5 minutes ago?)"),
    "V3-C08": ("Forgetting to update `pg_hba.conf`, locking everyone out of PostgreSQL including yourself.", "`ALTER USER postgres WITH PASSWORD '123';` (Did you just set a trivial password on the superuser?)"),
    "V3-C09": ("Binding the database to `0.0.0.0` without a firewall, exposing it to the entire internet.", "`GRANT ALL PRIVILEGES ON *.* TO 'app'@'%'` (Does the web app really need DROP privileges?)"),
    "V3-C10": ("Backing up the database to the same physical disk the database is running on.", "`mysqldump --all-databases > backup.sql` (Will this lock the tables and cause an outage during the dump?)"),
    "V3-C11": ("Forgetting to update the serial number in the SOA record. The secondary DNS servers will never pull the new records.", "`systemctl restart named` (Did you run `named-checkzone` first?)"),
    "V3-C12": ("Creating a DHCP scope that overlaps with your statically assigned servers, causing massive IP conflicts.", "`systemctl restart isc-dhcp-server` (Are you sure there isn't another rogue DHCP server on the network?)"),
    "V3-C13": ("Leaving Postfix configured as an open relay. You will be blacklisted by every major email provider within 24 hours.", "`postsuper -d ALL` (Did you just delete legitimate outgoing email along with the spam?)"),
    "V3-C14": ("Relying on hardware clocks across a distributed database cluster. The nodes will reject transactions if they are out of sync by a few milliseconds.", "`date -s '12:00:00'` (Did you just manually jump the time? Databases might crash due to time-traveling transactions!)"),
    "V3-C15": ("Routing all internet traffic through the VPN (0.0.0.0/0) instead of just the corporate subnet, saturating your office bandwidth.", "`wg-quick down wg0` (Are you connected over the VPN right now? You will drop your own connection.)"),
    "V3-C16": ("Setting Samba permissions wide open (`guest ok = yes`) on a share containing HR documents.", "`smbpasswd -a user` (Does the Linux user actually exist in `/etc/passwd`?)"),
    "V3-C17": ("Forwarding debug-level logs to the central logging server, overwhelming the network and filling up the disk in hours.", "`logger 'Test message'` (Did you check which facility and severity it was sent to?)"),
    "V3-C18": ("Scraping metrics every 1 second from hundreds of targets. Prometheus will run out of memory and crash.", "`systemctl restart prometheus` (Did you validate the YAML syntax? Prometheus will refuse to start if there's a single extra space.)"),
    "V3-C19": ("Creating a dashboard that queries a year of high-resolution data on load, causing the browser to freeze and the database to spike.", "`systemctl restart grafana-server` (Did you backup the SQLite database first?)"),
    "V3-C20": ("Using Redis as a primary persistent database without understanding that it holds data in volatile RAM.", "`FLUSHALL` (Did you just delete the cache for the entire production cluster?)"),
    "V3-C21": ("Running containers with the `--privileged` flag, giving the container root access to the host machine.", "`docker run -d -p 80:80 nginx` (Is port 80 already in use by Apache on the host?)"),
    "V3-C22": ("Putting `apt-get update` and `apt-get install` on separate lines in the Dockerfile. Docker will cache the update and install outdated packages.", "`docker build --no-cache .` (Do you have the time to wait 20 minutes for a full rebuild?)"),
    "V3-C23": ("Hardcoding IP addresses in `docker-compose.yml` instead of relying on the internal Docker DNS resolver.", "`docker-compose down -v` (Did you just delete the named volumes and all the database data?)"),
    "V3-C24": ("Mounting a local host directory `/data` into a container without setting the correct SELinux context (`:z`). The container will get Permission Denied.", "`rm -rf /var/lib/docker/volumes/` (Are you sure you want to destroy all persistent data for all containers?)"),
    "V3-C25": ("Trying to manually manage 100 containers across 10 hosts using Docker CLI instead of moving to an orchestrator like Kubernetes.", "`docker swarm init` (Are you prepared for the complexity of distributed state?)"),
}

sops = {
    "V3-C03": {
        "title": "502 Bad Gateway on All Web Traffic",
        "triage": "Charlie receives a P1 Critical alert: The primary e-commerce site is returning 502 errors.",
        "discovery": "Charlie checks the NGINX error logs (`/var/log/nginx/error.log`) and sees `connect() failed (111: Connection refused) while connecting to upstream`. The proxy cannot reach the backend application.",
        "containment": "Charlie places a static 'Maintenance' page on the NGINX proxy to provide a better user experience while he investigates.",
        "resolution": "Charlie SSHes into the backend application server and discovers the Node.js process crashed. He restarts the service (`systemctl restart node-app`).",
        "verification": "Charlie runs `curl -I localhost:3000` on the backend, then removes the Maintenance page on NGINX. The site loads successfully.",
        "closure": "Charlie documents the upstream connection refusal and resolves the ticket.",
        "followup": "Charlie adds a systemd `Restart=always` directive to the Node.js service to automatically recover from future crashes.",
        "escalation": "If the backend application continuously crashed on startup, Charlie would escalate to the Development team."
    },
    "V3-C05": {
        "title": "Expired SSL Certificate",
        "triage": "Charlie takes a P1 ticket: Users report their browsers are showing a terrifying 'Your connection is not private' red screen.",
        "discovery": "Charlie runs `curl -vI https://example.com` and sees `SSL certificate problem: certificate has expired`. He checks the Let's Encrypt logs and sees the automated renewal cron job failed due to a firewall change.",
        "containment": "Charlie immediately opens port 80 on the firewall, which Let's Encrypt requires for the HTTP-01 challenge.",
        "resolution": "Charlie manually forces the renewal using `certbot renew --force-renewal`. He then reloads NGINX to apply the new certificate.",
        "verification": "Charlie accesses the site in a fresh browser session and verifies the padlock is green and valid for another 90 days.",
        "closure": "Charlie documents the firewall blockage and resolves the ticket.",
        "followup": "Charlie sets up an external monitoring alert to notify the team 14 days before a certificate expires.",
        "escalation": "If the certificate authority was completely unreachable, Charlie would escalate to Network Engineering to check outbound routing."
    },
    "V3-C11": {
        "title": "DNS NXDOMAIN for Primary API",
        "triage": "Charlie receives a P1 alert: The mobile app cannot connect to `api.corp.com`.",
        "discovery": "Charlie runs `dig api.corp.com` and receives an `NXDOMAIN` (Non-Existent Domain) response. He checks the primary BIND server and sees a syntax error in the zone file loaded 10 minutes ago.",
        "containment": "Charlie immediately rolls back the zone file to the previous version and runs `rndc reload` to restore service.",
        "resolution": "Charlie reviews the broken zone file and finds a missing trailing dot on a CNAME record, which corrupted the entire zone. He fixes the typo.",
        "verification": "Charlie runs `named-checkzone` to verify the syntax, applies the change, and runs `dig` to confirm the IP resolves correctly.",
        "closure": "Charlie documents the missing trailing dot and resolves the ticket.",
        "followup": "Charlie implements a git hook that automatically runs `named-checkzone` before allowing any engineer to commit changes to the DNS repository.",
        "escalation": "If the issue was a global root server problem, Charlie would escalate to the ISP."
    },
    "V3-C23": {
        "title": "Database Connection Failure in Docker Compose",
        "triage": "Charlie takes a P2 ticket: The newly deployed staging environment via Docker Compose is failing to start.",
        "discovery": "Charlie runs `docker-compose logs web` and sees `Host not found: db`. He checks `docker-compose.yml` and notices the web service and the database service are on entirely different custom bridge networks.",
        "containment": "Charlie stops the broken deployment (`docker-compose down`) to free up the ports.",
        "resolution": "Charlie edits the `docker-compose.yml` file, moving both services to the same custom bridge network so Docker's internal DNS can resolve the service names.",
        "verification": "Charlie runs `docker-compose up -d` and watches the logs. The web service successfully connects to the database.",
        "closure": "Charlie documents the network isolation issue and resolves the ticket.",
        "followup": "Charlie adds a network validation step to the CI/CD pipeline.",
        "escalation": "If the container kept crashing silently without logs, Charlie would escalate to the application developers to add debug logging."
    }
}

spotlights = {
    "V3-C11": """## Industry Incident Spotlight: The 2021 Facebook BGP & DNS Outage

> [!CAUTION] **When You Delete Yourself From the Internet**
> In October 2021, Facebook, Instagram, and WhatsApp disappeared from the internet for over six hours.
>
> **The Timeline:**
> - During routine maintenance, an engineer issued a command intended to assess global backbone capacity.
> - A bug in an auditing tool allowed the command to execute incorrectly, cutting off all BGP routing between Facebook's data centers.
> - Because the BGP routes were withdrawn, the global internet could no longer reach Facebook's DNS servers.
>
> **The Root Cause:**
> Without DNS, nothing worked. Internal tools, employee door badges, and external routing all relied on the same unified network infrastructure, which had just effectively severed its own connections to the outside world.
>
> **The Business Impact:**
> Over $60 million in lost ad revenue and massive disruptions to global communications.
>
> **The Lessons Learned:**
> 1. **DNS is the Achilles Heel of the Internet.** If your DNS servers go down, it doesn't matter if your web servers are perfectly healthy.
> 2. Avoid circular dependencies. Facebook employees couldn't access the data centers to fix the issue because their digital door badges relied on the servers they were trying to fix.
""",
    "V3-C07": """## Industry Incident Spotlight: The 2017 British Airways IT Outage

> [!CAUTION] **When High Availability Fails**
> In May 2017, British Airways suffered a massive IT outage that grounded flights globally for three days.
>
> **The Timeline:**
> - A contractor performing maintenance at a primary data center accidentally disconnected a power supply.
> - When power was restored minutes later, the surge caused massive damage to the database servers.
> - The automated failover to the backup data center failed because the database replication became unsynchronized and corrupted.
>
> **The Root Cause:**
> The primary database systems were violently shut down, and the disaster recovery protocols had not been properly tested for this specific "unclean shutdown" scenario.
>
> **The Business Impact:**
> 75,000 passengers stranded, thousands of flights canceled, and an estimated £80 million in compensation costs.
>
> **The Lessons Learned:**
> 1. **Test your Disaster Recovery.** Having a backup database is useless if the failover mechanism fails when you actually need it.
> 2. Uncontrolled power restoration can be more damaging than the power loss itself.
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
    if not filename.startswith("V3-C") or not filename.endswith(".md"):
        continue
        
    chapter_id = filename.split('-')[0] + '-' + filename.split('-')[1]
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean existing summary tags if any, to append our features cleanly
    content = re.sub(r"## Common Mistakes & Pro-Tips.*?(?=## Chapter Summary)", "", content, flags=re.DOTALL)
    
    # 1. Inject SOP (Only for selected chapters)
    if chapter_id in sops:
        ticket_id = f"INC-3026{int(''.join(filter(str.isdigit, chapter_id)))}"
        sop_block = build_sop_block(sops[chapter_id], ticket_id)
        if "## Hands-on Lab" in content:
            content = content.replace("## Hands-on Lab", sop_block + "\n\n## Hands-on Lab")
        elif "## Chapter Summary" in content:
            content = content.replace("## Chapter Summary", sop_block + "\n\n## Chapter Summary")

    # 2. Inject Spotlight
    if chapter_id in spotlights:
        spotlight_block = spotlights[chapter_id]
        if "## Hands-on Lab" in content:
            content = content.replace("## Hands-on Lab", spotlight_block + "\n\n## Hands-on Lab")
        elif "## Chapter Summary" in content:
            content = content.replace("## Chapter Summary", spotlight_block + "\n\n## Chapter Summary")

    # 3. Inject Common Mistakes
    if chapter_id in mistakes_dict:
        mistake, think = mistakes_dict[chapter_id]
        features_block = f"""## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> {mistake}

> [!CAUTION] Think Before You Type
> {think}

"""
        content = content.replace("## Chapter Summary", features_block + "## Chapter Summary")

    # 4. Inject Transition
    if chapter_id in transitions:
        transition = transitions[chapter_id]
        trans_block = f"""**Chapter Transition**
> {transition}

"""
        # Append before Navigation or end of file
        if "## Navigation" in content:
            content = re.sub(r"---(\s+)## Navigation", f"---\n\n{trans_block}---\n\\1## Navigation", content)
        else:
            content += f"\n\n---\n\n{trans_block}---\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Volume 3 Refactored Successfully!")
