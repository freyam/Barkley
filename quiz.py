from utils import *
import json


def add_question(question_text, sender):
    sender_key = str(sender)

    with open("questions.json", "r") as f:
        questions = json.load(f)
        unique_hash = str(get_unique_hash())
        questions[unique_hash] = questions.get(unique_hash) or {}

        if not questions.get(unique_hash).get(question_text):
            questions.get(unique_hash)[question_text] = question_text

    with open("questions.json", "w") as f:
        json.dump(questions, f)


def add_answer(q_hash, sender, answer):
    q_hash = str(sender)

    with open("questions.json", "r") as f:
        questions = json.load(f)
        questions[q_hash] = questions.get(q_hash) or {}

        if not questions.get(q_hash).get(answer):
            questions.get(q_hash)[answer] = []
            questions.get(q_hash)[answer].append(answer)

    with open("questions.json", "w") as f:
        json.dump(questions, f)
