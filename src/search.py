# search.py
from src.fetch import fetch_semantic_papers, fetch_crossref_metadata, fetch_openalex_results, fetch_arxiv_data
from src.utils import normalize_results
def search_papers(query):

    all_results = []

    semantic_results, status1 = fetch_semantic_papers(query)
    if status1 == 200:
        all_results.extend(semantic_results)

    crossref_results, status2 = fetch_crossref_metadata(query)
    if status2 == 200:
        all_results.extend(crossref_results)

    openalex_results, status3 = fetch_openalex_results(query)
    if status3 == 200:
        all_results.extend(openalex_results)

    arxiv_results, status4 = fetch_arxiv_data(query)
    if status4 == 200:
        all_results.extend(arxiv_results)

    if not all_results:
        return {"error": "No papers found"}, 404
    
    # FIXED Bug: normalize AFTER collecting data
    all_results = normalize_results(all_results)
    
    return all_results, 200