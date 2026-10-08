import argparse
from pathlib import Path

from config import GRAMMAR_FILE, OUTPUT_DIR, DEFAULT_TEMPERATURE, DEFAULT_TEMPO
from grammar import ProbabilisticGrammar
from generator import generate_events
from midi_utils import save_midi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--tempo", type=int, default=DEFAULT_TEMPO)
    args = parser.parse_args()

    if not GRAMMAR_FILE.exists():
        raise FileNotFoundError("Execute python train.py primeiro.")

    grammar = ProbabilisticGrammar.from_file()
    events = generate_events(grammar, args.temperature, args.seed)

    output = OUTPUT_DIR / f"generated_seed{args.seed}_temp{args.temperature:.2f}.mid"
    save_midi(events, output, args.tempo)

    print(f"Arquivo gerado: {output}")


if __name__ == "__main__":
    main()
