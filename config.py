from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = ROOT / "output"

DATASET_DIR = RAW_DIR / "nottingham"
MELODY_DIR = DATASET_DIR / "MIDI" / "melody"

MOTIFS_FILE = PROCESSED_DIR / "motifs.json"
STATS_FILE = PROCESSED_DIR / "corpus_stats.json"
GRAMMAR_FILE = PROCESSED_DIR / "grammar.json"

MOTIF_LENGTH = 4
MIN_MOTIF_COUNT = 5
MAX_NOTES_PER_SONG = None
PHRASES = 4
MOTIFS_PER_PHRASE = 2
DEFAULT_TEMPERATURE = 1.0
DEFAULT_TEMPO = 110

MAX_MOTIFS = 500
