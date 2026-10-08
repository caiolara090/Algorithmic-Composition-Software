import json
from collections import Counter

from config import (
    MELODY_DIR,
    MOTIFS_FILE,
    STATS_FILE,
    MOTIF_LENGTH,
    MIN_MOTIF_COUNT,
    MAX_NOTES_PER_SONG,
    MAX_MOTIFS,
)
from midi_utils import load_melody


def intervals(events):
    if len(events) < 2:
        return []

    return [
        (events[i + 1][0] - events[i][0], events[i][1])
        for i in range(len(events) - 1)
    ]


def extract_motifs(sequence, length):
    if len(sequence) < length:
        return []

    return [
        sequence[i:i + length]
        for i in range(len(sequence) - length + 1)
    ]


def main():
    if not MELODY_DIR.exists():
        raise FileNotFoundError(
            f"{MELODY_DIR} não existe. Execute python download_dataset.py primeiro."
        )

    counter = Counter()
    song_count = 0
    note_count = 0

    for path in sorted(MELODY_DIR.glob("*.mid")):
        try:
            events = load_melody(path)
        except Exception as exc:
            print(f"Ignorando {path.name}: {exc}")
            continue

        events = events[:MAX_NOTES_PER_SONG]
        seq = intervals(events)

        for motif in extract_motifs(seq, MOTIF_LENGTH):
            counter[tuple(tuple(x) for x in motif)] += 1

        song_count += 1
        note_count += len(events)

    counter = Counter({
        motif: count
        for motif, count in counter.items()
        if count >= MIN_MOTIF_COUNT
    })

    # Mantém somente os MAX_MOTIFS motivos mais frequentes.
    top_motifs = counter.most_common(MAX_MOTIFS)

    motifs = [
        {
            "events": [list(event) for event in motif],
            "count": count,
        }
        for motif, count in top_motifs
    ]

    MOTIFS_FILE.parent.mkdir(parents=True, exist_ok=True)
    MOTIFS_FILE.write_text(
        json.dumps(motifs, indent=2),
        encoding="utf-8",
    )

    stats = {
        "songs": song_count,
        "notes": note_count,
        "unique_motifs": len(motifs),
        "motif_length": MOTIF_LENGTH,
        "min_motif_count": MIN_MOTIF_COUNT,
        "max_motifs": MAX_MOTIFS,
    }

    STATS_FILE.write_text(
        json.dumps(stats, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()