# Contributing

Thanks for reading. This guide gets better when people who've actually hit these pains weigh in.

## Ways to contribute

### Submit a new pain

A pain you've hit that isn't in the guide. Open an issue using the "New pain" template, or open a PR adding a file to `pains/`. The format is: what's happening, the pattern, primitives, what you keep, what you give up.

### Fix or update a primitive

A tool got deprecated, a better one emerged, or the recommendation is off. Open an issue or PR. Don't worry about being polite; corrections are welcome.

### Add a runnable example

The `examples/` directory is filling in pain-by-pain. If you have a working manifest, Helm chart, or script that demonstrates a primitive from one of the pains, open a PR adding it under `examples/<pain-number>-<short-name>/` with a short README explaining what it shows and how to run it.

### Correct something

Typo, broken link, factual error. Just open a PR.

## What I'm looking for

- **Concrete over abstract.** "Job + PVC + checkpoint hooks" beats "use Kubernetes patterns."
- **Actual experience over theory.** Tell me what broke, not what the docs say.
- **Honest scope.** This guide is about cloud native. AI-specific layer concerns (eval, prompts, retrieval) go in the [where CN doesn't help](reference/where-cn-doesnt-help.md) section, not in the pains.

## Style

- Pain-first: lead with the problem, then the answer
- Roughly 150 words per pain section
- Concise over comprehensive
- Plain text, no em-dashes (period or comma instead)

## Pull requests

Small PRs that touch one pain or one reference file are easiest to review. Large structural changes: open an issue first to discuss.

## License

By contributing, you agree your contributions are licensed under Apache-2.0, same as the repo.
