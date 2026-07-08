# Command Index: Volume 4 (Enterprise Infrastructure)

This is a comprehensive index of the primary CLI tools and commands introduced in Volume 4.

### Kubernetes (`kubectl`)
* `kubectl get nodes` - List all nodes in the cluster.
* `kubectl get pods` - List all pods in the current namespace.
* `kubectl describe pod <name>` - View detailed information about a specific pod.
* `kubectl apply -f <file.yaml>` - Create or update resources from a YAML manifest.
* `kubectl logs <pod-name>` - Print the logs for a container in a pod.
* `kubectl exec -it <pod-name> -- /bin/sh` - Get an interactive shell inside a running pod.
* `kubectl rollout undo deployment <name>` - Roll back a deployment to the previous version.

### Kubernetes Ecosystem (Helm)
* `helm repo add` - Add a chart repository.
* `helm install` - Install a chart.
* `helm list` - List releases.

### HashiCorp Terraform (`terraform`)
* `terraform init` - Initialize a working directory and download provider plugins.
* `terraform plan` - Generate and show an execution plan.
* `terraform apply` - Builds or changes infrastructure.
* `terraform destroy` - Destroy Terraform-managed infrastructure.
* `terraform fmt` - Reformat your configuration in the standard style.
* `terraform validate` - Check whether the configuration is valid.

### Ansible (`ansible`)
* `ansible all -m ping -i inventory.ini` - Test connection to all hosts in the inventory.
* `ansible all -a "/bin/echo hello" -i inventory.ini` - Run an arbitrary command on all hosts.
* `ansible-playbook playbook.yaml` - Execute an Ansible playbook.
* `ansible-galaxy init <role_name>` - Initialize a new Ansible role directory structure.

### HashiCorp Vault (`vault`)
* `vault server -dev` - Start a local development server.
* `vault login <token>` - Authenticate to the Vault server.
* `vault kv put secret/path key=value` - Write a static secret.
* `vault kv get secret/path` - Read a static secret.

### Incident Response & Auditing (`auditd`)
* `sudo systemctl status auditd` - Check the status of the audit daemon.
* `sudo auditctl -w /path/to/file -p rwxa -k <keyname>` - Set a dynamic watch rule on a file.
* `sudo ausearch -k <keyname>` - Search the audit logs for a specific key.

### Advanced Diagnostics (`tcpdump` & `strace` & `crash`)
* `sudo tcpdump -i any tcp port 80` - Sniff TCP packets on port 80 on all interfaces.
* `sudo tcpdump -i any -w capture.pcap` - Write captured packets to a file.
* `tcpdump -r capture.pcap` - Read captured packets from a file.
* `sudo strace -p <PID>` - Attach to a running process and trace its system calls.
* `sudo strace -e trace=openat -p <PID>` - Trace only specific system calls.
* `echo c | sudo tee /proc/sysrq-trigger` - Intentionally trigger a Kernel Panic (DANGEROUS).
* `crash /path/to/vmlinux /path/to/vmcore` - Open a core dump for analysis.
* `bt` - (Inside crash) Print the backtrace of the panic.
