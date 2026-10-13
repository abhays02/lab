"""Build evidence-led GIFs from the experiment JSON files."""

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SIZE = (720, 405)
BG = "#111318"
PANEL = "#1d2330"
WHITE = "#f5f7fa"
MUTED = "#9fa6b5"
BLUE = "#4a8be0"
ORANGE = "#eb5c28"
GREEN = "#48b487"


def load_json(relative_path):
    return json.loads((ROOT / relative_path).read_text())


def canvas(section, title, subtitle):
    image = Image.new("RGB", SIZE, BG)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, SIZE[0], 5), fill=BLUE)
    draw.text((32, 19), f"ABHAYS02 / LAB  |  {section.upper()}", fill=MUTED,
              font=ImageFont.load_default(size=13))
    draw.text((32, 49), title, fill=WHITE, font=ImageFont.load_default(size=23))
    draw.text((32, 82), subtitle, fill=MUTED, font=ImageFont.load_default(size=15))
    return image, draw


def footer(draw, text):
    draw.line((32, 350, 688, 350), fill="#343944", width=1)
    draw.text((32, 362), text, fill=MUTED, font=ImageFont.load_default(size=12))


def axes(draw, x_label, y_label):
    draw.line((76, 135, 76, 310), fill="#596170", width=2)
    draw.line((76, 310, 680, 310), fill="#596170", width=2)
    draw.text((79, 318), x_label, fill=MUTED, font=ImageFont.load_default(size=12))
    draw.text((78, 119), y_label, fill=MUTED, font=ImageFont.load_default(size=12))


def progressive_counts(total, frame_count=9):
    return sorted({max(1, math.ceil(total * i / frame_count))
                   for i in range(1, frame_count + 1)})


def save_gif(name, frames):
    output = ROOT / name
    output.parent.mkdir(parents=True, exist_ok=True)
    indexed = [frame.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
               for frame in frames]
    indexed[0].save(
        output,
        format="GIF",
        save_all=True,
        append_images=indexed[1:],
        duration=420,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"{output.relative_to(ROOT)}: {len(indexed)} frames, {output.stat().st_size} bytes")


def barren_frames():
    data = load_json("barren-plateaus/barren_log.json")
    rows = [(int(n), result["variance_gradient_local"],
             result["variance_gradient_global"])
            for n, result in data["results"].items()]
    low = min(math.log10(value) for _, *values in rows for value in values)
    high = max(math.log10(value) for _, *values in rows for value in values)
    frames = []
    for count in progressive_counts(len(rows)):
        image, draw = canvas(
            "Barren plateaus", "Measured gradient variance",
            "Fixed depth 20; 150 circuits at each measured qubit count",
        )
        axes(draw, "qubits", "variance (log scale)")
        draw.text((435, 119), "Local Z0", fill=BLUE, font=ImageFont.load_default(size=13))
        draw.text((535, 119), "Global parity", fill=ORANGE, font=ImageFont.load_default(size=13))
        visible = rows[:count]
        points = [[], []]
        for n, local, global_ in visible:
            x = 86 + (n - 2) / 10 * 570
            for series, value in enumerate((local, global_)):
                y = 145 + (high - math.log10(value)) / (high - low) * 145
                points[series].append((x, y))
        for series, color in enumerate((BLUE, ORANGE)):
            if len(points[series]) > 1:
                draw.line(points[series], fill=color, width=2)
            for point in points[series]:
                x, y = point
                draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color)
        draw.text((84, 329), "2", fill=MUTED, font=ImageFont.load_default(size=12))
        draw.text((640, 329), "12", fill=MUTED, font=ImageFont.load_default(size=12))
        last_n, local, global_ = visible[-1]
        footer(draw, f"Through {last_n} qubits. Markers are recorded values; lines are visual guides.")
        frames.append(image)
    return frames


