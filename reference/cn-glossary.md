# CN primitives glossary

When you read the pain files you will hit lower-level CN terms that have no direct ML equivalent. The tables below give a one-line definition for each, grouped by the problem it addresses.

---

### Compute and scheduling

| Term | What it means |
|---|---|
| Pod | A single running instance of one or more containers, the smallest deployable unit in Kubernetes |
| Replica | A running copy of a service; more replicas means more capacity and fault tolerance |
| ReplicaSet | A controller that ensures exactly N replicas of a pod are running at all times |
| DaemonSet | Runs exactly one pod on every node in the cluster, used for node-level agents like log collectors |
| Namespace | A virtual partition inside a cluster that isolates one team's workloads from another's |
| PriorityClass | A label that ranks jobs so high-priority workloads are scheduled before lower-priority ones |
| Gang scheduling | A policy that starts all pods of a job simultaneously or holds them all back; prevents partial-start deadlocks in distributed training |
| GPU node pools | Groups of machines dedicated to GPU workloads, kept separate from CPU-only nodes |

### Storage

| Term | What it means |
|---|---|
| PersistentVolume / PVC | Durable network-attached storage that survives pod restarts; PVC is the claim a pod makes against a PersistentVolume |
| Init container | A short-lived container that runs and completes before the main container starts, used to stage data, fetch config, or check dependencies |

### Networking and security

| Term | What it means |
|---|---|
| Service mesh | A network layer (e.g., Istio, Linkerd) that controls, observes, and secures traffic between services without changing application code |
| mTLS | Mutual TLS; both sides of a connection present certificates so each verifies the other's identity |
| RBAC | Role-Based Access Control; defines which users and service accounts can perform which actions on which resources |
| NetworkPolicy | Firewall-like rules that restrict which pods can send or receive traffic from which other pods |
| External Secrets | An operator that pulls secrets from external vaults (AWS Secrets Manager, HashiCorp Vault, etc.) into the cluster at runtime |

### Autoscaling

| Term | What it means |
|---|---|
| HPA (Horizontal Pod Autoscaler) | Automatically adds or removes pod replicas based on CPU, memory, or custom metrics |
| KEDA | Extends HPA to scale on external event sources such as queue depth, Kafka lag, or HTTP request rate |
| Cluster autoscaler | Adds nodes when pods are pending due to insufficient capacity and removes idle nodes to cut cost |

### ML-specific operators and tools

| Term | What it means |
|---|---|
| NCCL | NVIDIA Collective Communications Library; handles GPU-to-GPU data transfer (all-reduce, broadcast) during distributed training |
| Rank | Each worker's integer ID in a distributed training job; rank 0 is typically the coordinator that aggregates gradients |
| Training operator | A Kubernetes controller (PyTorchJob, MPIJob, KubeRay) that manages distributed training jobs, coordinates workers, and handles restarts |
| RDMA | Remote Direct Memory Access; high-speed network transfer that bypasses the CPU and OS for lower latency between nodes |
| GPUDirect | NVIDIA technology enabling direct GPU-to-GPU data transfer over the network fabric without staging through host memory |
| MIG | Multi-Instance GPU; an NVIDIA feature that partitions one large GPU into isolated virtual GPUs with guaranteed resources |
| MPS | Multi-Process Service; NVIDIA technology that shares GPU execution resources across multiple processes to improve utilization |

### Deployment strategies

| Term | What it means |
|---|---|
| Canary deployment | Routes a small percentage of live traffic to the new version while the old version handles the rest; roll back if errors spike |
| Blue-green deployment | Runs the old version (blue) and new version (green) in parallel, then switches all traffic at once with an instant rollback path |
| Argo Rollouts / Flagger | Kubernetes controllers that automate canary and blue-green deployments, including metric-gated promotion and automatic rollback |

---

[Back to Rosetta table](rosetta-table.md) | [Back to landscape](../README.md)
