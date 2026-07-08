# Command Index: Volume 3 (Enterprise Linux Services)

This is a comprehensive index of the primary CLI tools and commands introduced in Volume 3.

### Web Services
* `apache2ctl` / `apachectl` - Apache HTTP server control interface (e.g., `apache2ctl configtest`).
* `nginx -t` - Test NGINX configuration for syntax errors.
* `nginx -s reload` - Reload NGINX without dropping connections.
* `certbot` - Tool for obtaining and renewing Let's Encrypt SSL/TLS certificates.

### Database Services
* `mysql` / `mariadb` - The MariaDB/MySQL command-line tool.
* `mysql_secure_installation` - Script to improve MariaDB security.
* `mysqldump` - Logical database backup program.
* `psql` - The PostgreSQL interactive terminal.
* `pg_dump` - Extract a PostgreSQL database into a script file or other archive file.

### Network Services
* `dig` - DNS lookup utility (e.g., `dig @8.8.8.8 google.com`).
* `nslookup` - Query Internet name servers interactively.
* `mail` / `mailx` - Send and receive Internet mail.
* `chronyc` - Command-line interface for Chrony daemon (e.g., `chronyc tracking`, `chronyc sources`).
* `wg` - Configuration utility for WireGuard VPN (e.g., `wg genkey`, `wg pubkey`).

### Infrastructure Services
* `smbclient` - FTP-like client to access SMB/CIFS resources on servers.
* `smbstatus` - Report on current Samba connections and Oplocks.
* `jq` - Command-line JSON processor (used for parsing structured logs).
* `curl` - Transfer a URL (used heavily for fetching `/metrics` endpoints).
* `redis-cli` - The Redis command line interface (e.g., `SET`, `GET`, `EXPIRE`).

### Modern App Deployment (Containers)
* `docker run` - Run a command in a new container.
* `docker ps` - List running containers.
* `docker images` - List local images.
* `docker build` - Build an image from a Dockerfile.
* `docker exec` - Run a command in a running container.
* `docker rm` - Remove one or more containers.
* `docker volume create` - Create a volume.
* `docker compose up` - Build, (re)create, start, and attach to containers for a service.
* `docker compose down` - Stop containers and remove containers, networks, volumes, and images created by `up`.
