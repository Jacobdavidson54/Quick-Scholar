def search_web(query: str):
    """
    This function handles the search logic.
    For now, it returns fake data.
    """
    return {
        "query": query,
        "results": [
            f"Result 1 for {query}",
            f"Result 2 for {query}",
            f"Result 3 for {query}"
        ]
    }
