# Practice Guide: Chapter 8 (Volume 3)

## Objective
To install PostgreSQL, navigate its unique Peer Authentication system, and set a password for the default administrative user.

## Assignment 1: Installation
First, we install the database and start the service.

1. Install PostgreSQL:
   * **Ubuntu/Debian:** `sudo apt update && sudo apt install postgresql postgresql-contrib`
   * **RHEL/CentOS:** `sudo dnf install postgresql-server && sudo postgresql-setup --initdb`
2. Enable and start the service:
   `sudo systemctl enable --now postgresql`
3. Verify it is listening on its default port (5432):
   `sudo ss -tulpn | grep 5432`

## Assignment 2: The Peer Rejection
Let's purposely trigger the famous error.

1. While logged in as your normal user (e.g., `ubuntu` or `root`), try to access the `postgres` database shell:
   `psql -U postgres`
2. **Observation:** You should be instantly rejected with the `Peer authentication failed for user "postgres"` error!

## Assignment 3: The Proper Login
We must respect the `pg_hba.conf` rules. We need to become the correct Linux user first.

1. Switch to the `postgres` Linux system user (which was created during installation):
   `sudo -i -u postgres`
2. **Observation:** Your terminal prompt will change. You are no longer `root` or `ubuntu`.
3. Now, try to launch the shell again (you don't even need the `-U` flag now, because it knows who you are!):
   `psql`
4. **Observation:** Success! Your prompt changes to `postgres=#`.

## Assignment 4: Setting a Password
If we want to change `pg_hba.conf` to allow password logins later, we must actually set a password for this user first!

1. While inside the `psql` shell, type the following SQL command to set a password (replace `MySecret123` with your own password):
   `\password postgres`
2. Type your new password twice.
3. Exit the `psql` shell:
   `\q`
4. Exit the `postgres` Linux user and return to your normal user:
   `exit`

## Success Criteria
You have successfully completed this practice if you intentionally triggered a Peer Authentication error, bypassed it by switching to the correct Linux system user, logged into the `psql` shell, and set a permanent database password.
