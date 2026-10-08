from pathlib import Path
from statistics import mean

from music21 import converter, note

from config import OUTPUT_DIR


def evaluate(path):
    score = converter.parse(path)
    notes = list(score.flatten().notes)

    if not notes:
        return None

    intervals = []
    for a, b in zip(notes, notes[1:]):
        intervals.append(abs(b.pitch.midi - a.pitch.midi))

    return {
        "file": path.name,
        "notes": len(notes),
        "duration": round(float(score.duration.quarterLength), 2),
        "mean_abs_interval": round(mean(intervals), 2) if intervals else 0.0,
        "stepwise_ratio": round(
            sum(i <= 2 for i in intervals) / len(intervals), 3
        ) if intervals else 0.0,
    }


def main():
    rows = []

    for path in sorted(OUTPUT_DIR.glob("*.mid")):
        result = evaluate(path)
        if result:
            rows.append(result)

    if not rows:
        print("Nenhum MIDI encontrado em output/.")
        return

    print("file,notes,duration,mean_abs_interval,stepwise_ratio")
    for row in rows:
        print(
            f"{row['file']},{row['notes']},{row['duration']},"
            f"{row['mean_abs_interval']},{row['stepwise_ratio']}"
        )


if __name__ == "__main__":
    main()
