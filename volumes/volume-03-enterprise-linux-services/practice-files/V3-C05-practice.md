# Practice Guide: Chapter 5 (Volume 3)

## Objective
To generate a "Self-Signed" SSL certificate using `openssl` and configure NGINX to use it on Port 443.

*(Note: We cannot use `certbot` for this lab because you need a real, registered domain name to get a certificate from Let's Encrypt. A Self-Signed certificate provides the exact same encryption, but because it is not signed by a real CA, your browser will show a warning).*

## Assignment 1: Generating the Keys
We will use the OpenSSL tool to generate our own Private Key and Public Certificate.

1. Run the following massive command to generate the keys (it will prompt you for information; just press `Enter` to accept the defaults for everything):
   `sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt`
2. Verify the keys were created:
   `ls -l /etc/ssl/certs/nginx-selfsigned.crt`
   `sudo ls -l /etc/ssl/private/nginx-selfsigned.key`

## Assignment 2: Configuring NGINX for HTTPS
Now we must tell NGINX to listen on Port 443 and use the keys we just generated.

1. Open your NGINX configuration from the previous chapter:
   `sudo nano /etc/nginx/sites-available/myapp.conf`
2. Modify the configuration to look exactly like this:
   ```nginx
   server {
       listen 80;
       server_name localhost;
       return 301 https://$host$request_uri; # Redirect HTTP to HTTPS
   }

   server {
       listen 443 ssl;
       server_name localhost;
       
       ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
       ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
       }
   }
   ```
3. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).
4. Test and reload NGINX:
   `sudo nginx -t`
   `sudo systemctl reload nginx`

## Assignment 3: Testing the Secure Connection
Let's verify NGINX is now forcing encryption. Ensure your Python backend from Chapter 4 is still running in another terminal!

1. Try to visit the site over Port 80 (HTTP):
   `curl -I http://localhost`
2. **Observation:** You will receive a `HTTP/1.1 301 Moved Permanently` response. The server refused to serve the data and told you to use HTTPS!
3. Try to visit the site over Port 443 (HTTPS):
   `curl -k https://localhost` 
   *(The `-k` flag tells `curl` to ignore the fact that our certificate is self-signed and not trusted by a CA).*
4. **Result:** You will securely receive the `<h1>Hello from the hidden Python App!</h1>` message, fully encrypted!

## Success Criteria
You have successfully completed this practice if you generated an OpenSSL keypair, configured NGINX to listen on Port 443, implemented a 301 redirect on Port 80, and successfully fetched encrypted data using `curl -k`.
