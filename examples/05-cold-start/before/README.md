# Before: weight download baked into the server

`server.py` downloads the "model weights" file from a hardcoded URL on startup. The source URL and all download logic live inside the server code.

This is the natural starting point. Most model servers begin this way: a startup script that downloads weights from a hardcoded URL (an S3 bucket, a GCS path, a HuggingFace repo ID) before launching the server. It works fine until you need to change the source. Switch from S3 to GCS, move to a different bucket, or pull from HuggingFace instead. You are rebuilding and re-pushing the entire server image.

## Run it

No dependencies beyond the standard library.

```bash
python3 server.py
```

## Expected output

Startup:

```
[startup] Downloading weights from https://raw.githubusercontent.com/arun-gupta/the-pain-first-way/main/examples/05-cold-start/after/weights.txt ...
[startup] Weights downloaded in 0.45s -> /tmp/weights.txt
[startup] Model loaded. Weights preview: these are fake model weights...
[ready] Inference server listening on port 8080
[ready]   GET /health  -> liveness check
[ready]   GET /predict -> simulated inference
```

In another terminal:

```bash
$ curl localhost:8080/predict
prediction using model: [these are fake model weights
layer_0: 0.312 0.847 0.193 0.65...]
```

## The problem

To change the weights source (switch from this URL to an S3 bucket, a GCS path, or HuggingFace), you edit `WEIGHTS_URL` in `server.py` and rebuild the image. The download source and the serving logic are coupled in the same file and the same container image. That coupling is what the [`after/`](../after/) example eliminates.
