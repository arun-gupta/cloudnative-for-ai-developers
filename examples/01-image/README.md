# Pain 1 example: from script to container

A working demonstration of [Pain 1: Model works locally, breaks in prod](../../pains/01-model-works-locally.md). Same Python code, two deployment styles. The Dockerfile is the only thing that changes. And it changes everything.

## What's here

```
01-image/
├── before/        # the typical Python-script-on-a-VM way
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
└── after/         # the cloud native way
    ├── app.py     # IDENTICAL to before/app.py
    ├── requirements.txt   # IDENTICAL too
    ├── Dockerfile
    ├── .dockerignore
    ├── build.sh
    └── README.md
```

The model: `sentence-transformers/all-MiniLM-L6-v2`. About 22MB. The app exposes `POST /embed`.

## The point of the diff

`before/app.py` and `after/app.py` are byte-for-byte identical. So are `requirements.txt`. **Going cloud native is not rewriting your code; it's wrapping it.** The Dockerfile is the entire delta.

## Before you read the Dockerfile: look at your own mess

Paste this into a terminal. Five seconds. It surfaces the laptop state your "before" deployment depends on without you realizing.

```bash
echo "=== Pythons on PATH ==="; which -a python python3 2>/dev/null | sort -u
echo "=== Active Python ==="; python3 -c "import sys; print(sys.executable, sys.version.split()[0])"
echo "=== HuggingFace cache ==="; du -sh "${HF_HOME:-$HOME/.cache/huggingface}" 2>/dev/null || echo "(no cache yet)"
echo "=== Relevant env vars ==="; env | grep -E '^(CUDA|HF_|TRANSFORMERS_|TORCH_|LD_LIBRARY)' | sort
```

You'll likely see: two or three Pythons (one of which is "active" and isn't the one your editor uses), a multi-gigabyte HF cache full of models you don't remember downloading, and a handful of env vars baked into your shell that don't exist anywhere prod can see.

None of this ships with `git push`.

## Run the two versions

**Before** (typical Python script):

```bash
cd before
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

**After** (container):

```bash
cd after
bash build.sh
docker run -p 8000:8000 embedder:latest
```

Both serve at `localhost:8000/embed`. Same curl, same response. The difference is everything around the response.

See [`before/README.md`](before/README.md) for the failure modes the typical approach hits on a real Linux VM, and [`after/README.md`](after/README.md) for what the Dockerfile actually declares.

## Trade-offs

**What you keep**: your `app.py`, your `requirements.txt`, your model artifacts. All unchanged.

**What you give up**: "it works on my machine" as a defense. The image either runs everywhere or runs nowhere.

---

[← Back to Pain 1](../../pains/01-model-works-locally.md) · [Landscape](../../README.md) · [Examples index](../README.md)
