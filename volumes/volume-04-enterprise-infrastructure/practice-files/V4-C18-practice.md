# Practice Guide: Chapter 18 (Volume 4)

## Objective
To use `tcpdump` to capture raw network packets on a specific port, write them to a file, and read them back.

## Assignment 1: Basic Packet Sniffing
Let's watch raw internet traffic in real-time.

1. Ensure `tcpdump` is installed (it usually is by default on servers):
   `sudo apt install tcpdump` (Ubuntu) or `sudo dnf install tcpdump` (RHEL)
2. Run `tcpdump`, telling it to listen on all interfaces (`-i any`), filter only TCP port 443 (HTTPS), and disable DNS resolution (`-n`) so it runs faster:
   `sudo tcpdump -i any -n tcp port 443`
3. Open a second terminal (or just open a web browser and go to a random website).
4. **Observation:** Your terminal will explode with scrolling text. You are seeing the raw packets of your secure web browsing!
5. Press `Ctrl+C` in the `tcpdump` terminal to stop the capture.

## Assignment 2: Capturing to a PCAP File
Reading scrolling text is hard. We want to save the packets to a file for analysis.

1. We will use the `-w` flag to write to a file, and the `-c` flag to tell `tcpdump` to automatically exit after it captures exactly 20 packets.
2. We will also monitor port 80 (HTTP) instead of 443.
   `sudo tcpdump -i any -n tcp port 80 -c 20 -w /tmp/my_capture.pcap`
3. **Observation:** The terminal will just sit there, saying `listening on any...`. It is waiting for HTTP traffic!
4. Open your second terminal and generate some HTTP traffic using `curl`. We will use a public API that does not require HTTPS:
   `curl http://ip-api.com/json/`
5. Go back to your first terminal. It should have exited automatically, stating `20 packets captured`.

## Assignment 3: Reading the PCAP
Normally, you would download `/tmp/my_capture.pcap` to your laptop and open it in the Wireshark GUI. However, we can also read it directly in the terminal!

1. Use the `-r` flag to read the file:
   `tcpdump -r /tmp/my_capture.pcap`
2. **Analysis:** Look closely at the output. 
   * You will see the IP address of your machine sending a packet to the IP of `ip-api.com` with the `[S]` flag. That is the `SYN` packet!
   * You will see `ip-api.com` replying with a packet flagged `[S.]`. The dot means `ACK`. This is the `SYN-ACK` packet!
   * You will see your machine reply with `[.]` (just the `ACK`). 
   * The 3-Way Handshake is complete! The subsequent packets contain the actual HTTP `curl` request and the JSON response data.

## Assignment 4: Cleanup
1. PCAP files contain sensitive data. Delete it!
   `rm /tmp/my_capture.pcap`

## Success Criteria
You have successfully completed this practice if you ran a live packet capture, filtered it by port, wrote the raw packets to a `.pcap` file, and successfully identified the `[S]` and `[S.]` flags of the 3-Way Handshake in the output.
