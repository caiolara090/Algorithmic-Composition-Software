import json
import math
import random
from collections import Counter

from config import GRAMMAR_FILE, MOTIFS_FILE


class ProbabilisticGrammar:
    def __init__(self, motifs):
        self.motifs = motifs

    @classmethod
    def from_file(cls, path=MOTIFS_FILE):
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(data)

    def to_dict(self):
        total = sum(item["count"] for item in self.motifs)
        productions = []

        for item in self.motifs:
            probability = item["count"] / total if total else 0
            productions.append({
                "rhs": item["events"],
                "count": item["count"],
                "probability": probability,
            })

        return {
            "start": "S",
            "nonterminals": ["S", "PIECE", "PHRASE", "MOTIF"],
            "terminals": ["interval", "duration"],
            "productions": {
                "S": [["PIECE", 1.0]],
                "PIECE": [["PHRASE"] * 4, 1.0],
                "PHRASE": [["MOTIF", "MOTIF"], 1.0],
                "MOTIF": productions,
            },
        }

    def save(self, path=GRAMMAR_FILE):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    def sample_motif(self, temperature=1.0, rng=None):
        rng = rng or random.Random()

        if not self.motifs:
            raise RuntimeError("A gramática não possui motivos.")

        temperature = max(float(temperature), 0.05)

        logits = [math.log(max(item["count"], 1)) / temperature for item in self.motifs]
        max_logit = max(logits)
        weights = [math.exp(x - max_logit) for x in logits]

        selected = rng.choices(self.motifs, weights=weights, k=1)[0]
        return [tuple(event) for event in selected["events"]]


def train_grammar():
    grammar = ProbabilisticGrammar.from_file()
    grammar.save()
    return grammar
