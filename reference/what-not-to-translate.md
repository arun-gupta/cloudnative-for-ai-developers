# What not to translate

A few places where cloud native dogma either bends or breaks for AI workloads. Knowing these makes you fluent, not just compliant.

- **Stateless is not the default for AI.** Twelve-factor assumes workloads are stateless and can be rescheduled cheaply. Models are big, slow to load, and warm slowly. Cold start is a real cost, not a footnote.
- **Pods are not always ephemeral.** A serving replica with a 70B model in GPU memory is not "interchangeable" the way a stateless Go service is. Treat it that way operationally, but build for graceful drain.
- **Microservices is not always the right shape.** An agent pipeline can be a graph inside one process or a fleet of services. The right boundary depends on failure isolation, scaling needs, and latency, not on a default.
- **Horizontal scaling has a ceiling at GPU prices.** Sometimes the answer is one bigger box, not more small ones.
- **Scale-to-zero is often the wrong choice.** Defensible for small CPU workloads, expensive for big models. Most AI workloads want a warm minimum, not a cold zero.
- **CRDs are not free.** A new operator is a new dependency. Use the upstream one (KubeRay, Kubeflow, KServe) before you write your own.

---

[Back to landscape](../README.md)
