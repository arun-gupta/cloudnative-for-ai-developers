# Before: the raw way

Submit Jobs directly. No queue, no priority, no visibility.

## What you'll observe

Three jobs compete for two available CPU slots. One sits `Pending`. You don't know:

- Which experiment will start next
- When the pending job will run
- Whether a critical production job could ever jump ahead
- Who else is consuming cluster resources and why

This is exactly what happens with GPUs on a shared cluster. Replace "1 CPU" with "1 A100" and the experience is identical.

Each job runs 20 epochs at 10 seconds each (~200 seconds total). `experiment-c` waits the full duration of two jobs before it can start. On a real GPU cluster each epoch might take 30-60 minutes, so the same wait is measured in hours, not minutes. The simulation compresses that to something you can observe in a single terminal session.

## Prerequisites

- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- A running Kind cluster (`kind create cluster` if you don't have one)

## Run it

First, apply the namespace quota. This simulates a shared cluster where your team's allocation is 2 GPU slots. On a well-resourced machine (M4, 32-core workstation) the jobs would otherwise all schedule immediately and the pain wouldn't land.

```bash
kubectl apply -f quota.yaml
```

> **Note:** the quota is a simulation device. In this demo it stands in for a real shared GPU cluster where someone else already holds most of the allocation. It is not something you'd add to fix the problem — that's what Kueue does in the `after/` folder.

Apply the three jobs at once:

```bash
kubectl apply -f jobs.yaml
```

Watch what happens:

```bash
kubectl get pods -w
```

You'll see two pods reach `Running` and one sit `Pending`:

```
experiment-a-xxxxx   0/1   Pending   0          0s
experiment-b-xxxxx   0/1   Pending   0          0s
experiment-c-xxxxx   0/1   Pending   0          0s
experiment-a-xxxxx   1/1   Running   0          2s
experiment-b-xxxxx   1/1   Running   0          3s
```

`experiment-c` never moves. You don't know when it will.

## The questions you can't answer

```bash
# How many jobs are waiting?
kubectl get pods --field-selector=status.phase=Pending
# Tells you count. Tells you nothing about order or estimated start time.

# Which team is using all the resources?
kubectl get pods -A --field-selector=status.phase=Running
# Tells you pods. Tells you nothing about quotas or allocations.

# Can I preempt a lower-priority job for my production workload?
# No mechanism to express priority at all.
```

## Clean up

```bash
kubectl delete -f jobs.yaml
kubectl delete -f quota.yaml
```

## What this costs in the real world

- A researcher submits a 20-hour training run and waits 6 hours in `Pending`.
- A production fine-tune that needs to ship by morning is stuck behind weekend experiments.
- No one knows whose job to cancel to unblock the queue.
- The cluster has idle capacity on a different node pool, but no one thought to check.

The cloud native answer: a queue with declared quotas, priorities, and fair sharing so every job has a visible position and an expected start time.

The [after/](../after/) folder shows how Kueue provides all of that.
