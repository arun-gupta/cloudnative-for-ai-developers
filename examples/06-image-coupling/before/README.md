# Before: source URL and credentials baked into the server image

`server.py` hardcodes `WEIGHTS_SOURCE`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` as constants. The download logic lives in the same file as the serving logic.

This is the natural starting point. When you containerize this, those constants end up in the image -- either as `ENV` instructions in the Dockerfile or as values in the source file copied into it. Either way they travel with the image: cached in your registry, your CI system, and on every node that ever pulled it.

The rebuild tax shows up as soon as anything operational changes:

| Change | Requires image rebuild? |
|---|---|
| Rotate the access key | Yes |
| Move weights to a new bucket | Yes |
| Switch from S3 to GCS | Yes |
| Fix a bug in the serving logic | Yes (of course) |

## Run it

No dependencies beyond the standard library.

```bash
cd examples/06-image-coupling/before
python3 server.py
```

## Expected output

```
[startup] Connecting to .../before/weights.txt
[startup] Using key: AKIAIOS... (hardcoded in this file)
[startup] Weights staged in 0.000s -> /tmp/weights.txt
[startup] Model loaded. Preview: these are fake model weights...
[startup] To change the source or rotate the key, edit this file and rebuild.
[ready] Inference server listening on port 8080
[ready]   GET /health  -> liveness check
[ready]   GET /predict -> simulated inference
```

In another terminal:

```bash
curl localhost:8080/predict
```

```
prediction using model: [these are fake model weights
layer_0: 0.312 0.847 0.193 0.65...]
```

## The problem

The access key in `server.py` is now in your image. To rotate it you edit the file, commit, rebuild, re-push, and redeploy -- even though nothing about the serving logic changed. The [`after/`](../after/) example shows how a ConfigMap and a Secret decouple these concerns so neither the key nor the bucket URL ever lives in the image.
