# Practice Guide: Chapter 3 (Volume 3)

## Objective
To completely remove Apache, install NGINX in its place, and configure a basic Server Block.

## Assignment 1: Clearing the Port
Remember Chapter 1! Both Apache and NGINX want to listen on Port 80. They cannot run at the same time. We must remove Apache.

1. Stop and disable Apache:
   `sudo systemctl disable --now apache2` (or `httpd` on RHEL)
2. Verify Port 80 is free:
   `sudo ss -tulpn | grep :80`
   *(It should return absolutely nothing).*

## Assignment 2: Installing NGINX
Now we can install our new, high-performance web server.

1. Install NGINX:
   * **Ubuntu/Debian:** `sudo apt install nginx`
   * **RHEL/CentOS:** `sudo dnf install nginx`
2. Enable and start the service:
   `sudo systemctl enable --now nginx`
3. Verify it stole Port 80:
   `sudo ss -tulpn | grep :80`
   *(You should see `nginx` listed in the output!)*

## Assignment 3: Writing a Server Block
Let's tell NGINX to serve a specific directory for a specific domain name.

1. Create a new directory for our app:
   `sudo mkdir /var/www/myapp`
2. Create an `index.html` file inside it:
   `echo "<h1>Powered by NGINX!</h1>" | sudo tee /var/www/myapp/index.html`
3. Create the NGINX configuration file:
   `sudo nano /etc/nginx/sites-available/myapp.conf`
4. Write the following Server Block (pay attention to the semicolons!):
   ```nginx
   server {
       listen 80;
       server_name localhost;
       root /var/www/myapp;
       index index.html;
   }
   ```
5. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Assignment 4: Syntax Testing and Enabling
Let's see if we made any typos.

1. Run the test command:
   `sudo nginx -t`
   *(If it says `syntax is ok` and `test is successful`, proceed!)*
2. Since we are on Ubuntu, we must manually symlink the file to enable it. (There is no `a2ensite` for Nginx, we use the raw `ln` command):
   `sudo ln -s /etc/nginx/sites-available/myapp.conf /etc/nginx/sites-enabled/`
3. Reload NGINX to apply the changes:
   `sudo systemctl reload nginx`
4. Test the website:
   `curl http://localhost`
   *(You should see `<h1>Powered by NGINX!</h1>`)*

## Success Criteria
You have successfully completed this practice if you stopped the Apache service, installed NGINX, wrote a custom `server {}` block, validated it with `nginx -t`, and successfully served your custom HTML page.
