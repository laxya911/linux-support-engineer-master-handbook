# Practice Guide: Chapter 5 (Volume 4)

## Objective
To install the Helm CLI, add a third-party repository, and deploy a pre-packaged Apache architecture.

## Assignment 1: Installing Helm
Helm is a binary CLI tool, exactly like `kubectl`. It runs on your laptop, not in the cluster.

1. Download and execute the official installation script:
   `curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3`
   `chmod 700 get_helm.sh`
   `./get_helm.sh`
2. Verify the installation:
   `helm version`

## Assignment 2: Adding a Repository
Helm needs to know where to download Charts from. Bitnami (owned by VMware) maintains some of the best, most secure open-source Helm Charts in the world.

1. Add the Bitnami repository to your local Helm client:
   `helm repo add bitnami https://charts.bitnami.com/bitnami`
2. Update your local cache (just like `apt-get update`):
   `helm repo update`
3. Search the repository to see if they have an Apache chart:
   `helm search repo bitnami/apache`
4. **Observation:** You should see the chart listed in the search results!

## Assignment 3: The Deployment
Let's deploy the entire Apache stack. We will name our specific installation (Release) `my-web-server`.

1. Ensure your local cluster is running:
   `minikube start`
2. Install the Chart:
   `helm install my-web-server bitnami/apache`
3. **Observation:** Helm will instantly output a summary of what it deployed.
4. Verify what Helm actually created in your Kubernetes cluster:
   `kubectl get deployments`
   `kubectl get pods`
   `kubectl get services`
5. **Result:** You will see that Helm automatically created a Deployment, spun up a Pod, and created a Service, all perfectly configured to work together!

## Assignment 4: Cleanup
Uninstalling a massive architecture is just as easy as installing it.

1. Tell Helm to uninstall the Release:
   `helm uninstall my-web-server`
2. Verify the cluster is clean:
   `kubectl get pods`

## Success Criteria
You have successfully completed this practice if you installed the Helm CLI, added the Bitnami repository, deployed an Apache stack with a single command, and successfully uninstalled it.
