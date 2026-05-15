# After: the cloud native way

Same `train.py`, with a checkpoint hook. A Kubernetes Job runs it to completion with automatic retries. A PersistentVolumeClaim keeps the checkpoints alive across pod deaths.

Kill the pod mid-run. The Job restarts it. It resumes from the last checkpoint, not from epoch 0.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (tested with 29+)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- A running Kind cluster (`kind create cluster` if you don't have one)
- [kind CLI](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)

## 1. Build and load the image

```bash
./build.sh
```

This builds the Docker image and loads it directly into your Kind cluster. No registry needed.

Verify the image is loaded:

```bash
docker exec -it $(kind get nodes --name $(kind get clusters | head -1)) crictl images | grep training-job
```

## 2. Apply the manifests

```bash
kubectl apply -f pvc.yaml
kubectl apply -f job.yaml
```

The PVC provisions a small volume on the Kind node. The Job starts a pod that mounts it.

## 3. Watch the training run

```bash
kubectl get pods -w
```

Once the pod is `Running`, tail its logs:

```bash
kubectl logs -f job/training-job
```

You'll see:

```
No checkpoint found. Starting from epoch 0.
epoch   0/20  loss=2.3000  (checkpoint saved)
epoch   1/20  loss=1.8769  (checkpoint saved)
epoch   2/20  loss=1.5378  (checkpoint saved)
...
```

## 4. Simulate a crash

While the job is running, open a second terminal and delete the pod:

```bash
kubectl delete pod -l job-name=training-job
```

The Job controller immediately schedules a replacement pod. Watch it appear:

```bash
kubectl get pods -w
```

## 5. Watch the resume

Tail the new pod's logs:

```bash
kubectl logs -f job/training-job
```

You'll see it pick up from the last saved epoch, not from 0:

```
Checkpoint found: epoch 7 loss=0.4823. Resuming from epoch 8.
epoch   8/20  loss=0.3965  (checkpoint saved)
epoch   9/20  loss=0.3267  (checkpoint saved)
...
```

That's the point. A real GPU job at hour 14 would resume from hour 13, not hour 0.

## 6. Clean up

```bash
kubectl delete -f job.yaml
kubectl delete -f pvc.yaml
```

## What the Dockerfile declares

- `FROM python:3.11-slim` -- one Python, pinned, no host env
- stdlib only, no pip install needed
- Non-root user
- `/checkpoints` as the volume mount point

The `train.py` in this folder is byte-for-byte identical to `before/train.py` except for the checkpoint logic. **The cloud-native version adds checkpointing and a manifest; it doesn't rewrite your training code.**

## What this maps to on a real GPU cluster

| This demo | Real GPU job |
|---|---|
| `python:3.11-slim` base | CUDA base image (`nvcr.io/nvidia/pytorch:24.05-py3`) |
| Fake loss loop, 3 s/epoch | Actual model forward/backward pass |
| `checkpoint.json` (tiny) | Model weights snapshot (GB-scale) |
| Kind `local-path` PVC | EBS, GCS Filestore, EFS, or Lustre PVC |
| `kubectl delete pod` | Spot-instance preemption, OOM kill, node failure |
| `backoffLimit: 4` | Same -- adjust to your expected failure rate |

---

[← Back to Pain 2](../../pains/02-gpu-job-crashed.md) · [Landscape](../../README.md) · [Examples index](../README.md)
