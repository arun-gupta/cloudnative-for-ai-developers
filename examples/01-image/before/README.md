# Before: the typical Python-script way

The way most AI/ML developers actually ship things: clone, install, run.

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

```bash
curl -X POST http://localhost:8000/embed \
  -H 'content-type: application/json' \
  -d '{"text": "hello"}'
```

It works.

## What breaks when you ship this to a real machine

You SSH to a Linux VM, `git clone`, `pip install -r requirements.txt`, `python -m uvicorn app:app`. Some of the things that go wrong, in roughly the order you'll discover them:

- **Wrong Python.** The VM has 3.10; your laptop has 3.12. Some wheels match, some don't. `pip install` works; `import` doesn't.
- **Missing system libs.** PyTorch needs `libgomp1` for OpenMP. macOS has the equivalent; minimal Ubuntu images don't. You get `OSError: libgomp.so.1: cannot open shared object file`.
- **The model isn't there.** `sentence-transformers` downloads to `~/.cache/huggingface` on first call. The VM has no cache. The first request takes 30+ seconds, or fails if the VM has no internet.
- **Pip versions drift.** Your `requirements.txt` pins `sentence-transformers==3.2.1`, but that pulls a transitive dependency whose wheel differs between macOS-arm64 and linux-x64.

These are the visible failures. The invisible ones are worse: env vars set in your `.zshrc` that don't exist on the VM, HF tokens at `~/.huggingface/token` that aren't there either, model weights and data files at hardcoded paths.

The [after/](../after/) folder shows how the Dockerfile makes all of this moot.
