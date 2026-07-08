# Practice Guide: Chapter 9 (Volume 3)

## Objective
To implement the Principle of Least Privilege by creating a dedicated database and a restricted user in MariaDB.

## Assignment 1: The Root Admin
First, we must log in as the ultimate authority.

1. Log into your MariaDB server using the root user:
   `sudo mysql -u root -p`
   *(Enter the password you created in Chapter 7).*
2. View the current databases:
   `SHOW DATABASES;`

## Assignment 2: Creating the Infrastructure
Let's pretend we are installing a new web application called "WebStore".

1. Create a dedicated database for the application:
   `CREATE DATABASE webstore_db;`
2. Create a dedicated user for the application (replace the password with your own):
   `CREATE USER 'webstore_app'@'localhost' IDENTIFIED BY 'SecretAppPass123';`
3. Give the new user full control, but *only* over their specific database:
   `GRANT ALL PRIVILEGES ON webstore_db.* TO 'webstore_app'@'localhost';`
4. Apply the security changes to the daemon:
   `FLUSH PRIVILEGES;`
5. Exit the root session:
   `exit;`

## Assignment 3: Testing the Blast Radius
Now, let's pretend to be the WebStore application and see what we have access to.

1. Log in as the new restricted user:
   `mysql -u webstore_app -p`
   *(Enter the SecretAppPass123 password).*
2. Try to view all the databases on the server:
   `SHOW DATABASES;`
3. **Observation:** Look closely at the output. You will only see `information_schema` (a system requirement) and `webstore_db`. You cannot see the `mysql` database. You cannot see the `sys` database. The server is hiding them from you because you don't have privileges!
4. Try to create a new database:
   `CREATE DATABASE hacker_db;`
5. **Observation:** The server will block you: `ERROR 1044 (42000): Access denied for user 'webstore_app'@'localhost' to database 'hacker_db'`.

## Success Criteria
You have successfully completed this practice if you created a dedicated database and user, logged in as that restricted user, and proved that the user was physically incapable of accessing or creating databases outside of their granted permissions.
