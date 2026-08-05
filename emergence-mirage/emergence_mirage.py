"""
Reproduces the core mechanism behind Schaeffer, Miller & Liang (2023),
"Are Emergent Abilities of Large Language Models a Mirage?" (arXiv:2304.15004):
a per-token accuracy that improves smoothly and monotonically with a scale
parameter can produce an exact-match accuracy curve that looks like a sharp,
discontinuous "emergent" jump, purely from the metric's nonlinearity
(requiring all k steps of a k-step task correct at once).

Scope of the claim this script supports: it measures, exactly, how strong
that specific metric artifact is and how it scales with task length k. It
does not determine whether every reported emergent ability in real models
is this artifact and nothing else -- that is the part of the debate that
is still open in the 2025 literature (see compute.md for sources).
"""
import numpy as np

def per_token_accuracy(x, x0=5.0, steepness=1.2):
    """Smooth, monotonic logistic improvement in per-token accuracy vs a
    scale parameter x (stand-in for log-compute or log-params). No jump,
    no plateau, no special point -- constant curvature in logit space."""
    return 1.0 / (1.0 + np.exp(-steepness * (x - x0)))

def inv_per_token_accuracy(p, x0=5.0, steepness=1.2):
    return x0 + np.log(p / (1 - p)) / steepness

x = np.linspace(0, 20, 4000)
p = per_token_accuracy(x)

ks = [1, 5, 20, 50, 100]
rows = []
for k in ks:
    p_at_50 = 0.5 ** (1.0 / k)          # per-token accuracy needed for exact-match = 50%
    x_at_50 = inv_per_token_accuracy(p_at_50)
    p10 = 0.10 ** (1.0 / k)
    p90 = 0.90 ** (1.0 / k)
    x10 = inv_per_token_accuracy(p10)
    x90 = inv_per_token_accuracy(p90)
    width = x90 - x10
    rows.append({
        "k": k,
        "per_token_acc_needed_for_50pct_exact_match": round(p_at_50, 6),
        "x_where_exact_match_crosses_50pct": round(float(x_at_50), 4),
        "x_width_10pct_to_90pct": round(float(width), 4),
    })

if __name__ == "__main__":
    print("Fixed smooth per-token accuracy curve p(x); only the metric changes.")
    print(f"{'k':>4} {'p needed for 50% exact-match':>30} {'x at 50% crossing':>20} {'10->90% x-width':>18}")
    for r in rows:
        print(f"{r['k']:>4} {r['per_token_acc_needed_for_50pct_exact_match']:>30} "
              f"{r['x_where_exact_match_crosses_50pct']:>20} {r['x_width_10pct_to_90pct']:>18}")
    print()
    print("Same underlying model, same smooth p(x). Requiring more correct")
    print("steps at once pushes the apparent jump later (larger x) and makes")
    print("it sharper (smaller x-width), purely as a function of k.")
    k1_width = rows[0]["x_width_10pct_to_90pct"]
    k100_width = rows[-1]["x_width_10pct_to_90pct"]
    print(f"k=1 -> k=100 sharpens the visible jump by {round(k1_width/k100_width, 1)}x")
    print(f"k=1 needs {rows[0]['per_token_acc_needed_for_50pct_exact_match']*100:.1f}% per-token accuracy to cross 50% exact-match")
    print(f"k=100 needs {rows[-1]['per_token_acc_needed_for_50pct_exact_match']*100:.2f}% per-token accuracy to cross 50% exact-match")
