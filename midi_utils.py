from pathlib import Path
from music21 import converter, instrument, note, chord, stream, tempo as m21tempo


def load_melody(path: Path):
    score = converter.parse(path)
    parts = score.parts

    if not parts:
        return []

    part = parts[0]
    events = []

    for element in part.flatten().notesAndRests:
        if isinstance(element, note.Note):
            events.append((int(element.pitch.midi), float(element.duration.quarterLength)))
        elif isinstance(element, chord.Chord):
            if element.pitches:
                pitch = max(element.pitches, key=lambda p: p.pitchClass)
                events.append((int(pitch.midi), float(element.duration.quarterLength)))

    return events


def save_midi(events, path: Path, bpm=110):
    path.parent.mkdir(parents=True, exist_ok=True)

    score = stream.Stream()
    score.insert(0, instrument.Piano())

    for pitch, duration in events:
        n = note.Note(pitch)
        n.duration.quarterLength = duration
        score.append(n)

    score.insert(0, m21tempo.MetronomeMark(number=bpm))
    score.write("midi", fp=str(path))