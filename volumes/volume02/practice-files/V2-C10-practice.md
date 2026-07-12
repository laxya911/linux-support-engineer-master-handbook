# Practice Guide: Chapter 10 (Volume 2)

## Objective
To capture live ICMP (ping) traffic using `tcpdump` and filter out background noise.

## Assignment 1: The Infinite Loop Warning
If you run `tcpdump` without filters, you will capture your own SSH session. Every time `tcpdump` prints a line of text, that text is sent over SSH, which generates another packet, which `tcpdump` captures and prints, generating another packet...

1. Run a filtered capture that explicitly *ignores* your SSH port (Port 22):
   `sudo tcpdump -i any not port 22`
2. **Observation:** You might see some random background noise (like NTP time syncs or DNS queries), but it shouldn't flood your screen.
3. Stop the capture by pressing `Ctrl+C`.

## Assignment 2: Capturing a Ping
Let's capture a specific protocol: ICMP (the protocol used by the `ping` command).

1. You will need two terminal windows open and connected to your VM.
2. **In Terminal 1**, start the packet capture, filtering specifically for ICMP traffic:
   `sudo tcpdump -i any icmp`
   *(Notice that the command just sits there, waiting).*
3. **In Terminal 2**, send 3 pings to Google:
   `ping -c 3 8.8.8.8`
4. **Observation:** Look back at Terminal 1. You should see exactly 6 lines of output! 
   * Three lines showing your server sending an "echo request" to Google.
   * Three lines showing Google sending an "echo reply" back to your server.
5. Stop the capture in Terminal 1 using `Ctrl+C`.

## Success Criteria
You have successfully completed this practice if you were able to use `tcpdump` to capture and verify the exact moment a `ping` packet left your server and returned.
