---
name: kubernetes-k8s-suite
description: "Master unified Kubernetes (K8s) suite. Integrates cluster operations, troubleshooting pods (CrashLoopBackOff, Pending, OOMKilled), declarative manifest generation, Helm chart authoring, and ingress/networking setup."
use_when: "Troubleshooting workloads or authoring Kubernetes and Helm configuration."
avoid_when: "Making unapproved production changes or working outside Kubernetes."
entry_inputs: "Cluster/context, namespace, workload symptoms, manifests, and authorization."
workflow: "Inspect read-only state first, isolate cause, propose minimal change, validate safely."
verification: "Run manifest validation and targeted checks; verify rollout only when authorized."
exit_output: "Root cause or manifest changes with risk and verification evidence."
category: "cloud-and-security"
tools:
  - kubectl
  - helm
---

# Kubernetes (K8s) Suite (Unified Master Skill)

A comprehensive operations and troubleshooting suite for Kubernetes workloads, Helm packaging, and declarative manifests.

## 1. Operations Decision Tree

```
[Kubernetes task or issue]
   |
   +---> Is a pod failing, crashing, or stuck?
   |        └──> Use `k8s-debug` protocol (check Events, Describe, Logs, Resource limits).
   |
   +---> Need to package a service for multi-environment rollout?
   |        └──> Use `helm-generator` (parameterized `values.yaml`, helpers, templates).
   |
   +---> Need clean standalone YAML (Deployment, Service, ConfigMap, Ingress)?
   |        └──> Use standard declarative Kubernetes manifest generation.
   |
   +---> Need cluster security policies and RBAC?
            └──> Apply Pod Security Standards, NetworkPolicies, and least-privilege RoleBindings.
```

## 2. Pod Troubleshooting Protocol (`k8s-debug`)

Execute commands in strict diagnostic order:

```bash
# Step 1: Check pod status and restart count
kubectl get pods -n <namespace>

# Step 2: Inspect events (reveals ImagePullBackOff, scheduling failures, PVC mount issues)
kubectl describe pod <pod-name> -n <namespace>

# Step 3: Check application stdout/stderr
kubectl logs <pod-name> -n <namespace> --tail=100

# Step 4: If pod crashed, check previous instance logs
kubectl logs <pod-name> -n <namespace> --previous
```

### Common Failure Modes & Quick Fixes
- **`CrashLoopBackOff`**: Application threw an uncaught error at boot or failed health check probe (`livenessProbe` timing). Check `--previous` logs.
- **`OOMKilled`**: Pod exceeded `resources.limits.memory`. Increase memory limits or inspect memory leaks.
- **`Pending`**: Insufficient CPU/Memory on nodes, unsatisfied node selector, or unattached PersistentVolumeClaim.

## 3. Production Deployment Skeleton

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  labels:
    app: api-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
    spec:
      containers:
      - name: api
        image: myregistry.com/api:v1.2.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 10
```
