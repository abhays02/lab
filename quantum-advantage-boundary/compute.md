# compute.md — quantum advantage boundary (random circuit sampling)

Validation-gate record for this run's LinkedIn draft. Script:
`rcs_verify.py`. Raw output: `rcs_results.json` (both in this folder).
Run with numpy only, no external quantum-simulation library, seeded
(`np.random.default_rng(20260804)`) for reproducibility.

## The open question (this post's ASK)

Random circuit sampling (RCS) is the leading experimental route to
"quantum advantage": have a quantum processor sample from the output
distribution of a hard-to-simulate random circuit, faster than any known
classical method can. Every RCS advantage claim to date has been
followed, at some distance, by classical algorithms (mostly tensor
network methods) closing part or all of the gap. Whether there is a hard
floor under this, past which classical methods provably cannot follow,
or whether it is an open-ended arms race where the boundary simply moves
with the best available classical algorithm, is not settled. That is the
open problem this post asks about, not "is RCS hard" (which has
theoretical support) but "where, if anywhere, does the classical chase
permanently stop."

## Established results (cited, not computed this run)

- Arute et al., "Quantum Supremacy Using a Programmable Superconducting
  Processor," Nature 574 (2019): Sycamore, 53 qubits, circuit depth 20,
  ~200 seconds on the quantum processor; paper's own classical-runtime
  estimate: ~10,000 years on a then-state-of-the-art supercomputer.
- IBM's rebuttal, same year (2019): a paper arguing an improved classical
  simulation technique using Summit's disk storage could run the
  identical circuit in about 2.5 days, not 10,000 years -- Google's own
  authors acknowledged in the original paper that classical estimates
  would likely fall with better algorithms and hardware.
- Pan and Zhang (2021-2022), tensor-network "spoofing" of the Sycamore
  circuit: generated one million correlated bitstrings for the 53-qubit,
  20-cycle circuit using a 60-GPU cluster over five days, reaching linear
  XEB fidelity 0.739 -- higher fidelity than Google's own quantum run
  achieved (~0.2%).
- ZuChongzhi 2.1 follow-up work: tensor-network methods simulated a
  60-qubit, 24-cycle circuit in 4.2 hours (~1.63x10^18 floating-point
  operations), reaching XEB (3.66 +/- 0.345)x10^-4.
- A new RCS-based advantage claim surfaced this month (reported early
  August 2026, e.g. phys.org and IBM's own quantum blog): a structured
  sampling task said to retain RCS-level hardness while adding
  built-in error detection, completed in roughly 15 minutes on a quantum
  processor, with several current classical simulation approaches
  reported to face "prohibitive" runtimes against it. WebFetch to both
  the phys.org article and the IBM blog post returned HTTP 403 through
  this session's outbound proxy on direct attempt (same restriction
  logged in the 2026-08-04 0430 run for arxiv.org); relied on WebSearch's
  synthesized snippets of both pages, which agree with each other and
  with independent coverage surfaced in the same search. Treated as
  established-but-freshly-reported: the historical pattern (claim, then
  a classical answer arrives later) is what makes this worth watching,
  not a specific number from this newest claim, which is why the post
  below does not lean on unverified specifics from it.

## Verified computation (this run, in-session, numpy)

1. **Porter-Thomas statistics of a simulated random circuit.** Built a
   14-qubit statevector simulator from scratch (no quantum library):
   brick-pattern layers of Haar-random single-qubit SU(2) rotations plus
   CZ entangling gates, alternating even/odd qubit pairs, matching the
   same structural ingredients (random single-qubit gates + fixed
   two-qubit entanglers, brick layout) real RCS circuits use, at a scale
   that is exactly and cheaply simulable. Pooled 6 independent circuit
   instances at 40 layers (98,304 output-probability samples total).
   Scaled probabilities q = dim * p should follow the Porter-Thomas law
   P(q) = e^-q (mean 1, variance 1) if the circuit is scrambling like a
   Haar-random unitary -- this is the same statistical assumption both
   the RCS hardness argument and the cross-entropy benchmarking (XEB)
   verification metric depend on.
   Result at 40 layers: mean(q) = 1.000, var(q) = 1.003 (theory: 1.0),
   Kolmogorov-Smirnov statistic (manual, no scipy) = 0.0011 against the
   theoretical exponential CDF. A near-exact match.
2. **Depth matters -- shallow circuits do not reach it.** Swept circuit
   depth 9/15/20/30/40/60 layers on the same 14-qubit circuit. At 9
   layers: var(q) = 2.357, KS = 0.123 -- a visibly bad fit, the circuit
   has not scrambled enough yet. The fit improves monotonically with
   depth and is essentially exact by 40 layers. This matches the
   published anti-concentration story (circuits need enough depth to
   look Haar-random) as a verified, in-session reproduction, not a new
   claim.
3. **Exact classical memory cost, full statevector.** Pure arithmetic
   (not simulation): bytes = 2^n * 16 (complex128), n = 10..60 qubits.
   At n = 53 (Sycamore's actual qubit count): exactly 144,115,188,075,
   855,872 bytes = 144.12 PB. At n = 60: 18.45 EB. This is the concrete,
   undisputed reason EXACT full-statevector classical simulation is
   infeasible past a modest qubit count -- and exactly why every real
   classical competitor (IBM's Summit estimate, Pan and Zhang's tensor
   network, ZuChongzhi 2.1's tensor network) uses an approximate method
   instead of ever holding the full statevector, which is the actual
   contest, not brute-force storage.
4. **Linear XEB sanity check.** Computed the standard linear XEB
   estimator (F = dim * mean(p_sampled) - 1) on this run's own noiseless
   simulated circuits, sampling 4,000 outcomes per circuit from the true
   distribution. Mean across 6 circuits: 1.012 +/- 0.015. For a perfect,
   noiseless simulation the literature's expected value is 1.0; this
   run's own estimator reproduces that, confirming the XEB computation
   here is implemented correctly, not a new result.

## Claim classification (as used in the post)

- "Sycamore's claim, IBM's 2.5-day rebuttal, Pan and Zhang's spoof, the
  new 2026 claim" -- established result, cited above.
- "144 PB to hold one 53-qubit circuit's full statevector, exactly" --
  verified computation, this run, exact arithmetic (see item 3 above),
  not an estimate.
- "Random circuits need real depth before they look truly random" --
  verified computation, this run (item 2), consistent with published
  anti-concentration results, not this run's own novel claim.
- "Whether there's a permanent floor under quantum advantage, or the
  boundary just keeps moving with the next classical algorithm" -- open
  question, explicitly not resolved by this run or by the cited
  literature. Framed in the post as the open question itself, not as a
  hypothesis or an answer.

No claim in the post is presented as solved. The validation gate is used
here to ground the WHY (exponential classical cost, why depth matters,
why XEB is trustworthy as a metric) in this run's own arithmetic and
simulation, while the actual open question is left open, honestly.
