import random

from config import PHRASES, MOTIFS_PER_PHRASE
from grammar import ProbabilisticGrammar


def choose_start_pitch(rng):
    return rng.choice([60, 62, 64, 65, 67])


def generate_events(grammar, temperature=1.0, seed=None):
    rng = random.Random(seed)
    current_pitch = choose_start_pitch(rng)
    events = []

    for _ in range(PHRASES):
        for _ in range(MOTIFS_PER_PHRASE):
            motif = grammar.sample_motif(temperature, rng)

            for interval, duration in motif:
                current_pitch += int(interval)
                current_pitch = max(48, min(84, current_pitch))
                events.append((current_pitch, max(0.125, float(duration))))

    return events
