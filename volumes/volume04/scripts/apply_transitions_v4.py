import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(os.path.dirname(script_dir), "chapters")

transitions = {
    "V4-C01": "We understand the control plane and worker nodes, but how do we actually run an application on them? It's time to create Deployments.",
    "V4-C02": "Our application is running and scaling, but pods are ephemeral. How do users consistently access them? We need Kubernetes Networking.",
    "V4-C03": "Network traffic is flowing, but what happens when a database pod crashes and loses all its data? We must master Stateful workloads.",
    "V4-C04": "We can manage complex workloads, but manually editing dozens of YAML files is error-prone. Enter the Helm package manager.",
    "V4-C05": "Kubernetes handles the application layer beautifully. But who provisions the underlying Kubernetes clusters and VMs? We need Infrastructure as Code.",
    "V4-C06": "We can declare infrastructure in code, but how do we orchestrate deploying massive networks across public clouds?",
    "V4-C07": "The cloud infrastructure is provisioned, but the VMs are blank. How do we configure them automatically at scale? We need Configuration Management.",
    "V4-C08": "We know the basics of Ansible, but running ad-hoc commands doesn't scale. We must structure our automation into Playbooks.",
    "V4-C09": "Our infrastructure and configurations are automated, but engineers shouldn't run these from their laptops. We need Continuous Integration and Delivery.",
    "V4-C10": "Code flows automatically to production, but how do we route users to the geographically closest data center? Global DNS.",
    "V4-C11": "Traffic reaches the right data center, but how do we ensure internal services don't blindly trust each other? Zero Trust Architecture.",
    "V4-C12": "We assume breach, but where are we storing our database passwords and API tokens? Hardcoding them is a disaster waiting to happen.",
    "V4-C13": "Secrets are secured centrally, but what stops a compromised web server from talking directly to a payroll database? Microsegmentation.",
    "V4-C14": "The perimeter and interior are secured, but what happens when a novel attack still succeeds? You must execute a formal Incident Response.",
    "V4-C15": "The fire is out and the incident is over, but guessing the root cause prevents learning. We must use Scientific Troubleshooting.",
    "V4-C16": "The scientific method guides us, but how do you diagnose a system that entirely locks up and crashes? You must analyze Kernel Panics.",
    "V4-C17": "The kernel is stable, but an application is mysteriously dropping connections. It's time to pull out the packet analyzer.",
    "V4-C18": "Network packets are flowing correctly, but the application is still unacceptably slow. Where is the CPU spending all its time?",
    "V4-C19": "We've optimized the code and systems, but how do we prove our infrastructure can survive a real failure? By intentionally breaking it."
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
    print("Volume 4 transitions applied successfully.")
