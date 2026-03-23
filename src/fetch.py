# fetch.py
import asyncio
import xml.etree.ElementTree as ET
import aiohttp
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
        "rows": 15
    }

    try:
        timeout = aiohttp.ClientTimeout(total = 10) # Bug fix: Added a timeout to prevent hanging requests and improve user experience when the API is slow or unresponsive.
        async with session.get(url, headers=headers, params=params, timeout=timeout) as response:
            response.raise_for_status()
            raw_data = await response.json()

        items = raw_data.get("message", {}).get("items", [])

        if not items:
            return []

        cleaned_results = []

        for item in items:
            title = item.get("title", [""])
            year = item.get("issued", {}).get("date-parts", [[0]])[0][0]
            citations = item.get("is-referenced-by-count", 0)

        for item in items:
            cleaned_results.append({
                "title": title[0] if title else "",
                "year": year if isinstance(year, int) else 0,
                "citations": citations if isinstance(citations, int) else 0,
                "authors": item.get("author"),
                "doi": item.get("DOI"),
                "url": item.get("URL"),
                "publisher": item.get("publisher"),
                "source": "crossref"
            })

        return cleaned_results
# Bug fix : Added specific exception handling for aiohttp.ClientError and asyncio.TimeoutError to provide clearer error messages and prevent the entire application from crashing due to API issues. This ensures that if one API fails, the others can still return results without interruption. Additionally, a general exception catch is included to handle any unforeseen errors gracefully.
    except aiohttp.ClientError as e:
        print(f"CrossRef API error: {e}")
        return []
    except asyncio.TimeoutError:
        print("CrossRef API timeout")
        return []
    except Exception as e: # Notice : This code line is still going  to be fixed in the future, because it is a general exception catch that can hide specific issues. In a production environment, it's better to handle specific exceptions and log them appropriately rather than catching all exceptions in a broad manner.
        print(f"Unexpected error in CrossRef API: {e}")
        return []

       
async def fetch_openalex_results(session, search):

    url = "https://api.openalex.org/works"

    params = {
        "search": search,
        "per_page": 15
    }

    try:
        timeout = aiohttp.ClientTimeout(total = 10)
        async with session.get(url, params=params, timeout=timeout) as response:
            response.raise_for_status()
            raw_info = await response.json()

        results = raw_info.get("results", [])

        if not results:
            return []

        cleaned_info = []

        for info in results:
            location = info.get("primary_location") or {}
            title = info.get("title")
            year = info.get("publication_year")
            citations = info.get("cited_by_count")

            cleaned_info.append({
                "title": title if title else "",
                "abstract": None,
                "full_text": location.get("pdf_url"),
                "year": year if isinstance(year, int) else 0,
                "citations": citations if isinstance(citations, int) else 0,
                "source": "openalex"
            })

        return cleaned_info

    except aiohttp.ClientError as e:
        print(f"OpenAlex API error: {e}")
        return []
    except asyncio.TimeoutError:
        print("OpenAlex API timeout")
        return []
    except Exception as e:
        print(f"Unexpected error in OpenAlex API: {e}")
        return []


async def fetch_arxiv_data(session, query):

    url = "http://export.arxiv.org/api/query"

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": 15
    }

    try:
        timeout = aiohttp.ClientTimeout(total = 10)
        async with session.get(url, params=params, timeout=timeout) as response:
            response.raise_for_status()
            content = await response.text()

        root = ET.fromstring(content)

        cleaned_metadata = []

        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):

            title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
            published_elem = entry.find("{http://www.w3.org/2005/Atom}published").text

            published = published_elem.strip() if published_elem is not None else "" 

            cleaned_metadata.append({
                "title": title if title is not None else "",
                "year": int(published[:4]) if published else None,
                "citations": 0,
                "source": "arxiv"
            })

        return cleaned_metadata

    except aiohttp.ClientError as e:
        print(f"arXiv API error: {e}")
        return []
    except asyncio.TimeoutError:
        print("arXiv API timeout")
        return []
    except Exception as e:
        print(f"Unexpected error in arXiv API: {e}")
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