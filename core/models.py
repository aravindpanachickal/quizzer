import uuid

def new_question(category, question, options, correct):
    return {
        "id": str(uuid.uuid4()),
        "question": question,
        "options": options,
        "correct": correct,
        "stats": {
            "attempts": 0,
            "correct": 0,
            "wrong": 0,
            "weight": 1.0
        }
    }
