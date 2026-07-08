# Practice Guide: Chapter 1 (Volume 4)

## Objective
To install `kubectl` (the Kubernetes command-line tool) and `minikube` (a local, single-node Kubernetes cluster for testing).

## Assignment 1: Installing kubectl
`kubectl` is just a binary executable that sends REST API requests to a Kubernetes Control Plane. You can install it on your local laptop, even if your cluster is in AWS!

1. Download the latest binary for Linux:
   `curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"`
2. Make the binary executable:
   `chmod +x kubectl`
3. Move it to your system's PATH so you can run it from anywhere:
   `sudo mv kubectl /usr/local/bin/`
4. Verify the installation:
   `kubectl version --client`

## Assignment 2: Installing Minikube
To practice Kubernetes without paying AWS for 3 servers, we use `minikube`. It spins up a tiny virtual machine on your laptop that acts as BOTH the Control Plane and the Worker Node.

1. Download the Minikube binary:
   `curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64`
2. Install it:
   `sudo install minikube-linux-amd64 /usr/local/bin/minikube`
3. Start your local cluster! *(Note: this assumes Docker is already installed and running on your system from Volume 3).*
   `minikube start --driver=docker`
4. **Observation:** Minikube will download the Kubernetes ISO and spin up the Control Plane components (API Server, etcd).

## Assignment 3: Querying the Cluster
Now that `kubectl` is installed and the cluster is running, let's talk to the API Server!

1. Ask the API Server for a list of all physical servers (Nodes) in the cluster:
   `kubectl get nodes`
2. **Result:** You should see a single node named `minikube` with a status of `Ready` and a role of `control-plane`.
3. Ask the API Server for detailed information about this specific node:
   `kubectl describe node minikube`
4. **Observation:** This output is massive! It shows exactly how much CPU and RAM the node has, what its IP address is, and what system software (like the Container Runtime) it is running.

## Success Criteria
You have successfully completed this practice if you installed `kubectl` and `minikube`, successfully started a local cluster, and used `kubectl get nodes` to retrieve data from the Kube-API Server.
