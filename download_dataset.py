from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
import shutil
import tempfile

from config import RAW_DIR, DATASET_DIR

URL = "https://github.com/jukedeck/nottingham-dataset/archive/refs/heads/master.zip"


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if (DATASET_DIR / "MIDI" / "melody").exists():
        print(f"Dataset já existe em: {DATASET_DIR}")
        return

    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / "nottingham.zip"
        print("Baixando Nottingham Dataset...")
        with urlopen(URL, timeout=60) as response, archive.open("wb") as out:
            shutil.copyfileobj(response, out)

        print("Extraindo...")
        with ZipFile(archive) as z:
            z.extractall(tmp)

        extracted = Path(tmp) / "nottingham-dataset-master"
        if not extracted.exists():
            raise RuntimeError("Estrutura inesperada no arquivo baixado.")

        shutil.copytree(extracted, DATASET_DIR)

    print(f"Dataset instalado em: {DATASET_DIR}")


if __name__ == "__main__":
    main()
