from grammar import train_grammar
from config import GRAMMAR_FILE


def main():
    train_grammar()
    print(f"Gramática salva em: {GRAMMAR_FILE}")


if __name__ == "__main__":
    main()
