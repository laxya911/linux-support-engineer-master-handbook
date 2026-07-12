# Practice Guide: Chapter 23 (Volume 3)

## Objective
To write a `docker-compose.yml` file and launch a multi-container microservice stack.

## Assignment 1: The Configuration
We are going to deploy the exact WordPress/MariaDB stack discussed in the chapter!

1. Create a new directory and move into it:
   `mkdir ~/wordpress-stack && cd ~/wordpress-stack`
2. Create the compose file:
   `nano docker-compose.yml`
3. Paste the following YAML. *(Warning: YAML is highly sensitive to spaces. Do not use tabs, use spaces for indentation!)*:
   ```yaml
   version: '3.8'

   services:
     web:
       image: wordpress:latest
       ports:
         - "8080:80"
       environment:
         WORDPRESS_DB_HOST: database:3306
         WORDPRESS_DB_USER: wp_user
         WORDPRESS_DB_PASSWORD: wp_password
         WORDPRESS_DB_NAME: wp_db

     database:
       image: mariadb:10.6
       environment:
         MYSQL_DATABASE: wp_db
         MYSQL_USER: wp_user
         MYSQL_PASSWORD: wp_password
         MYSQL_RANDOM_ROOT_PASSWORD: '1'
   ```
4. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Assignment 2: The Execution
Let's spin it up!

1. Run the stack in detached mode:
   `sudo docker compose up -d`
   *(If you are on an older OS, the command might be `docker-compose` with a hyphen).*
2. **Observation:** Docker will pull both the `wordpress` and `mariadb` images. It will automatically create a virtual network, and it will start both containers simultaneously.
3. Check the status of the stack:
   `sudo docker compose ps`
4. **Result:** You should see both `web` and `database` in an "Up" state.

## Assignment 3: Verification
Did the internal DNS work? Did WordPress find the database?

1. Open your web browser or use `curl` to hit the web container:
   `curl -L http://localhost:8080`
2. **Result:** If it dumps a massive amount of HTML to your screen, it worked! WordPress successfully resolved the name `database`, logged into MariaDB using the environment variables, and rendered the setup page.
3. Tear down the entire stack (this destroys the containers and the network):
   `sudo docker compose down`

## Success Criteria
You have successfully completed this practice if you wrote a valid YAML compose file, spun up the stack using `docker compose up -d`, and verified that the `web` container successfully communicated with the `database` container via internal DNS.
