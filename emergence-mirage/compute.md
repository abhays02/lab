# emergent abilities as a metric artifact: verification

## the open question

Do large language models exhibit genuine, unpredictable phase transitions
in capability as they scale ("emergent abilities"), or is the appearance
of a sudden jump mostly an artifact of the metric used to measure it?

- Wei et al., "Emergent Abilities of Large Language Models" (2022),
  https://arxiv.org/abs/2206.07682 -- introduced and catalogued the
  phenomenon: dozens of tasks where accuracy sits near zero, then jumps,
  as model scale crosses a threshold.
- Schaeffer, Miller & Liang, "Are Emergent Abilities of Large Language
  Models a Mirage?" (NeurIPS 2023), https://arxiv.org/abs/2304.15004 --
  argues the jump often comes from choosing a nonlinear or discontinuous
  metric (like exact-match on a multi-token answer), not from a real
  change in the model.
- Still active, not settled: "Emergent Abilities in Large Language
  Models: A Survey" (March 2025), https://arxiv.org/abs/2503.05788, and
  "Random Scaling of Emergent Capabilities" (Feb 2025),
  https://arxiv.org/abs/2502.17356, both treat the ontological status of
  emergence, and whether it can be predicted before it's observed, as
  open. The 2025 survey states plainly that the debate has not converged.

## what this script actually checks (verified computation, not a claim about real models)

`emergence_mirage.py` builds one smooth, monotonic per-token accuracy
curve p(x) (a logistic in a scale parameter x, standing in for
log-compute or log-parameters). p(x) has no threshold, no plateau, no
special point anywhere -- constant curvature in logit space by
construction.

It then asks: if a task requires k of these per-token predictions correct
simultaneously (exact-match accuracy = p(x)^k, the metric Schaeffer et al.
identify as the common culprit), what does the SAME underlying curve look
like for different k?

Result (exact, not simulated with noise):

| k   | per-token accuracy needed for 50% exact-match | x where exact-match crosses 50% | 10%->90% x-width |
|-----|-----------------------------------------------|----------------------------------|-------------------|
| 1   | 50.0%                                          | 5.00                              | 3.66               |
| 5   | 87.06%                                          | 6.59                              | 2.76               |
| 20  | 96.59%                                          | 7.79                              | 2.62               |
| 50  | 98.62%                                          | 8.56                              | 2.59               |
| 100 | 99.31%                                          | 9.14                              | 2.58               |

The underlying model trend never changes. Only k changes. Going from
k=1 to k=100 pushes the visible "jump" 83% further along the scale axis
(x=5.00 to x=9.14) and needs the model to go from 50% to 99.31% per-token
accuracy before the multi-step metric shows anything, because
0.5^(1/100) = 0.9931. That's arithmetic, not a property of any model.

## classification (per the validation gate)

- ESTABLISHED (cited): the metric-artifact mechanism itself -- Schaeffer,
  Miller & Liang (2023), above.
- VERIFIED (this session's computation): the exact numbers in the table
  above, reproduced from a from-scratch numpy model, not copied from the
  paper.
- OPEN, NOT CLAIMED SOLVED: whether every empirically reported "emergent
  ability" in a real trained model is fully explained by this mechanism,
  versus some being a genuine phase transition the metric artifact alone
  doesn't account for. The 2025 survey and follow-up papers above treat
  this as unresolved. This post does not claim to resolve it -- it shows
  precisely how strong the artifact can be, which is one piece of the
  argument, not the whole argument.

## reproduce

```
python3 emergence_mirage.py
```

No external data, no network calls. Pure numpy, deterministic.