def double_descent_frames():
    data = load_json("double-descent/double_descent_log.json")
    rows = data["results"]
    min_x, max_x = math.log10(rows[0]["p"]), math.log10(rows[-1]["p"])
    values = [math.log10(row["test_mse_mean"]) for row in rows]
    min_y, max_y = min(values), max(values)
    frames = []
    for count in progressive_counts(len(rows)):
        image, draw = canvas(
            "Double descent", "Measured test MSE by feature count",
            "30 trials per point; both axes use log scales",
        )
        axes(draw, "features p", "test MSE")
        draw.text((460, 119), "recorded sweep points", fill=BLUE,
                  font=ImageFont.load_default(size=12))
        visible = rows[:count]
        for row in visible:
            x = 86 + (math.log10(row["p"]) - min_x) / (max_x - min_x) * 570
            y = 145 + (max_y - math.log10(row["test_mse_mean"])) / (max_y - min_y) * 145
            color = ORANGE if row["p"] == 100 else GREEN if row["p"] == 101 else BLUE
            radius = 6 if row["p"] in (100, 101) else 3
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
            if row["p"] == 100:
                draw.text((x - 22, y - 23), "p=100", fill=ORANGE,
                          font=ImageFont.load_default(size=12))
            elif row["p"] == 101:
                draw.text((x + 7, y + 5), "p=101", fill=GREEN,
                          font=ImageFont.load_default(size=12))
        peak = data["peak"]["test_mse_mean"]
        after = next(row["test_mse_mean"] for row in rows if row["p"] == 101)
        footer(draw, f"Recorded p=100: {peak:,.2f}; p=101: {after:.2f}. No values are interpolated.")
        frames.append(image)
    return frames


def colibri_frames():
    data = load_json("colibri-glm/colibri_math.json")
    stages = [
        ("Published model size", "744B total parameters; 40B active per token",
         "Source values recorded in colibri_math.py; no local model run."),
        ("Active fraction", f"{data['active_fraction_pct']:.2f}% active per token",
         "Arithmetic from published parameter counts."),
        ("Implied routing", f"{data['implied_top_k_per_layer']:.1f} experts per layer",
         "Derived from the reported cold-token read volume."),
        ("Cold-token read math", f"{data['predicted_gb_per_token_at_top8']:.2f} GB at top-8",
         "Arithmetic check; this is not a full-model benchmark."),
        ("Implied throughput", "0.55-1.10 GB/s",
         "Derived from published speed/read figures; not a drive measurement."),
    ]
    frames = []
    for active in range(len(stages)):
        image, draw = canvas(
            "Colibri / GLM", "Architecture arithmetic, not a benchmark",
            "Published architecture and performance inputs; calculations only",
        )
        labels = [
            ("Model", "744B total  |  40B active/token"),
            ("Active fraction", f"{data['active_fraction_pct']:.2f}%"),
            ("Routing", f"{data['implied_top_k_per_layer']:.1f} experts/layer"),
            ("Cold token", f"{data['predicted_gb_per_token_at_top8']:.2f} GB predicted at top-8"),
            ("Read rate", "0.55-1.10 GB/s implied"),
        ]
        for index, (label, value) in enumerate(labels):
            y = 132 + index * 39
            color = ORANGE if index == active else PANEL
            draw.rounded_rectangle((48, y, 672, y + 31), radius=6, fill=color)
            draw.text((62, y + 7), label, fill=WHITE, font=ImageFont.load_default(size=14))
            draw.text((250, y + 7), value, fill=WHITE, font=ImageFont.load_default(size=14))
        footer(draw, f"{stages[active][0]}: {stages[active][2]}")
        frames.append(image)
    return frames


def sorting_frames():
    result = load_json("sorting-network-depth/batcher_results.json")["16"]
    depth = result["depth_layers"]
    frames = []
    for count in range(1, depth + 1):
        image, draw = canvas(
            "Sorting networks", "Batcher depth at n=16",
            "Computed network layers; comparator diagram is intentionally schematic",
        )
        draw.text((54, 137), "10 computed rounds", fill=WHITE,
                  font=ImageFont.load_default(size=16))
        for index in range(depth):
            x = 54 + index * 62
            fill = BLUE if index < count else PANEL
            draw.rounded_rectangle((x, 174, x + 48, 226), radius=6, fill=fill)
            draw.text((x + 15, 190), str(index + 1), fill=WHITE,
                      font=ImageFont.load_default(size=15))
        draw.text((54, 254), "Proven optimum: 9 rounds", fill=ORANGE,
                  font=ImageFont.load_default(size=18))
        draw.text((54, 286),
                  f"{result['comparators']} comparators; {2 ** 16:,} binary inputs checked",
                  fill=MUTED, font=ImageFont.load_default(size=14))
        draw.text((54, 310), "0 counterexamples in the committed result",
                  fill=GREEN, font=ImageFont.load_default(size=14))
        footer(draw, "Round blocks show depth only; they are not the measured comparator layout.")
        frames.append(image)
    return frames


