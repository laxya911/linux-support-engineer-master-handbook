import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(os.path.dirname(script_dir), "chapters")

transitions = {
    "V5-C01": "We have the philosophy of performance analysis, but the standard tools are too slow and invasive. We need something running directly in the kernel: eBPF.",
    "V5-C02": "eBPF gives us incredible data, but raw data is impossible for a human to interpret quickly. We need to visualize it with Flame Graphs.",
    "V5-C03": "We can visualize CPU time, but what happens when the application isn't using CPU, it's just hoarding memory and crashing the server?",
    "V5-C04": "Memory leaks are resolved, but the application is still slow. Is it the code, or is the network silently dropping packets?",
    "V5-C05": "Network latency is under control, but a misconfiguration has left the system completely unbootable. How do we recover?",
    "V5-C06": "The system boots, but under heavy load, it abruptly dies with a kernel panic. We must extract the core dump to find out why.",
    "V5-C07": "The kernel is stable, but our traditional filesystems can't handle petabytes of data and snapshotting. We need advanced filesystems.",
    "V5-C08": "Storage is scalable, but as our clusters grow, standard iptables firewalls melt down. We must use eBPF for networking and security.",
    "V5-C09": "The network is secure, but the default Linux kernel limits are choking our high-throughput database. We must tune the sysctl parameters.",
    "V5-C10": "The system is perfectly tuned, but how do we know when we will physically run out of servers? We need formal Capacity Planning.",
    "V5-C11": "We have planned capacity, but a sudden viral traffic spike will overwhelm it regardless. We must aggressively drop traffic with Rate Limiting.",
    "V5-C12": "Traffic is shaped, but managing rate limits across 500 microservices is impossible. We need a dedicated Service Mesh.",
    "V5-C13": "The mesh routes traffic flawlessly, but how do multiple databases agree on the truth across geographic regions? Distributed Consensus.",
    "V5-C14": "Our systems are globally distributed, but how do we mathematically measure if they are 'reliable enough' for our users? Service Level Objectives.",
    "V5-C15": "We are measuring reliability, but when the SLO drops and the entire platform crashes, who is in charge of fixing it? The Incident Commander.",
    "V5-C16": "The fire is out and the incident is resolved. But if you punish the engineer who broke it, you will never learn why. We need Blameless Post-Mortems.",
    "V5-C17": "We've learned from the incident, but implementing the fix requires 10 hours of manual, repetitive work. This is Toil, and it must be destroyed.",
    "V5-C18": "Automation has eliminated toil. But how do we train the junior engineers to handle the stress of a real outage? We run War Room Simulations.",
    "V5-C19": "You've survived the simulations and mastered the technology. It's time to talk about the final transition: leading other engineers."
}

def apply_transitions():
    for filename in os.listdir(base_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(base_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Clean up old generic transition
            content = re.sub(r'## Chapter Transition\n\nIn this chapter.*?## Navigation', '## Navigation', content, flags=re.DOTALL)
            content = re.sub(r'\*\*Chapter Transition\*\*.*?(?=---\s+## Navigation)', '', content, flags=re.DOTALL)
            
            # Inject new custom transition
            chapter_id = filename[:6]
            if chapter_id in transitions:
                trans_text = transitions[chapter_id]
                new_block = f"**Chapter Transition**\n> {trans_text}\n\n---\n\n## Navigation"
                content = re.sub(r'## Navigation', new_block, content, count=1)
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    apply_transitions()
    print("Volume 5 transitions applied successfully.")
