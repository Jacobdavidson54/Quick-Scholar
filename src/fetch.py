# fetch.py
import aiohttp
import asyncio
import xml.etree.ElementTree as ET
# Removed request module for asynchttp and aiohttp for better performance and non-blocking calls to APIs.

# Upgrade : removed the loading and saving logic from fetch.py to utils.py to centralize file handling and keep fetch.py focused on data retrieval from APIs. This separation of concerns makes the code cleaner and easier to maintain.

# Bug fix : remove Semantic Scholar API function ,because they have strict rate limits and often return 404 and 400 errors, which can disrupt the user experience. By removing it, we can focus on more reliable sources like CrossRef, OpenAlex, and arXiv for fetching research papers.
async def fetch_crossref_metadata(session, query):

    url = "https://api.crossref.org/works"

    headers = {
        "User-Agent": "QuickScholar/1.0 (mailto:nergtonicsa@gmail.com)"
    }

    params = {
        "query": query,
        "rows": 5
    }

    try:
        async with session.get(url, headers=headers, params=params) as response:
            response.raise_for_status()
            raw_data = await response.json()

        items = raw_data.get("message", {}).get("items", [])

        if not items:
            return []

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

        return cleaned_results

    except Exception:
        return []


async def fetch_openalex_results(session, search):

    url = "https://api.openalex.org/works"

    params = {
        "search": search,
        "per_page": 5
    }

    try:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            raw_info = await response.json()

        results = raw_info.get("results", [])

        if not results:
            return []

        cleaned_info = []

        for info in results:
            location = info.get("primary_location") or {}

            cleaned_info.append({
                "title": info.get("title"),
                "abstract": None,
                "full_text": location.get("pdf_url"),
                "year": info.get("publication_year"),
                "citations": info.get("cited_by_count"),
                "source": "openalex"
            })

        return cleaned_info

    except Exception:
        return []


async def fetch_arxiv_data(session, query):

    url = "http://export.arxiv.org/api/query"

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": 5
    }

    try:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            content = await response.text()

        root = ET.fromstring(content)

        cleaned_metadata = []

        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):

            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            published = entry.find("{http://www.w3.org/2005/Atom}published").text

            cleaned_metadata.append({
                "title": title,
                "year": int(published[:4]) if published else None,
                "citations": 0,
                "source": "arxiv"
            })

        return cleaned_metadata

    except Exception:
        return []


async def fetch_all_sources(query):

    async with aiohttp.ClientSession() as session:

        results = await asyncio.gather(
            fetch_crossref_metadata(session, query),
            fetch_openalex_results(session, query),
            fetch_arxiv_data(session, query)
        )

        combined = []
        for source in results:
            combined.extend(source)

        return combined