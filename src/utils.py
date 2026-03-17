# utils.py
import unicodedata
import json
import os
import re

FILE_NAME = "results_research.json"

def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump([], file)

def load_file():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# normalize a single string
def normalize_string(text):

    if not text:
        return ""

    text = text.lower()

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")


    # bug fix: Cleaned text by removing punctuation and extra spaces, so words are neat and searchable.
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()


    text = text.strip()

    return text


# normalize list of papers
def normalize_results(results):

    for paper in results:

        if "title" in paper:
            paper["title"] = normalize_string(paper["title"])

    return results


