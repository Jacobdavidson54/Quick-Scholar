from src.fetch import fetch_semantic_papers, fetch_crossref_metadata

def search_papers(query):

    all_results = []

    semantic_results, status1 = fetch_semantic_papers(query)
    if status1 == 200:
        all_results.extend(semantic_results)

    crossref_results, status2 = fetch_crossref_metadata(query)
    if status2 == 200:
        all_results.extend(crossref_results)

    if not all_results:
        return {"error": "No papers found"}, 404

    return all_results, 200