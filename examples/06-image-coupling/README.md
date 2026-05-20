# Example 06: Server image coupling

Demonstrates the pain and the fix from [Pain 6: My server image bakes in the weights source](../../pains/06-server-image-coupling.md).

| | Before | After |
|---|---|---|
| Source URL | Hardcoded constant in `server.py` | ConfigMap, injected into init container |
| Credentials | Hardcoded constants in `server.py` | Secret, injected into init container only |
| Rotate the key | Edit code + rebuild image | `kubectl apply` on the Secret, recycle pod |
| Change the bucket | Edit code + rebuild image | `kubectl apply` on the ConfigMap, recycle pod |
| Credentials in registry | Yes | No |

## Structure

```
before/
  server.py       # serving + download with hardcoded source URL and credentials
  weights.txt     # fake model weights used by the demo

after/
  server.py       # serving code only
  downloader.py   # init container -- reads source URL and credentials from env vars
  Dockerfile
  build.sh
  configmap.yaml  # WEIGHTS_SOURCE
  secret.yaml     # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
  pod.yaml        # PVC + init container + server container
  weights.txt     # fake model weights bundled into the init container image
```

## Run the before

No Docker or Kubernetes needed:

```bash
cd before && python3 server.py
```

## Run the after

Requires Docker, kubectl, and kind:

```bash
cd after && ./build.sh && kubectl apply -f configmap.yaml -f secret.yaml -f pod.yaml
```

See [`after/README.md`](after/README.md) for the full walkthrough, including the key-rotation and source-change demos.

---

[← Back to Pain 6](../../pains/06-server-image-coupling.md) · [Examples index](../README.md)
