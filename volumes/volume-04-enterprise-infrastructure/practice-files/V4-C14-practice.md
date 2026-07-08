# Practice Guide: Chapter 14 (Volume 4)

## Objective
To conceptually design a Kubernetes `NetworkPolicy` that implements a Default Deny posture, and then surgically punches a hole for legitimate traffic.

## Assignment 1: The Default Deny
We want to lock down our entire `production` namespace so that no Pods can talk to each other.

1. Open a new file:
   `nano default-deny.yaml`
2. Write the theoretical YAML. Notice that the `podSelector` is completely empty `{}`. This means "select ALL pods in this namespace". 
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: default-deny-ingress
     namespace: production
   spec:
     podSelector: {}
     policyTypes:
     - Ingress
   ```
3. **Analysis:** Because we defined `Ingress` in `policyTypes`, but we did not provide an `ingress` rule block allowing traffic, this policy drops 100% of incoming TCP/UDP traffic to every single pod in the `production` namespace.

## Assignment 2: The Surgical Whitelist
Now that the database is completely isolated (and broken), we need to write a second policy that explicitly allows the API backend to connect to it on port 5432.

1. Open a new file:
   `nano allow-db-traffic.yaml`
2. Write the theoretical YAML. 
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: allow-api-to-db
     namespace: production
   spec:
     podSelector:
       matchLabels:
         app: postgres-database
     policyTypes:
     - Ingress
     ingress:
     - from:
       - podSelector:
           matchLabels:
             app: backend-api
       ports:
       - protocol: TCP
         port: 5432
   ```
3. **Analysis:** Let's break this down line by line.
   * `podSelector: matchLabels: app: postgres-database`: This tells Kubernetes to apply this firewall rule ONLY to the database pods.
   * `ingress: - from: podSelector: matchLabels: app: backend-api`: This is the whitelisting rule. It says "Allow incoming traffic, but ONLY if the traffic originates from a Pod that has the label `app: backend-api`."
   * `ports: port: 5432`: It further restricts the traffic. Even if the backend-api pod tries to connect, it can *only* connect on port 5432. If it tries to SSH on port 22, the packet is dropped.

## Success Criteria
You have successfully completed this practice if you can look at the YAML blocks above and understand exactly why a compromised WordPress container would be unable to ping or connect to the Postgres database in a properly segmented cluster.
