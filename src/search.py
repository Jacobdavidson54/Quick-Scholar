# search.py
from src.cache import get_cache, set_cache
from src.db import get_papers_by_query, save_papers, insert_search_history
from src.fetch import fetch_all_sources
from src.utils import sort_by_year, normalize_results


async def search_papers(query):

    insert_search_history(query)

    cached = get_cache(query)
    if cached:
        print("Cache hit for query:", query)
        return cached

    db_results = get_papers_by_query(query)
    if db_results:
        print("Database hit for query:", query)
        set_cache(query, db_results)
        return db_results

    print("Fetching from APIs for query:", query)
    all_results = await fetch_all_sources(query)

    if not all_results:
        return []

    
    all_results = normalize_results(all_results)
    all_results = sort_by_year(all_results)

    set_cache(query, all_results)
    save_papers(query, all_results)

    return all_results