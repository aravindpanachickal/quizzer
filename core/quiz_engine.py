import random
from core.storage import load_bank, save_bank

class QuizEngine:
    def __init__(self, categories=None):
        self.bank = load_bank()
        self.questions = self._collect_questions(categories)
        self.current_question = None

        # SESSION-LEVEL STATS (RAM ONLY)
        self.session = {
            "attempted": 0,
            "correct": 0,
            "wrong": 0,
            "score": 0
        }

    def _collect_questions(self, categories):
        collected = []

        all_categories = self.bank.get("categories", {})

        if not categories:
            categories = all_categories.keys()

        for cat in categories:
            collected.extend(all_categories.get(cat, []))

        return collected

    def has_questions(self):
        return len(self.questions) > 0

    def next_question(self):
        if not self.questions:
            return None

        weights = [q["stats"]["weight"] for q in self.questions]
        self.current_question = random.choices(
            self.questions,
            weights=weights,
            k=1
        )[0]

        return self.current_question

    def submit_answer(self, selected_index):
        q = self.current_question
        if q is None:
            return None

        # Session tracking
        self.session["attempted"] += 1

        q["stats"]["attempts"] += 1

        if selected_index == q["correct"]:
            self.session["correct"] += 1
            self.session["score"] += 1  # simple scoring rule

            q["stats"]["correct"] += 1
            q["stats"]["weight"] = max(0.2, q["stats"]["weight"] * 0.8)
            correct = True
        else:
            self.session["wrong"] += 1

            q["stats"]["wrong"] += 1
            q["stats"]["weight"] = min(5.0, q["stats"]["weight"] * 1.25)
            correct = False

        save_bank(self.bank)
        return correct

    def get_session_summary(self):
        return self.session.copy()