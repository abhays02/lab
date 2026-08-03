# compute.md — colibri-glm

## Claim classification

**Established (published by the project/press, not re-run here):**
- Colibri is a real, open-source inference engine (pure C, zero
  dependencies) that runs GLM-5.2, a 744B-parameter Mixture-of-Experts
  model, on consumer hardware with as little as 25GB RAM and no GPU, by
  streaming routed experts from an NVMe SSD instead of holding the full
  model in memory. Released July 2026 by developer JustVugg.
  Source: github.com/JustVugg/colibri (README).
- GLM-5.2: 744B total parameters, ~40B active per token, 19,456 routed
  experts across 75 MoE layers, ~19MB per expert at int4 quantization.
  Dense portion (~17B params: attention, shared experts, embeddings)
  stays resident in RAM at int4 (~9.9GB); the 19,456 routed experts
  (~370GB total) stream from disk on demand.
- Reported cold-cache decode speed on a 25GB dev box: 0.05-0.1 tokens/sec.
  Reported ~11GB of disk reads per cold token.
  Corroborated by independent coverage (GIGAZINE, Better Stack, dev.to,
  2.9k GitHub stars, 859-point/214-comment Hacker News thread as of
  2026-08-03).

**Verified this run (arithmetic on the published numbers, not a
benchmark run on local hardware -- the model is 372GB and no such
machine is available in this environment):**
- Active-parameter fraction: 40B / 744B = 5.38%.
- Cross-checked the reported "~11GB per cold token" figure against the
  architecture numbers: 11GB / (75 layers x 19MB/expert) implies ~7.9
  experts activated per layer per token, consistent with the common
  top-8 MoE routing scheme (predicts 11.13GB at exactly top-8). The
  published figures are internally consistent.
- Converted the reported 0.05-0.1 tok/s into per-token wall time: 10 to
  20 seconds per token. Dividing the reported 11GB by that range gives
  an implied effective disk-read throughput of 0.55 to 1.1 GB/s during
  cold decode.
- Compared that against typical consumer NVMe rated sequential read
  speed (widely published Gen3/Gen4 spec range: 3.5-7.0 GB/s). The
  implied throughput is 3.2x to 12.7x below the drive's own rated spec.
  Presented as an open question, not a claimed answer: the project's own
  materials don't break down whether scattered reads, page-cache misses,
  or CPU-bound routing/compute is the dominant cause.

## Sources checked live this run

- github.com/JustVugg/colibri (primary source, README)
- gigazine.net/gsc_news/en/20260710-colibri-glm
- betterstack.com/community/guides/ai/colibri-glm
- Hacker News discussion (859 points, 214 comments as of this check)
- General NVMe sequential-read spec range: published PCIe Gen3/Gen4
  consumer drive specifications.

## Artifacts

- colibri_math.py — arithmetic validation script (pure Python).
- colibri_math.json — its output.
