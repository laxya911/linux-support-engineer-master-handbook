# Practice Guide: Chapter 7 (Volume 3)

## Objective
To install MariaDB, run the secure installation script, and successfully log into the database prompt.

## Assignment 1: Installation
Let's install the database daemon.

1. Install MariaDB Server:
   * **Ubuntu/Debian:** `sudo apt update && sudo apt install mariadb-server`
   * **RHEL/CentOS:** `sudo dnf install mariadb-server`
2. Ensure the service is running and enabled on boot:
   `sudo systemctl enable --now mariadb`
3. Verify it is listening on Port 3306:
   `sudo ss -tulpn | grep 3306`

## Assignment 2: Hardening
We must remove the insecure defaults immediately.

1. Run the security script:
   `sudo mysql_secure_installation`
2. Answer the prompts carefully:
   * Current password for root: *(Leave blank and press Enter)*
   * Switch to unix_socket authentication? `Y`
   * Change the root password? `Y` *(Type a secure password and remember it!)*
   * Remove anonymous users? `Y`
   * Disallow root login remotely? `Y`
   * Remove test database and access to it? `Y`
   * Reload privilege tables now? `Y`

## Assignment 3: Logging In
Now let's access the database shell using our new credentials.

1. Tell the `mysql` client to connect using the `root` database user (`-u root`) and prompt for a password (`-p`):
   `mysql -u root -p`
2. Type the password you created in the previous step.
3. **Observation:** Your terminal prompt will change from `user@server:~$` to `MariaDB [(none)]>`. You are now inside the database!
4. Run a SQL command to view the internal databases:
   `SHOW DATABASES;`
   *(Don't forget the semicolon at the end!)*
5. Exit the database and return to Linux:
   `exit;`

## Success Criteria
You have successfully completed this practice if you installed MariaDB, secured it using the built-in wizard, logged into the `mysql>` prompt, and executed the `SHOW DATABASES;` command successfully.
