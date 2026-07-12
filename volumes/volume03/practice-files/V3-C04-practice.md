# Practice Guide: Chapter 4 (Volume 3)

## Objective
To spin up a dummy backend application using Python, and then configure NGINX to act as a Reverse Proxy for it.

## Assignment 1: The Backend Application
We need an "Application Server" to hide. We will use a built-in Python tool to create a simple HTTP server on Port 8000.

1. Open a terminal and create a folder for the app:
   `mkdir ~/backend_app`
   `cd ~/backend_app`
2. Create an HTML file for the app:
   `echo "<h1>Hello from the hidden Python App!</h1>" > index.html`
3. Start the Python web server on Port 8000:
   `python3 -m http.server 8000`
4. **Observation:** This terminal is now locked, running the application. It will print any requests it receives. Leave this terminal window open!

## Assignment 2: The NGINX Shield
Open a *second* terminal window and connect to your VM. Let's configure the shield.

1. Open the NGINX configuration you created in the last chapter:
   `sudo nano /etc/nginx/sites-available/myapp.conf`
2. Delete the `root` and `index` lines. Replace them with the `proxy_pass` directive so the file looks exactly like this:
   ```nginx
   server {
       listen 80;
       server_name localhost;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
3. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).
4. Test for typos and reload:
   `sudo nginx -t`
   `sudo systemctl reload nginx`

## Assignment 3: Testing the Proxy
1. In your second terminal, make a request to Port 80 (NGINX):
   `curl http://localhost`
2. **Observation:** You should receive `<h1>Hello from the hidden Python App!</h1>`.
3. Look at your first terminal window (where Python is running). You will see a log entry confirming that NGINX successfully grabbed the request from Port 80 and forwarded it to Python on Port 8000!

## Success Criteria
You have successfully completed this practice if you started a Python backend server, reconfigured your NGINX Server Block to use `proxy_pass`, and successfully retrieved the Python app's data by querying the NGINX proxy.
