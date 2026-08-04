import itertools, json

def bitonic_sort_network(n):
    """Batcher's bitonic sorting network comparators for n = power of 2.
    Returns list of (layer_index, i, j) with i<j, arrow meaning compare-swap so a[i]<=a[j]
    (ascending network). Standard textbook construction (Batcher 1968)."""
    assert n & (n - 1) == 0 and n >= 2
    comparators = []  # (layer, i, j)

    def bitonic_merge(lo, cnt, direction, layer):
        if cnt > 1:
            k = cnt // 2
            for i in range(lo, lo + k):
                a, b = i, i + k
                if direction:
                    comparators.append((layer, a, b))
                else:
                    comparators.append((layer, b, a))
            bitonic_merge(lo, k, direction, layer + 1)
            bitonic_merge(lo + k, k, direction, layer + 1)

    def bitonic_sort(lo, cnt, direction, layer):
        if cnt > 1:
            k = cnt // 2
            sub_layer = bitonic_sort(lo, k, True, layer)
            sub_layer2 = bitonic_sort(lo + k, k, False, layer)
            start = max(sub_layer, sub_layer2)
            bitonic_merge(lo, cnt, direction, start)
            # depth added by this merge = log2(cnt)
            import math
            return start + int(math.log2(cnt))
        return layer

    bitonic_sort(0, n, True, 0)
    return comparators

def apply_network(bits, comparators):
    bits = list(bits)
    for (_layer, i, j) in comparators:
        if bits[i] > bits[j]:
            bits[i], bits[j] = bits[j], bits[i]
    return bits

def verify_0_1_principle(n, comparators):
    """Knuth's 0-1 principle: a comparator network sorts all real sequences
    iff it sorts all 2^n binary sequences. Brute-force check every bitstring."""
    bad = []
    for bits in itertools.product([0, 1], repeat=n):
        out = apply_network(bits, comparators)
        if list(out) != sorted(bits):
            bad.append(bits)
    return bad

results = {}
for k in range(1, 8):  # n = 2,4,8,...,128
    n = 2 ** k
    net = bitonic_sort_network(n)
    layers = max(l for l, _, _ in net) + 1 if net else 0
    count = len(net)
    formula_depth = k * (k + 1) // 2
    entry = {"n": n, "comparators": count, "depth_layers": layers,
             "formula_k(k+1)/2": formula_depth, "depth_matches_formula": layers == formula_depth}
    if n <= 16:  # brute-force verifiable in reasonable time (2^16 = 65536)
        bad = verify_0_1_principle(n, net)
        entry["verified_0_1_principle"] = (len(bad) == 0)
        entry["counterexamples"] = bad[:3]
    results[n] = entry
    print(n, entry)

with open("/tmp/claude-0/-home-user/489beb8e-2881-5a06-bb86-a25a3cd421e3/scratchpad/work/sortnet/results.json", "w") as f:
    json.dump(results, f, indent=2)
