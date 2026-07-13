---
volume: 4
chapter: 4
part: 1
id: V4-C04
title: Stateful Applications in K8s
author: Laxman Aryal
edition: First Edition
reviewed_by:
  - Technical Review Pending
version: 0.1
difficulty: Advanced
estimated_time: 1.5 Hours
reading_time: 25 Minutes
labs: 1
interview_questions: 3
prerequisites: V4-C03
last_updated: 2026-07
status: In Progress
learning_outcomes: To be updated
career_level: Associate to Professional
enterprise_relevance: High
---

# Chapter 4 — Stateful Applications in K8s

## Learning Objectives

Containers are ephemeral, but databases are forever. In this chapter, we tackle the complexities of StatefulSets and PersistentVolumes, ensuring data survives even when Pods die.

By the end of this chapter, you will be able to:
* Explain the difference between Stateless and Stateful applications.
* Define PV (PersistentVolume) and PVC (PersistentVolumeClaim).
* Decouple configuration from code using ConfigMaps.
* Securely inject sensitive data into Pods using K8s Secrets.

## Visual Architecture: Decoupling State from Compute

In Volume 3, we learned that containers are ephemeral. If a database container dies, you lose its data unless you attach a Volume. 
Kubernetes takes this concept further. Because Pods can be scheduled on *any* node in the cluster at any time, local hard drives are basically useless. Kubernetes forces you to fully decouple your Data (State) and your Configuration from the actual compute Pods. 

```mermaid
flowchart TD
    subgraph K8s Control Plane
        A["ConfigMap \n (Non-sensitive Configs) "]
        B["Secret \n (Passwords/Keys) "]
    end
    
    subgraph External Cloud Storage
        C["AWS EBS Volume \n (PersistentVolume) "]
    end
    
    subgraph Ephemeral Pod
        D["Application Container "]
    end
    
    A -->|"Mounted as Environment Variables "| D
    B -->|"Mounted as Secure File "| D
    C -->|"Mounted via PVC to /var/lib/data "| D
    
    style A fill:#f39c12,stroke:#f1c40f,color:#000
    style B fill:#d63031,stroke:#ff7675,color:#fff
    style C fill:#00b894,stroke:#55efc4,color:#000
    style D fill:#0984e3,stroke:#74b9ff,color:#fff

```

## Theory & Concepts

### 1. PV and PVC
* **PersistentVolume (PV):** A piece of physical storage in the cluster (like an NFS share or an AWS EBS volume). It exists independently of any Pod.
* **PersistentVolumeClaim (PVC):** A request for storage by a user. A developer writes a PVC saying, "I need 10GB of fast SSD." The K8s Control Plane automatically finds a matching PV and binds them together. The Pod then mounts the PVC. If the Pod dies, the PVC and PV remain completely safe.

### 2. ConfigMaps
Applications often behave differently depending on the environment. In Dev, the logging level should be `DEBUG`. In Prod, the logging level should be `ERROR`. 
Instead of building two different Docker images, you build one image and inject a **ConfigMap**. The ConfigMap acts as a dictionary of key-value pairs that are injected into the Pod at runtime as Environment Variables or configuration files.

### 3. Secrets
A K8s Secret is exactly like a ConfigMap, but it is meant for sensitive data (API keys, database passwords). Kubernetes base64-encodes the data and stores it securely in `etcd`. 

## Scenario-Based Troubleshooting

### Scenario A: The Hardcoded Secret

