# Practice Guide: Chapter 13

## Objective
To master the `journalctl` utility by querying, filtering, and streaming live logs from the `systemd` journal.

## Assignment 1: The Firehose
If you run `journalctl` without filters, it will print everything that has happened on the server since it was turned on.

1. Type `journalctl` and press Enter.
2. Use the **Spacebar** to page down.
3. Use the **arrow keys** to scroll up and down line by line.
4. Press `/` to search, type `kernel`, and press Enter. 
5. Press `q` to quit the pager.

## Assignment 2: Surgical Filtering
We are going to isolate the logs for the Secure Shell (SSH) daemon, which handles your remote terminal connection.

1. Filter the journal by the SSH unit and jump directly to the end:
   `journalctl -u ssh -e` (Ubuntu) OR `journalctl -u sshd -e` (RHEL)
   *(Note: The service name differs slightly between Ubuntu and RHEL).*
2. Look at the output. You should see entries regarding "Accepted publickey" or "Accepted password", proving you logged in.
3. Press `q` to quit.
4. Now, run the same query but limit it to today:
   `journalctl -u ssh --since "today"` (Ubuntu) OR `journalctl -u sshd --since "today"` (RHEL)

## Assignment 3: Live Streaming
Just like `tail -f` in Chapter 6, `journalctl` can stream logs in real-time. We will watch the journal while we restart the Nginx web server we installed in Chapter 12.

1. Start streaming the `nginx` logs from the journal:
   `journalctl -u nginx -f`
2. Open a **second** terminal window/SSH session to your virtual machine.
3. In the second terminal, restart the web server:
   `sudo systemctl restart nginx`
4. Look back at your first terminal. You will instantly see the journal log that the daemon received a stop signal, shut down, and then successfully started back up.
5. Press `Ctrl + C` in the first terminal to stop following the log.

## Success Criteria
You have successfully completed this practice if you were able to filter the journal by a specific unit (`-u`), jump to the end of the logs (`-e`), restrict the timeframe (`--since`), and watch a service restart in real-time using the follow flag (`-f`).
