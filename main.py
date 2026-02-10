# main.py
from fastapi import FastAPI
from src.search import search_web 

app = FastAPI()

@app.get("/")
def home():
    return {"message": "QuickScholar API is running"}

@app.get("/search")
def search(query: str):
    """
    Endpoint to search research data.
    Usage: /search?query=biology
    """
    results = search_web(query)
    return results

