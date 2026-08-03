# compute.md — double-descent

## Claim classification

**Established (cited, not this run's finding):**
- Double descent itself: test risk falls, rises sharply near the
  interpolation threshold, then falls again as model capacity keeps
  growing past it. Belkin, Hsu, Ma, Mandal, "Reconciling modern
  machine-learning practice and the classical bias-variance trade-off,"
  PNAS 116(32), 2019 (10.1073/pnas.1903070116) — names the phenomenon,
  shows it in random forests and neural nets.
- The specific minimal model used here (random-feature / linear
  regression, minimum-norm solution, sharp peak exactly at p = n):
  Belkin, Hsu, Xu, "Two Models of Double Descent for Weak Features,"
  arXiv:1903.07571 (2019); and Hastie, Montanari, Rosset, Tibshirani,
  "Surprises in High-Dimensional Ridgeless Regression," arXiv:1903.08560
  (Annals of Statistics, 2022) — proves the minimum-norm least-squares
  risk diverges as p approaches n in the noiseless limit, and spikes to a
  large finite value with additive noise, which is exactly the shape
  reproduced below.
- Extension to deep, non-linear models (model-wise, epoch-wise,
  sample-wise double descent in CNNs, ResNets, transformers): Nakkiran,
  Kaplan, Bahri, Belkin, Yang, Barak, Sutskever, "Deep Double Descent,"
  arXiv:1912.02292 (2019).

**Verified this run (own computation, artifact attached, not previously
claimed as new):**
- Wrote double_descent.py from scratch in plain numpy: 100 fixed training
  points, random-Fourier-feature regression (cos(Wx+b) features on top of
  a 20-dim linear ground truth plus noise), fit via the minimum-norm
  least-squares solution (np.linalg.lstsq) at every feature count p,
  never switching methods between the underparameterized and
  overparameterized regimes.
- Swept p from 5 to 2000, averaged over 30 random trials per p (fresh
  ground-truth vector, fresh random features, fresh noise each trial).
  Full results: double_descent_log.json.
- Result: test MSE falls from 1.209 (p=5) to 1.028 (p=40) in the
  underparameterized regime (mild bias-variance improvement), then
  starts rising again as p approaches n=100 from below (train MSE keeps
  falling to near zero the whole time). At p=100, exactly the
  interpolation threshold, test MSE spikes to 238,807 (mean over 30
  trials) — a near-singular feature matrix chasing noise with nothing
  left to constrain it. One feature past the threshold, at p=101, it is
  already down to 32.9. By p=2000, test MSE settles at 0.464, the lowest
  point in the entire sweep, lower than every underparameterized model
  tested.
- This is a straight, honest reproduction of an established analytic
  result, not a new finding. It was worth doing in-session anyway: the
  magnitude of the spike (238,807, roughly 500,000x the far-overparameterized
  floor) and how fast it collapses (7x in a single added feature, p=100
  to p=101) are not obvious from reading the theorem, only from running
  it.

**Owner's framing (explicitly not asserted as fact):**
- What remains open is not whether double descent happens (established)
  but whether there is one mechanism that explains it across model
  classes rather than a different proof or a different empirical account
  per class. Linear/random-feature models have the analytic account
  above; deep non-linear networks are still explained through several
  partially-overlapping but distinct frameworks published in 2024-2026 (a
  VC-theoretic account, a Bayesian account, a "scale-time equivalence"
  account unifying model-wise and epoch-wise double descent, and a
  2025-2026 extension of the same phenomenon into quantum kernel
  methods) — no single paper unifies all of these as of this writing.

## Sources

- Belkin, Hsu, Ma, Mandal, PNAS 2019, 10.1073/pnas.1903070116
- Belkin, Hsu, Xu, arXiv:1903.07571
- Hastie, Montanari, Rosset, Tibshirani, arXiv:1903.08560
- Nakkiran, Kaplan, Bahri, Belkin, Yang, Barak, Sutskever, arXiv:1912.02292
- VC-theoretic double-descent papers (IEEE Xplore 10508981, Springer
  978-3-032-15120-9_9, both 2025), "Bayesian Double Descent"
  arXiv:2507.07338 (2025), "Unified Neural Network Scaling Laws and
  Scale-time Equivalence" arXiv:2409.05782, "Double Descent in Quantum
  Kernel Methods," PRX Quantum (10.1103/cn64-gs6b)
