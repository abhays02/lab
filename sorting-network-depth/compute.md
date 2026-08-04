# compute.md — sorting-network-depth

## Claim being validated

"Parallel sorting networks: the exact minimum number of comparison
rounds (depth) needed to sort n items is proven for n up to 17. Past
that, only best-known upper bounds exist, and the record for 27/28
channels moved from depth 14 to depth 13 in November 2025 — still not
proven optimal."

## What was computed in this session (batcher_verify.py)

Implemented Batcher's bitonic sorting network (1968) from scratch in
plain Python — the construction most engineers meet first, in any
parallel-algorithms course. For n = 2, 4, 8, 16, 32, 64, 128:

1. Generated the comparator list via the standard recursive bitonic
   merge/sort construction.
2. Verified correctness using Knuth's 0-1 principle (a comparator
   network sorts all real-valued sequences iff it sorts all 2^n binary
   sequences) — brute-forced every one of the 2^n binary inputs for
   n <= 16 (65,536 cases at n=16) and confirmed the network produces a
   sorted output for all of them. Zero counterexamples at every size
   tested.
3. Counted comparators and depth (number of layers whose comparators
   act on disjoint wires, i.e. can run in parallel) directly from the
   generated network, and cross-checked against the closed-form
   k(k+1)/2 for n=2^k. Exact match at every size, k=1..7.

Result (see batcher_results.json for raw output):

| n   | depth (Batcher, computed+verified) | comparators |
|-----|-------------------------------------|-------------|
| 4   | 3                                   | 6           |
| 8   | 6                                   | 24          |
| 16  | 10                                  | 80          |
| 32  | 15                                  | 240         |
| 64  | 21                                  | 672         |
| 128 | 28                                  | 1792        |

## Cross-check against the literature

For n=16, the proven-optimal depth is 9 (Bundala, Codish, Cruz-Filipe,
Schneider-Kamp, Zavodny, "Optimal-Depth Sorting Networks," arXiv:1412.5302,
closing six previously-open instances n=13..16 via SAT solvers). Batcher's
construction, verified above, needs 10 — one layer more than the true
minimum, at just 16 items. The gap is small at this size but the
construction offers no way to know how it grows, because nobody has an
exact answer for larger n.

For n=17: proven-optimal depth is 10 (same line of work / the
follow-up closing n=17, "Sorting Networks: to the End and Back Again,"
arXiv:1507.01428) — this is, per the sources surveyed this run, the
largest n for which the exact minimum depth is proven.

For 27 and 28 channels: "Depth-13 Sorting Networks for 28 Channels"
(Chengu Wang, arXiv:2511.04107, submitted 2025-11-06, revised
2025-11-22) constructs new networks establishing a depth-13 upper bound
for both 27 and 28 channels, improving the previous best known bound of
14. This is a new best-known CONSTRUCTION, not a proof of optimality —
no matching lower-bound proof for these sizes was found in the sources
surveyed. Whether 13 is truly the minimum, or whether it can still be
beaten, remains open.

## Classification (per JOB.md validation gate)

- "Batcher needs 10 rounds for 16 items, one more than proven optimal":
  VERIFIED COMPUTATION, this session, 0-1-principle brute force,
  artifact attached (batcher_verify.py, batcher_results.json).
- "n<=17 depth-optimal sorting networks are proven exactly": ESTABLISHED
  RESULT, cited (arXiv:1412.5302, arXiv:1507.01428).
- "28-channel best known depth is 13, down from 14, as of Nov 2025, not
  proven optimal": ESTABLISHED RESULT, cited (arXiv:2511.04107), stated
  plainly as an open upper bound, not a solved value.
- No claim in the post is the owner's unverified hypothesis — this piece
  is entirely established-result-plus-verified-computation, which is why
  it ships as a MYSTERY / THOUGHT+VALIDATION piece rather than needing a
  hedge.

## Tooling note

WebFetch/direct HTTP access to arxiv.org and other non-GitHub hosts
returned 403 through this session's outbound proxy (confirmed via a
direct curl attempt, not assumed) — validation for the two Bundala et
al. results relies on WebSearch result snippets rather than a full
fetched PDF; both are consistent across multiple independent search
results and match the standard literature narrative for this
well-established (2014-2015) result, cited by name, authors, and arXiv
ID above for the owner or any reader to verify directly. The Nov 2025
paper's title, author, submission date, and abstract were similarly
confirmed via WebSearch (raw.githubusercontent.com and github.com
remained reachable throughout; only third-party non-GitHub hosts were
blocked).