> [!IMPORTANT]  
> **Incident Report: The Hardcoded Secret**  
> **Reporter:** Security Operations Center (SOC)  
> **SOP execution:**
>
>
> 1. **11:00 AM — Incident Receipt:** SOC flags a critical vulnerability: `DB_PASSWORD: "SuperSecretAdminPassword123"` was committed to the public `database-deployment.yaml` file in GitHub.
>
> 2. **11:05 AM — Triage & Containment:** The engineer immediately connects to the production database directly and manually rotates the password, breaking the application temporarily to secure the data.
>
> 3. **11:08 AM — Investigation:** The engineer confirms that anyone with repo access could read the plaintext password. The deployment must be updated to use a secure object.
>
> 4. **11:10 AM — Root Cause:** A junior developer hardcoded the password directly in the Kubernetes Deployment manifest instead of using a Kubernetes Secret.
>
> 5. **11:12 AM — Resolution:** The engineer creates a Kubernetes Secret directly in the cluster (`kubectl create secret generic db-passwords --from-literal=DB_PASSWORD='NewSecurePassword456'`). They then modify the deployment YAML to inject the password via `valueFrom: secretKeyRef` and apply it.
>
> 6. **11:15 AM — Verification:** The newly deployed Pod successfully connects to the database using the securely injected secret. Total application downtime: 10 minutes.
>
> 7. **Post-Mortem:** Discuss secrets management in Kubernetes and implement a Git hook to scan for plaintext passwords.
>
> 8. **Documentation:** Write a guide on creating and injecting Kubernetes Secrets for the engineering team.

> [!CAUTION]  
> **Best Practice: Secrets are not Encrypted by Default**  
> Kubernetes Secrets are base64-encoded, *not* encrypted. Anyone with `kubectl` access to the namespace can easily decode them by running `echo "password" | base64 --decode`. In true enterprise environments, you must configure Encryption at Rest for the `etcd` database, or use an external KMS (Key Management Service) like HashiCorp Vault.

## Hands-on Lab

> [!TIP]
> **Practice Assignment Available**
> Proceed to the [Chapter 4 Practice Guide](../practice-files/V4-C04-practice.md) to create a K8s Secret and securely mount it into a Pod!

## Interview Questions

### Question 1: What is the difference between a PersistentVolume (PV) and a PersistentVolumeClaim (PVC)?
* **Target Answer**: "A PersistentVolume (PV) is the actual physical storage resource in the cluster, such as an AWS EBS volume or an NFS share, provisioned by the cluster administrator. A PersistentVolumeClaim (PVC) is a request made by a developer/user for a specific amount of storage and access mode. Kubernetes dynamically binds the PVC to an available PV, allowing a Pod to mount the PVC and safely write data independent of the Pod's lifecycle."

### Question 2: Why should you avoid storing large, unstructured data in ConfigMaps?
* **Target Answer**: "ConfigMaps are designed for small configuration files and environmental variables, and they are ultimately stored in the `etcd` database. `etcd` has a hard 1MB limit on object size. If you try to store massive data dumps or binary files in a ConfigMap, you will break the cluster's backing store. Large data belongs in Persistent Volumes."

### Question 3: A developer commits a Kubernetes Secret YAML file containing `password: bXlfc2VjcmV0` to a public GitHub repository. They claim it is secure because it is encrypted. Are they correct?
* **Target Answer**: "No, they are fundamentally incorrect. Kubernetes Secrets are base64-encoded, which is a data formatting scheme, not an encryption algorithm. Anyone who finds that string can easily decode it back to plain text (`my_secret`). Secrets should never be committed to source control in plain text or base64 format."

## Common Mistakes & Pro-Tips

> [!WARNING] Common Mistake
> Assuming Kubernetes Secrets are encrypted. By default, Secrets are only base64-encoded, NOT encrypted! Anyone who can run `kubectl get secret -o yaml` can decode it instantly. You must configure Encryption at Rest for `etcd` or use a KMS (Key Management System).

> [!TIP] Pro-Tip
> When injecting ConfigMaps as files via Volume Mounts, Kubernetes automatically updates the mounted files inside the running Pod when the ConfigMap is edited. However, if you inject them as Environment Variables, the Pod must be restarted to pick up the new values!

## Chapter Summary

The true power of Kubernetes is decoupling. By strictly separating Compute (Pods), Networking (Services), Configuration (ConfigMaps), Secrets, and Storage (PVCs), you create highly modular architectures that can survive almost any infrastructure failure.

## Completion Checklist

- [ ] I understand how PVs and PVCs interact.
- [ ] I understand the purpose of a ConfigMap.
- [ ] I know why Secrets should never be hardcoded into Deployment YAMLs.

---

## Navigation

⬅ Previous:
[Chapter 3 – Chapter Title](V4-C03-k8s-networking.md)

🏠 Volume Contents:
[Table of Contents](../TOC.md)

➡ Next:
[Chapter 5 – Chapter Title](V4-C05-helm-package-manager.md)