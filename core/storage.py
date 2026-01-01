import json
from pathlib import Path

DATA_FILE = Path("data/question_bank.json")

EMPTY_BANK = {
    "categories": {}
}

def load_bank():
    if not DATA_FILE.exists():
        return EMPTY_BANK.copy()

    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return EMPTY_BANK.copy()
            return json.loads(content)

    except (json.JSONDecodeError, OSError):
        # fallback if file is corrupted
        return EMPTY_BANK.copy()


def save_bank(bank):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(bank, f, indent=4, ensure_ascii=False)
