# search.py
from src.fetch import fetch_semantic_papers

def search_papers(query):
    results, status = fetch_semantic_papers(query)
    return results, status