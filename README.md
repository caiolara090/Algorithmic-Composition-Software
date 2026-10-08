# Composição Musical Algorítmica — Gramática Probabilística

Projeto do TP1 de Composição Musical Algorítmica.

## Método

O sistema usa uma **gramática generativa probabilística**. A estrutura hierárquica da música é definida manualmente, enquanto os motifs e suas probabilidades são aprendidos de um corpus real.

Fluxo:

1. baixar o Nottingham Dataset;
2. extrair MIDI de melodias monofônicas;
3. transformar notas em intervalos e durações;
4. extrair motivos recorrentes;
5. estimar probabilidades das produções;
6. gerar uma nova peça pela gramática;
7. reconstruir as alturas a partir dos intervalos;
8. salvar em MIDI.

A restrição estilística escolhida é **música folk tradicional em inglês**, usando melodias do Nottingham Dataset.

## Estrutura

```text
algoritmica-musical/
├── requirements.txt
├── README.md
├── config.py
├── download_dataset.py
├── extract_corpus.py
├── grammar.py
├── generator.py
├── midi_utils.py
├── train.py
├── generate.py
├── evaluate.py
├── data/
│   ├── raw/
│   └── processed/
└── output/
```

## Instalação

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Depois:

```bash
pip install -r requirements.txt
```

## Dataset

Execute:

```bash
python download_dataset.py
```

O script baixa a versão limpa do Nottingham Dataset do repositório JukeDeck e coloca os arquivos MIDI em `data/raw/nottingham/MIDI/melody/`.

O dataset contém aproximadamente 1.034 melodias MIDI, além das versões ABC e MIDI completo. A versão `MIDI/melody/` é usada porque contém somente a linha melódica.

Fonte:
https://github.com/jukedeck/nottingham-dataset

O repositório diz que os MIDI de melodia são derivados das versões ABC limpas.

## Extração

```bash
python extract_corpus.py
```

Isso gera:

```text
data/processed/motifs.json
data/processed/corpus_stats.json
```

## Treinamento da gramática

```bash
python train.py
```

Isso gera:

```text
data/processed/grammar.json
```

## Geração

```bash
python generate.py --seed 1 --temperature 0.8
python generate.py --seed 2 --temperature 1.0
python generate.py --seed 3 --temperature 1.2
```

Os MIDI serão gerados em `output/`.

## Avaliação

```bash
python evaluate.py
```

O script calcula estatísticas simples das peças geradas: duração, número de notas, média de intervalos e proporção de movimentos conjuntos.

## Ideia da gramática

A estrutura é:

```text
S
└── PIECE
    ├── PHRASE
    │   ├── MOTIF
    │   └── MOTIF
    ├── PHRASE
    │   ├── MOTIF
    │   └── MOTIF
    ├── PHRASE
    │   ├── MOTIF
    │   └── MOTIF
    └── PHRASE
        ├── MOTIF
        └── MOTIF
```

As alternativas de `MOTIF` são probabilísticas e estimadas do corpus. A temperatura altera a distribuição durante a geração, permitindo gerar peças diferentes com a mesma gramática.

## Experimento sugerido para o artigo

Gere 10 peças para cada:

```text
temperature = 0.5
temperature = 1.0
temperature = 1.5
```

Compare:

- duração média;
- número de notas;
- diversidade de motivos;
- proporção de intervalos pequenos;
- avaliação qualitativa por audição.

Não use a temperatura como "qualidade": ela é um parâmetro de diversidade. A avaliação musical deve ser reportada separadamente.

## Observação importante

O dataset não é copiado para este pacote porque é um corpus externo com licença própria. O `download_dataset.py` automatiza sua obtenção a partir da fonte original.

## Nota de Uso
