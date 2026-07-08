# Practice Guide: Chapter 4 (Volume 4)

## Objective
To create a Kubernetes Secret and securely inject it into a Pod as an Environment Variable.

## Assignment 1: Creating the Secret
We will use the imperative `kubectl` command to create the Secret directly in the cluster, ensuring it is never saved to a file on our hard drive.

1. Start your local cluster if it isn't running:
   `minikube start`
2. Create a generic secret named `my-db-secret` containing a dummy password:
   `kubectl create secret generic my-db-secret --from-literal=DB_PASS='SuperSecurePassword123!'`
3. Verify the secret exists in the cluster:
   `kubectl get secrets`
4. Attempt to view the secret data:
   `kubectl describe secret my-db-secret`
5. **Observation:** The output will show `Data: DB_PASS: 23 bytes`. It deliberately hides the actual password from casual observation!

## Assignment 2: Injecting the Secret
Now we will write a Pod manifest that references this Secret, rather than hardcoding the password.

1. Create a new file:
   `nano secure-pod.yaml`
2. Paste the following configuration:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: secure-app
   spec:
     containers:
     - name: alpine-container
       image: alpine
       command: ["sleep", "3600"]
       env:
         - name: DATABASE_PASSWORD
           valueFrom:
             secretKeyRef:
               name: my-db-secret
               key: DB_PASS
   ```
3. Save and exit. Notice how safe this file is! You could upload this `secure-pod.yaml` file to a public GitHub repository, and nobody would know the password. 

## Assignment 3: Verification
Did Kubernetes successfully inject the password into the running container?

1. Apply the manifest:
   `kubectl apply -f secure-pod.yaml`
2. Wait a few seconds, then verify the Pod is `Running`:
   `kubectl get pods`
3. Execute a command *inside* the running Pod to print its environment variables. We will pipe it to `grep` to look for `DATABASE_PASSWORD`:
   `kubectl exec secure-app -- env | grep DATABASE_PASSWORD`
4. **Result:** You should see `DATABASE_PASSWORD=SuperSecurePassword123!`. The Pod successfully pulled the secure data from the K8s API server at runtime!

## Assignment 4: Cleanup
1. Delete the Pod and the Secret:
   `kubectl delete -f secure-pod.yaml`
   `kubectl delete secret my-db-secret`

## Success Criteria
You have successfully completed this practice if you created a Secret imperatively, deployed a Pod that referenced that Secret using `secretKeyRef`, and verified the environment variable existed inside the running container.
