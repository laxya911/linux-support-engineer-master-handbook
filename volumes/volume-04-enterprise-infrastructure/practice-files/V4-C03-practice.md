# Practice Guide: Chapter 3 (Volume 4)

## Objective
To deploy an NGINX deployment, expose it internally via a `ClusterIP` Service, and prove that internal DNS resolves the Service name.

## Assignment 1: The Deployment and Service
We can combine multiple Kubernetes resources into a single YAML file by separating them with `---`.

1. Start your local cluster if it isn't running:
   `minikube start`
2. Create a new file:
   `nano my-network-stack.yaml`
3. Paste the following configuration:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: web-backend
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: nginx-backend
     template:
       metadata:
         labels:
           app: nginx-backend
       spec:
         containers:
         - name: nginx
           image: nginx:alpine
           ports:
           - containerPort: 80
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: backend-service
   spec:
     type: ClusterIP
     selector:
       app: nginx-backend
     ports:
       - port: 8080
         targetPort: 80
   ```
4. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Assignment 2: Execution
Notice in the file above, the Service `selector` exactly matches the Deployment `labels`. Notice also that the Service listens on port `8080`, but forwards to the Pods' targetPort `80`.

1. Apply the manifest:
   `kubectl apply -f my-network-stack.yaml`
2. Verify the Service was created:
   `kubectl get svc`
3. **Observation:** You will see `backend-service` of type `ClusterIP` with an internal IP address (e.g., `10.96.x.x`). Because it is ClusterIP, you *cannot* reach it from your laptop browser.

## Assignment 3: Internal DNS Proving
Let's pretend we are a different application inside the cluster trying to reach the backend. We will spin up a temporary, interactive Alpine pod just to test the network.

1. Run an interactive, disposable pod:
   `kubectl run test-pod -it --rm --image=alpine -- sh`
2. **Observation:** Your prompt has changed. You are now inside a pod in the Kubernetes cluster.
3. Inside the pod, install the `curl` utility:
   `apk add --no-cache curl`
4. Now, attempt to reach the NGINX backend using the exact name of the Service we created, on the Service's port (8080):
   `curl http://backend-service:8080`
5. **Result:** A massive dump of NGINX HTML! CoreDNS successfully translated `backend-service` into the ClusterIP, which then securely routed your TCP packets to one of the two NGINX Pods!
6. Exit the interactive pod (it will automatically delete itself because of the `--rm` flag):
   `exit`

## Assignment 4: Cleanup
1. Delete the Deployment and Service:
   `kubectl delete -f my-network-stack.yaml`

## Success Criteria
You have successfully completed this practice if you deployed a Service, dropped into an interactive Pod on the same network, and successfully used `curl` with the internal DNS name of the Service to fetch the NGINX homepage.
