# Colibri / GLM

<p align="center">
  <img src="frame.html" alt="A 744B model streaming experts from disk" width="100%" />
</p>

> **A 744B model. 25GB of RAM. About 11GB of disk reads for one token.**

### The numbers

| | Value |
|---|---:|
| Total parameters | 744B |
| Active per token | 40B |
| Active fraction | 5.38% |
| Routed experts | 19,456 |
| Implied experts per layer | ~7.9 |
| Published cold-cache speed | 0.05–0.1 tok/s |
| Implied effective read throughput | 0.55–1.1 GB/s |

### What I checked

```text
744B total
   ↓
40B active
   ↓
~5.4% actually used per token
   ↓
experts stream from NVMe
   ↓
~11GB of reads for a cold token
```

The arithmetic is internally consistent with the published architecture numbers.

### What is interesting

The reported effective read rate is roughly **3.2–12.7x below** common rated sequential NVMe throughput.

That is an open engineering question, not a claimed diagnosis.

### Important distinction

- The Colibri / GLM facts come from the published project and reporting.
- The calculations here were independently checked.
- This lab did not benchmark the 372GB model itself.

### Reproduce

```bash
python colibri_math.py
```

Then inspect:

- `colibri_math.json` — arithmetic validation
- `frame.html` — visual explainer
- `compute.md` — sources and provenance

[Back to the lab](../)
