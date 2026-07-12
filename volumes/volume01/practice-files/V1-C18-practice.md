# Practice Guide: Chapter 18

## Objective
To simulate a massive log file and parse it using vertical filtering (`grep -v`) and horizontal filtering (`awk`).

## Assignment 1: The Raw Data
First, let's create a dummy log file.

1. Open your terminal and copy/paste this exact command block to create a file named `server.log`:
```bash
cat << 'EOF' > server.log
192.168.1.10 admin SUCCESS logged_in
192.168.1.15 sarah SUCCESS logged_in
10.0.0.55    guest FAILURE bad_password
192.168.1.10 admin SUCCESS file_uploaded
172.16.0.4   root  FAILURE lockout
EOF
```
2. Run `cat server.log` to see the raw data. 

## Assignment 2: Vertical Filtering (Grep)
Imagine this file has 10,000 lines. We only want to see the failures.

1. Use `grep` to invert the match and filter OUT the noise:
   `grep -v "SUCCESS" server.log`
2. Look at the output. You should now only see the two lines containing "FAILURE".

## Assignment 3: Horizontal Filtering (Awk)
Now that we have the bad rows, we need to extract actionable data. We want to know exactly *which* IP addresses are failing so we can block them in our firewall.

1. Look at the structure of the data. The IP address is the first word (Column 1).
2. Use the pipe (`|`) to send the output of `grep` directly into `awk`:
   `grep -v "SUCCESS" server.log | awk '{print $1}'`
3. Look at the output. It should be perfectly clean:
   ```text
   10.0.0.55
   172.16.0.4
   ```
4. Now, let's extract the IPs and the Usernames (Columns 1 and 2):
   `grep -v "SUCCESS" server.log | awk '{print $1, $2}'`

## Success Criteria
You have successfully completed this practice if you were able to create the dummy log file, completely strip out the "SUCCESS" rows using `grep -v`, and extract the IP address column using `awk '{print $1}'`.
