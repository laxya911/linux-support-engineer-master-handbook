# Practice Guide: Chapter 27

## Objective
To simulate basic web server troubleshooting steps using command-line tools. 

*(Note: You do not need to install Nginx for this lab. We are practicing the diagnostic muscle memory).*

## Assignment 1: Local Connectivity Testing
When a website is down, you must figure out if the web server process is actually answering requests, or if the firewall is blocking it. You do this by testing from *inside* the server using `curl`.

1. Run the following command to ask Google's web server for its HTTP headers:
   `curl -I https://google.com`
2. **Result:** Look at the very first line of the output. It should say `HTTP/2 200`. The `200` means "OK" / "Success".
3. Now try fetching a page that doesn't exist:
   `curl -I https://google.com/this-is-a-fake-page.html`
4. **Result:** Look at the first line. It should say `HTTP/2 404`. The `404` means "Not Found".
5. *(In the real world, if you run `curl -I localhost` on a web server and get a `200`, but your customer gets a timeout, you instantly know the web server is fine and the firewall is broken!)*

## Assignment 2: Locating the Error Logs
If a web server throws a 403 or 500 error, the answer is always in the error log. You must memorize where these logs live.

1. Navigate to the main log directory:
   `cd /var/log/`
2. Run `ls`.
3. If you were troubleshooting an Apache server, you would look for a directory named `apache2` (Ubuntu) or `httpd` (RHEL).
4. If you were troubleshooting an Nginx server, you would look for a directory named `nginx`.
5. The command to watch errors happen in real-time is:
   `tail -f /var/log/nginx/error.log` (or `apache2/error.log`).

## Assignment 3: The Syntax Check Habit
Memorize these syntax check commands. They will save your job.

* If you are working on Nginx, run:
  `nginx -t`
* If you are working on Apache (Ubuntu), run:
  `apache2ctl configtest`
* If you are working on Apache (RHEL/CentOS), run:
  `httpd -t`

*Note: If you run these on your VM right now without the software installed, you will get a "command not found" error, which is expected. The goal is to memorize the commands!*

## Success Criteria
You have successfully completed this practice if you used `curl -I` to fetch HTTP headers (identifying a 200 OK and a 404 Not Found), navigated to `/var/log` to identify where web logs live, and memorized the syntax check commands for both Apache and Nginx.
