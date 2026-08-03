"""
Back-of-envelope validation of the published Colibri / GLM-5.2 numbers.
Not a benchmark I ran myself (the model is 372GB and this session has
no such hardware) -- a check of whether the publicly reported figures
are internally consistent, and what they imply about the real
bottleneck. All input numbers are from the project's own README and
independent coverage (see compute.md for exact sources); this script
only does the arithmetic.
"""
import json

# --- published inputs ---
TOTAL_PARAMS_B = 744          # GLM-5.2 total parameters, billions
ACTIVE_PARAMS_B = 40          # active parameters per token, billions
N_EXPERTS = 19456             # routed experts
N_MOE_LAYERS = 75             # MoE layers
EXPERT_SIZE_MB = 19           # int4 expert size, MB
RESIDENT_RAM_GB = 9.9         # dense portion resident in RAM (int4)
DISK_STREAMED_GB = 370        # routed experts on disk
COLD_TOKENS_PER_SEC = (0.05, 0.10)   # reported cold-cache range

results = {}

# 1. active fraction of the model
active_fraction = ACTIVE_PARAMS_B / TOTAL_PARAMS_B
results["active_fraction_pct"] = round(active_fraction * 100, 2)

# 2. reported "~11GB read per cold token" -- check what top-k routing
#    that implies, given experts-per-layer and expert size
reported_gb_per_cold_token = 11.0
implied_experts_per_layer_per_token = (
    reported_gb_per_cold_token * 1024  # MB
) / (N_MOE_LAYERS * EXPERT_SIZE_MB)
results["implied_top_k_per_layer"] = round(implied_experts_per_layer_per_token, 2)

# sanity check the other direction: what top-8 routing would predict
predicted_gb_at_top8 = (8 * N_MOE_LAYERS * EXPERT_SIZE_MB) / 1024
results["predicted_gb_per_token_at_top8"] = round(predicted_gb_at_top8, 2)

# 3. implied effective disk read throughput during cold decode
#    time per token = 1 / tokens_per_sec
lo_tok_s, hi_tok_s = COLD_TOKENS_PER_SEC
time_per_token_range_s = (1 / hi_tok_s, 1 / lo_tok_s)  # faster tok/s -> shorter time
implied_throughput_gbps = (
    reported_gb_per_cold_token / time_per_token_range_s[1],
    reported_gb_per_cold_token / time_per_token_range_s[0],
)
results["time_per_token_range_s"] = [round(t, 1) for t in time_per_token_range_s]
results["implied_effective_read_throughput_GBps"] = [
    round(x, 2) for x in implied_throughput_gbps
]

# 4. how that compares to a typical consumer NVMe's rated sequential speed
typical_nvme_sequential_gbps = (3.5, 7.0)  # widely published Gen3/Gen4 spec range
results["typical_nvme_sequential_GBps"] = typical_nvme_sequential_gbps
results["shortfall_vs_rated_spec_x"] = [
    round(typical_nvme_sequential_gbps[0] / implied_throughput_gbps[1], 1),
    round(typical_nvme_sequential_gbps[1] / implied_throughput_gbps[0], 1),
]

print(json.dumps(results, indent=2))

with open("colibri_math.json", "w") as f:
    json.dump(results, f, indent=2)
