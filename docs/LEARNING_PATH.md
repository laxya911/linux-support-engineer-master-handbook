# Learning Path

This guide maps common enterprise administration roles, tasks, and Windows Server features to their Linux counterparts. It provides a structured path showing how concepts transfer between systems.

---

## Conceptual Equivalency Mapping

When moving from a Windows Server administration background to Linux, use this table as a quick translation guide:

| Windows Server Concept / Tool | Linux Equivalent | Description | Volume |
| :--- | :--- | :--- | :--- |
| **Command Prompt / PowerShell** | Bash / Zsh / Shell Scripting | Text-based command line and scripting environments | Volume 1 |
| **Windows Explorer / Drive Letters** | Filesystem Hierarchy Standard (FHS) | Directory tree structure starting at the root `/` | Volume 1 |
| **File Permissions (NTFS / Shares)** | Standard UGO Permissions / POSIX ACLs | Owner, Group, and Other read/write/execute permissions | Volume 1 |
| **Windows Services (`services.msc`)** | `systemd` / Daemons | Background processes and daemon management | Volume 1 |
| **Task Scheduler** | `cron` / `systemd` timers | Scheduled tasks and automation scripts | Volume 1 |
| **Device Manager** | `/dev` / `lsblk` / `lspci` / `udev` | Device representation and hardware diagnostics | Volume 1 |
| **Event Viewer / Windows Logs** | `journald` / Syslog (`/var/log`) | Centralized log daemon and text-based logs | Volume 1 |
| **Control Panel / Registry** | `/etc/` configuration files | Configuration files stored in human-readable plain text | Volume 2 |
| **Active Directory (AD DS)** | LDAP / FreeIPA / SSSD / Samba | Directory services and centralized identity management | Volume 3 |
| **IIS (Internet Information Services)** | Nginx / Apache | High-performance web servers | Volume 3 |
| **Windows Firewall** | `firewalld` / `ufw` / `nftables` | Network traffic packet filtering and firewalls | Volume 3 |
| **Performance Monitor (`perfmon`)** | `top` / `htop` / `sar` / `sysstat` | Resource monitoring and performance analysis | Volume 4 |
| **Failover Clustering** | Pacemaker / Corosync / Keepalived | High availability and clustering | Volume 4 |
| **Active Directory Certificate Services** | OpenSSL / Certbot | Certificate authorities and cryptographic keys | Volume 5 |

---

## Suggested Progression

1. **Phase 1: Foundations (Volume 1)**
   * Focus on terminal navigation, text manipulation, file management, and getting comfortable running basic commands headless.
2. **Phase 2: Administration (Volume 2)**
   * Transition to managing disk partitions, mounting devices, setting up local user databases, and managing network configurations.
3. **Phase 3: Core Services (Volume 3)**
   * Deploy infrastructure servers: configure web servers (Nginx/Apache), secure them with local firewalls, and integrate them with centralized directory servers.
4. **Phase 4: Support & Diagnostics (Volume 4)**
   * Master debugging skills: analyze network packets, read log trends, perform system profiling, and troubleshoot kernel panics or boot failures.
5. **Phase 5: Scale & Automation (Volume 5)**
   * Automate deployments using Ansible, manage infrastructure-as-code, deploy containerized environments (Docker/Podman), and learn modern site reliability engineering (SRE) practices.
