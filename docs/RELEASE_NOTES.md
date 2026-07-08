# Release Notes

This document provides a reader-focused summary of changes and additions for each version of the **Linux Support Engineer Master Handbook**.

---

## Version 0.1 (In Progress)

**Added**
* Volume 1 foundational directory structure.
* [Chapter 1: Welcome to Linux Support Engineering](../volumes/volume-01-linux-fundamentals/chapters/V1-C01-welcome-to-linux-support-engineering.md)
* [Chapter 2: Linux Architecture & Distributions](../volumes/volume-01-linux-fundamentals/chapters/V1-C02-linux-architecture-and-distributions.md)
* [Chapter 3: Provisioning Linux](../volumes/volume-01-linux-fundamentals/chapters/V1-C03-provisioning-linux.md)
* [Chapter 4: Linux Boot Process](../volumes/volume-01-linux-fundamentals/chapters/V1-C04-linux-boot-process.md)
* [Chapter 5: Linux Filesystem](../volumes/volume-01-linux-fundamentals/chapters/V1-C05-linux-filesystem.md)
* [Chapter 6: Working with Files & Directories](../volumes/volume-01-linux-fundamentals/chapters/V1-C06-working-with-files-and-directories.md)
* [Chapter 7: Text Editors (nano & vim)](../volumes/volume-01-linux-fundamentals/chapters/V1-C07-text-editors.md)
* [Chapter 8: Users & Groups](../volumes/volume-01-linux-fundamentals/chapters/V1-C08-users-and-groups.md)
* [Chapter 9: File Permissions & Ownership](../volumes/volume-01-linux-fundamentals/chapters/V1-C09-file-permissions-and-ownership.md)
* [Chapter 10: Package Management](../volumes/volume-01-linux-fundamentals/chapters/V1-C10-package-management.md)
* [Chapter 11: Process Management](../volumes/volume-01-linux-fundamentals/chapters/V1-C11-process-management.md)
* [Chapter 12: Services & systemd](../volumes/volume-01-linux-fundamentals/chapters/V1-C12-services-and-systemd.md)
* [Chapter 13: Software Logs & Journals](../volumes/volume-01-linux-fundamentals/chapters/V1-C13-software-logs-and-journals.md)
* [Chapter 14: Networking Fundamentals](../volumes/volume-01-linux-fundamentals/chapters/V1-C14-networking-fundamentals.md)
* [Chapter 15: SSH Administration](../volumes/volume-01-linux-fundamentals/chapters/V1-C15-ssh-administration.md)
* [Chapter 16: Archiving and Compression](../volumes/volume-01-linux-fundamentals/chapters/V1-C16-archiving-and-compression.md)
* [Chapter 17: Storage & Disk Management](../volumes/volume-01-linux-fundamentals/chapters/V1-C17-storage-and-disk-management.md)
* [Chapter 18: Advanced Grep & Awk](../volumes/volume-01-linux-fundamentals/chapters/V1-C18-advanced-grep-and-awk.md)
* [Chapter 19: Output Redirection (Piping)](../volumes/volume-01-linux-fundamentals/chapters/V1-C19-output-redirection.md)
* [Chapter 20: Bash Scripting Basics](../volumes/volume-01-linux-fundamentals/chapters/V1-C20-bash-scripting-basics.md)
* [Chapter 21: Environment Variables](../volumes/volume-01-linux-fundamentals/chapters/V1-C21-environment-variables.md)
* [Chapter 22: User Automation (Cron)](../volumes/volume-01-linux-fundamentals/chapters/V1-C22-user-automation-cron.md)
* [Chapter 23: Basic System Monitoring](../volumes/volume-01-linux-fundamentals/chapters/V1-C23-basic-system-monitoring.md)
* [Chapter 24: Introduction to Networking (Firewalls)](../volumes/volume-01-linux-fundamentals/chapters/V1-C24-introduction-to-networking-firewalls.md)
* [Chapter 25: DNS & Name Resolution](../volumes/volume-01-linux-fundamentals/chapters/V1-C25-dns-and-name-resolution.md)
* [Chapter 26: System Startup & Troubleshooting](../volumes/volume-01-linux-fundamentals/chapters/V1-C26-system-startup-and-troubleshooting.md)
* [Chapter 27: Introduction to Web Servers](../volumes/volume-01-linux-fundamentals/chapters/V1-C27-introduction-to-web-servers.md)
* [Chapter 28: Reverse Proxies & Load Balancing](../volumes/volume-01-linux-fundamentals/chapters/V1-C28-reverse-proxies-and-load-balancing.md)
* [Chapter 29: Database Fundamentals](../volumes/volume-01-linux-fundamentals/chapters/V1-C29-database-fundamentals.md)
* [Chapter 30: Conclusion & Career Path](../volumes/volume-01-linux-fundamentals/chapters/V1-C30-conclusion-and-career-path.md)
* Practice guides for Chapters 1 through 30 (`practice-files/` directory).

### 🎯 Milestone Achieved
* **Volume 1 (Linux Fundamentals) is officially 100% complete.**
* Ready to begin Volume 2 (Linux Administration).
* `BOOK_STYLE_GUIDE.md` to enforce quality standards, including mandatory `mermaid` architectural diagrams.
* Dedicated `references/` tracker for external technical documentation.

**Improved**
* Officially standardized the dual-distribution approach, explicitly validating instructions against **Ubuntu 26.04 LTS** and **RHEL 10 / CentOS Stream**.
* Completely overhauled the Markdown frontmatter to track reading time, lab counts, and editorial review status.
* Migrated plain-text drafts into structured GitHub Flavored Markdown (GFM) with standardized callouts.

**Fixed**
* Replaced all absolute system paths with relative links to ensure portability on GitHub.
* Corrected the Volume 1 TOC to strictly follow the 30-chapter milestone path.
