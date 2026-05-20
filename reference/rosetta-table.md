# The Rosetta table

For the parts of cloud native that genuinely map one-to-one to something you already do today.

| What you're doing today | What changes in prod | What that's called |
|---|---|---|
| `pip install -r requirements.txt` on a server | Frozen, signed, reproducible artifact | Container image |
| `python train.py` and hoping | Scheduled, checkpointed, retried | Job |
| `uvicorn serve:app` on a VM | Rolling updates, health checks, N replicas | Deployment + Service |
| `.env` with HF_TOKEN | Rotated, audited, scoped per workload | Secret |
| Hyperparameters in argparse | Per-tenant config without rebuilding the image | ConfigMap |
| `ssh` into the GPU box | `kubectl exec` into the pod | (same idea, different door) |
| Ray cluster spun up by hand | Cluster as a declared object | KubeRay / Operator |
| Local model files on disk | Durable storage that survives the pod | PersistentVolume / PVC |
| "Restart if it dies" | Self-healing replicas | ReplicaSet / Deployment |

The table covers what cleanly maps. The [pain sections](../README.md#the-pains) cover what doesn't. For lower-level CN terms with no direct ML equivalent, see the [CN primitives glossary](cn-glossary.md).

---

[Back to landscape](../README.md)
