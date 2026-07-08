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
