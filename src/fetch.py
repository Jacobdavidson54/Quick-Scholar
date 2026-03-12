# fetch.py
import requests
from src.utils import load_file, save_data

def fetch_semantic_papers(query):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": 5,
        "fields": "title,authors,year,paperId"
    }
    headers = {"User-Agent": "QuickScholar/1.0"}  # prevent rejection

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # raises exception if status != 200

        if response.status_code != 200:
            return {
                "error": "API request failed",
                "status": response.status_code,
                "response": response.text
            }, response.status_code

        raw_data = response.json()
        papers = raw_data.get("data", [])
        if not papers:
            return {"error": "No papers found"}, 404

        cleaned_results = []
        for paper in papers:
            cleaned_results.append({
                "title": paper.get("title"),
                "authors": paper.get("authors"),
                "year": paper.get("year"),
                "url": f"https://www.semanticscholar.org/paper/{paper.get('paperId')}",
                "source": "semantic_scholar"
            })

        # Save to JSON
        existing_data = load_file()
        existing_data.extend(cleaned_results)
        save_data(existing_data)

        return cleaned_results, 200

    except requests.RequestException:
        return {"error": "Connection failed"}, 500



def fetch_crossref_metadata(query):

    crossref_url = "https://api.crossref.org/works"

    headers = {
        "User-Agent": "QuickScholar/1.0 (mailto:nergtonicsa@gmail.com)"
    }

    params = {
        "query": query,
        "rows": 5
    }

    try:
        response = requests.get(
            crossref_url,
            headers=headers,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        raw_data = response.json()

        items = raw_data.get("message", {}).get("items", [])

        if not items:
            return {"error": "No results found"}, 404

        cleaned_results = []

        for item in items:

            cleaned_results.append({
                "title": item.get("title", [""])[0],
                "authors": item.get("author"),
                "year": item.get("issued", {}).get("date-parts", [[None]])[0][0],
                "doi": item.get("DOI"),
                "url": item.get("URL"),
                "publisher": item.get("publisher"),
                "source": "crossref"
            })

        # Save results
        existing_data = load_file()
        existing_data.extend(cleaned_results)
        save_data(existing_data)

        return cleaned_results, 200

    except requests.RequestException:
        return {"error": "Connection failed"}, 500
    



                
    
