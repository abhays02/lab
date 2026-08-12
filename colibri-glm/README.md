# Colibri / GLM

<p align="center">
  <img src="animation.svg" alt="A 744B model streaming experts from storage" width="100%" />
</p>

> **A 744B model. 25GB of RAM. About 11GB of disk reads for one cold token.**

| Measure | Value |
|---|---:|
| Total parameters | 744B |
| Active per token | 40B |
| Active fraction | 5.38% |
| Routed experts | 19,456 |
| Implied experts per layer | ~7.9 |
| Published cold-cache speed | 0.05–0.1 tok/s |

## What you are seeing

```text
744B total
   ↓
40B active
   ↓
5.38% used per token
   ↓
experts stream from storage
   ↓
~11GB cold-token reads
```

## What I checked

- Arithmetic consistency of the published architecture numbers
- Implied active-expert count
- Implied effective read throughput
- Difference from rated sequential NVMe throughput

The last item is an engineering question, not a diagnosis.

## Important boundary

This lab did not benchmark the 372GB model itself. The project facts come from the published Colibri material; the calculations here are independent checks.

## Go deeper

[Open the original visual](frame.html) · [Run the calculation](colibri_math.py) · [Read the evidence](compute.md) · [Inspect output](colibri_math.json)

[Back to the lab](../)
