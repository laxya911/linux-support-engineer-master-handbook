# Practice Guide: Chapter 2 (Volume 4)

## Objective
To write a declarative Deployment YAML, deploy it to Minikube, and observe the self-healing capabilities of a ReplicaSet.

## Assignment 1: The Declarative YAML
Instead of imperative commands, we will write our desired state into a file.

1. Start your local cluster if it isn't running:
   `minikube start`

2. Create a new directory and file:
   `mkdir ~/k8s-practice && cd ~/k8s-practice`
   `nano my-deployment.yaml`

3. Paste the following configuration:

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: nginx-deployment
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: nginx
      template:
        metadata:
          labels:
            app: nginx
        spec:
          containers:
          - name: nginx
            image: nginx:1.21.4
            ports:
            - containerPort: 80
    ```
4. Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Assignment 2: Execution and Observation
Let's tell the API Server to make this reality.

1. Apply the manifest:
   `kubectl apply -f my-deployment.yaml`

2. **Observation:** The API Server responds with `deployment.apps/nginx-deployment created`.

3. Check the status of your Deployment:
   `kubectl get deployments`
4. Check the status of the ReplicaSet that the Deployment automatically created:
   `kubectl get replicasets`
5. Check the status of the Pods that the ReplicaSet created:
   `kubectl get pods`
6. **Result:** You should see 3 Pods, all in a `Running` state!

## Assignment 3: Chaos Engineering (Self-Healing)
Let's simulate a server crashing.

1. List your pods again, and copy the exact name of ONE of the pods (e.g., `nginx-deployment-7848d4b86f-abcde`):
   `kubectl get pods`

2. Delete that specific pod manually:
   `kubectl delete pod <PASTE-YOUR-POD-NAME-HERE>`

3. **IMMEDIATELY** run `kubectl get pods` again. 
4. **Result:** You will see the pod you deleted marked as `Terminating`. But look closely! You will see a brand new, 4th pod in a `ContainerCreating` state. The moment the ReplicaSet noticed a pod died, it instantly spawned a replacement to maintain the desired state of 3!

## Assignment 4: Cleanup

1. Delete the entire Deployment (which will automatically delete the ReplicaSet and all Pods):
   `kubectl delete -f my-deployment.yaml`

## Success Criteria
You have successfully completed this practice if you applied a Deployment YAML, observed the creation of 3 Pods, deleted one Pod manually, and verified that the ReplicaSet instantly self-healed the cluster by spawning a replacement.
