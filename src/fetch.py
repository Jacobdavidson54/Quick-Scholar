# fetch.py
import requests
from src.utils import load_file, save_data
import xml.etree.ElementTree as ET

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
    

def fetch_openalex_results(search):
    
    openA_url = "https://api.openalex.org/works"
    API_KEY = "IzOXOSjjmAMQGZronE67XU"  

    params = {
        "search": search,
        "per_page": 5,
        "api_key": API_KEY
    }

    try:
        response = requests.get(openA_url, params=params, timeout=10)
        response.raise_for_status()  # automatically raises exception if HTTP error

        raw_info = response.json()
        information = raw_info.get("results", [])

        if not information:
            return None, 404  # consistent 2-value return

        cleaned_info = []

        for info in information:
            title = info.get("title")

            # Abstract reconstruction note
            abstract = None
            if info.get("abstract_inverted_index"):
                abstract = "Abstract available (needs reconstruction)"

            # PDF / full_text URL
            pdf = None
            location = info.get("primary_location")
            if location:
                pdf = location.get("pdf_url")

            cleaned_info.append({
                "title": title,
                "abstract": abstract,
                "full_text": pdf,
                "source": "OpenAlex"
            })

        # Save processed data
        current_data = load_file()
        current_data.extend(cleaned_info)
        save_data(current_data)

        return cleaned_info, 200  # success

    except requests.RequestException:
        return None, 500  # connection failed
    
def fetch_arxiv_data(query):

    arxiv_url = "http://export.arxiv.org/api/query"

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": 5
    }

    try:
        response = requests.get(arxiv_url, params=params, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        cleaned_metadata = []

        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):

            title = entry.find("{http://www.w3.org/2005/Atom}title").text

            published = entry.find("{http://www.w3.org/2005/Atom}published").text

            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text

            entry_id = entry.find("{http://www.w3.org/2005/Atom}id").text

            authors = []

            for author in entry.findall("{http://www.w3.org/2005/Atom}author"):
                name = author.find("{http://www.w3.org/2005/Atom}name").text
                authors.append(name)

            cleaned_metadata.append({
                "title": title,
                "authors": authors,
                "published": published,
                "summary": summary,
                "url": entry_id,
                "source": "arxiv"
            })

        if not cleaned_metadata:
            return {"error": "No papers found"}, 404

        existing_metadata = load_file()
        existing_metadata.extend(cleaned_metadata)
        save_data(existing_metadata)

        return cleaned_metadata, 200

    except requests.RequestException:
        return {"error": "Connection failed"}, 500