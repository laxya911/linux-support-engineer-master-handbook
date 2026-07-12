# Practice Guide: Chapter 2 (Volume 3)

## Objective
To install the Apache web server, interact with the default Document Root, and serve a custom HTML page.

## Assignment 1: Installation
First, we must install the web server daemon.

1. **Ubuntu/Debian:** 
   `sudo apt update`
   `sudo apt install apache2`
2. **RHEL/CentOS:**
   `sudo dnf install httpd`
   `sudo systemctl enable --now httpd`

## Assignment 2: Verification
Let's prove the server is running and listening on the correct port.

1. Run the `ss` command to check for Port 80:
   `sudo ss -tulpn | grep :80`
2. **Observation:** You should see `apache2` (or `httpd`) listening on Port 80!
3. Now, let's use `curl` to fetch the default webpage from ourselves:
   `curl http://localhost`
4. **Observation:** Your terminal will fill with massive amounts of HTML code. This is the default "Welcome to Apache" page.

## Assignment 3: Modifying the Document Root
We don't want to serve the default page; we want to serve our own application!

1. Navigate to the default Document Root:
   `cd /var/www/html/`
2. Look at the files inside:
   `ls -l`
   *(You will see an `index.html` file. This is the file `curl` just downloaded).*
3. Let's delete the default file (requires `sudo`):
   `sudo rm index.html`
4. Now, create your own file and write a simple message into it:
   `echo "<h1>My First Web Server!</h1>" | sudo tee index.html`
5. Test the server again:
   `curl http://localhost`
6. **Result:** Instead of a massive wall of text, the server should respond with exactly what you wrote: `<h1>My First Web Server!</h1>`

## Success Criteria
You have successfully completed this practice if you installed Apache, proved it was listening on Port 80 using `ss`, and successfully modified the `/var/www/html/index.html` file to serve your own custom content.
