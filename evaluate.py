import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
from music21 import converter

from config import OUTPUT_DIR


TEMPERATURES = [0.5, 0.75, 1.0, 1.25, 1.5]


def load_midi(path):
    score = converter.parse(path)

    notes = []

    for element in score.flatten().notes:
        if hasattr(element, "pitch"):
            notes.append({
                "pitch": element.pitch.midi,
                "duration": float(element.duration.quarterLength),
            })

    return notes


def get_intervals(notes):
    return [
        notes[i + 1]["pitch"] - notes[i]["pitch"]
        for i in range(len(notes) - 1)
    ]


def get_durations(notes):
    return [note["duration"] for note in notes]


def get_motifs(notes, length=4):
    intervals = get_intervals(notes)

    return [
        tuple(intervals[i:i + length])
        for i in range(len(intervals) - length + 1)
    ]


def entropy(values):
    if not values:
        return 0.0

    counts = Counter(values)
    total = len(values)

    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
    )


def evaluate_file(path):
    notes = load_midi(path)

    if len(notes) < 2:
        return None

    intervals = get_intervals(notes)
    durations = get_durations(notes)
    motifs = get_motifs(notes)

    motif_counts = Counter(motifs)

    unique_motifs = len(motif_counts)
    total_motifs = len(motifs)

    repeated_motifs = sum(
        count for count in motif_counts.values()
        if count > 1
    )

    repetition_rate = (
        repeated_motifs / total_motifs
        if total_motifs
        else 0.0
    )

    total_duration = sum(durations)

    return {
        "file": path.name,
        "notes": len(notes),
        "duration_beats": total_duration,
        "duration_seconds": total_duration * 60 / 110,
        "mean_duration": np.mean(durations),
        "std_duration": np.std(durations),
        "mean_interval": np.mean(intervals),
        "std_interval": np.std(intervals),
        "unique_intervals": len(set(intervals)),
        "unique_motifs": unique_motifs,
        "motif_entropy": entropy(motifs),
        "repetition_rate": repetition_rate,
        "pitch_range": max(
            note["pitch"] for note in notes
        ) - min(
            note["pitch"] for note in notes
        ),
    }


def get_temperature(filename):
    return float(
        filename.split("_temp")[1].replace(".mid", "")
    )


def main():
    results = []

    for path in sorted(OUTPUT_DIR.glob("*.mid")):
        result = evaluate_file(path)

        if result is not None:
            result["temperature"] = get_temperature(path.name)
            results.append(result)

    if not results:
        raise RuntimeError(
            f"Nenhum arquivo MIDI encontrado em {OUTPUT_DIR}"
        )

    output = Path("evaluation_results.json")

    output.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    print("\nResultados por arquivo:")
    print("-" * 100)

    for result in results:
        print(
            f"{result['file']:<40} "
            f"T={result['temperature']:<4.2f} "
            f"notes={result['notes']:<3} "
            f"duration={result['duration_seconds']:<6.2f}s "
            f"motifs={result['unique_motifs']:<3} "
            f"entropy={result['motif_entropy']:<5.2f} "
            f"repeat={result['repetition_rate']:.2%}"
        )

    print("\nResumo por temperatura:")
    print("-" * 100)

    metrics = [
        "duration_seconds",
        "notes",
        "unique_motifs",
        "motif_entropy",
        "repetition_rate",
        "mean_interval",
        "std_interval",
        "mean_duration",
        "std_duration",
        "pitch_range",
    ]

    for temperature in sorted(
        set(result["temperature"] for result in results)
    ):
        subset = [
            result
            for result in results
            if result["temperature"] == temperature
        ]

        print(f"\nTemperature = {temperature:.2f}")

        for metric in metrics:
            values = [result[metric] for result in subset]

            print(
                f"  {metric:<20} "
                f"{np.mean(values):.4f} ± {np.std(values):.4f}"
            )


if __name__ == "__main__":
    main()