def quantum_frames():
    data = load_json("quantum-advantage-boundary/rcs_results.json")
    rows = data["classical_memory_table_full_statevector"]
    min_x, max_x = rows[0]["qubits"], rows[-1]["qubits"]
    values = [math.log10(row["bytes_exact"]) for row in rows]
    min_y, max_y = min(values), max(values)
    frames = []
    for count in progressive_counts(len(rows)):
        image, draw = canvas(
            "Quantum advantage boundary", "Exact full-statevector storage",
            "Complex128 bytes from committed exact-arithmetic table; y-axis is log scale",
        )
        axes(draw, "qubits", "bytes")
        points = []
        for row in rows[:count]:
            x = 86 + (row["qubits"] - min_x) / (max_x - min_x) * 570
            y = 145 + (max_y - math.log10(row["bytes_exact"])) / (max_y - min_y) * 145
            points.append((x, y))
            color = ORANGE if row["qubits"] == 53 else BLUE
            radius = 6 if row["qubits"] == 53 else 4
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
            if row["qubits"] in (10, 53, 60):
                draw.text((x - 18, y - 20), f"{row['qubits']}q", fill=color,
                          font=ImageFont.load_default(size=12))
        if len(points) > 1:
            draw.line(points, fill="#657083", width=2)
        target = next((row for row in rows if row["qubits"] == 53), None)
        footer(draw, f"53 qubits: {target['human']}; exact storage arithmetic, not a 53-qubit simulation.")
        frames.append(image)
    return frames


def emergence_frames():
    data = load_json("emergence-mirage/emergence_results.json")
    rows = data["rows"]
    min_x, max_x = min(row["k"] for row in rows), max(row["k"] for row in rows)
    min_y = min(row["x_where_exact_match_crosses_50pct"] for row in rows)
    max_y = max(row["x_where_exact_match_crosses_50pct"] for row in rows)
    frames = []
    for count in range(1, len(rows) + 1):
        image, draw = canvas(
            "Emergence mirage", "Computed exact-match thresholds",
            "One fixed synthetic logistic curve; only the exact-match length k changes",
        )
        axes(draw, "required correct steps k", "scale x at 50% exact match")
        points = []
        for row in rows[:count]:
            x = 86 + (row["k"] - min_x) / (max_x - min_x) * 570
            y = 285 - (row["x_where_exact_match_crosses_50pct"] - min_y) / (max_y - min_y) * 125
            points.append((x, y))
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=GREEN)
            draw.text((x - 8, 290, x + 33, 309), f"k={row['k']}",
                      fill=MUTED, font=ImageFont.load_default(size=11))
        if len(points) > 1:
            draw.line(points, fill=GREEN, width=2)
        latest = rows[count - 1]
        accuracy = latest["per_token_acc_needed_for_50pct_exact_match"] * 100
        footer(draw, f"k={latest['k']}: {accuracy:.2f}% token accuracy; synthetic math, not trained-model data.")
        frames.append(image)
    return frames


def workflow_frames():
    stages = ("QUESTION", "SCRIPT", "RAW JSON", "PROVENANCE")
    frames = []
    for active in range(len(stages)):
        image, draw = canvas(
            "Evidence workflow", "From question to inspectable evidence",
            "A guide to repository files, not a measurement",
        )
        for index, label in enumerate(stages):
            x = 36 + index * 170
            fill = BLUE if index == active else PANEL
            draw.rounded_rectangle((x, 180, x + 145, 245), radius=10,
                                   fill=fill, outline="#596170", width=1)
            draw.text((x + 16, 204), label, fill=WHITE,
                      font=ImageFont.load_default(size=16))
            if index < len(stages) - 1:
                draw.line((x + 147, 212, x + 166, 212), fill=MUTED, width=2)
                draw.polygon(((x + 166, 208), (x + 172, 212), (x + 166, 216)),
                             fill=MUTED)
        footer(draw, "Schematic workflow only; it contains no experimental data.")
        frames.append(image)
    return frames


def main():
    outputs = [
        ("barren-plateaus/animation.gif", barren_frames()),
        ("double-descent/animation.gif", double_descent_frames()),
        ("colibri-glm/animation.gif", colibri_frames()),
        ("sorting-network-depth/animation.gif", sorting_frames()),
        ("quantum-advantage-boundary/animation.gif", quantum_frames()),
        ("emergence-mirage/animation.gif", emergence_frames()),
        ("assets/evidence-workflow.gif", workflow_frames()),
    ]
    for name, frames in outputs:
        save_gif(name, frames)


if __name__ == "__main__":
    main()
