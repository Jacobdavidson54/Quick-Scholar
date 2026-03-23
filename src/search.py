# search.py
import asyncio
from src.fetch import  fetch_all_sources
from src.utils import  normalize_and_score
# Bug fix : removed the old search logic and replaced it with a new function that calls fetch_all_sources to get data from all sources, then normalizes the results using normalize_results before returning them. This ensures that the search function is streamlined and leverages the improvements made in fetch.py and utils.py for better performance and cleaner code.

#upgrade : Imported the fetch_all_sources function from fetch.py to handle fetching data from all sources in a single function. This simplifies the search_papers function and keeps the fetching logic centralized in fetch.py, making it easier to maintain and update in the future.

# imported asyncio to run the asynchronous fetch_all_sources function within the search_papers function, allowing for efficient handling of multiple API calls without blocking the main thread.

def search_papers(query):

    all_results = asyncio.run(fetch_all_sources(query))

    if not all_results:
        return {"error": "No papers found"}, 404

# replaced the old normalization logic with a call to normalize_and_score, which not only normalizes the results but also scores them based on relevance to the query. This provides a more comprehensive processing of the results before they are returned to the user.
    all_results = normalize_and_score(all_results, query)

    return all_results, 200
