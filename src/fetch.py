# fetch.py
import asyncio
import aiohttp


async def fetch_openalex_results(session, search):

    url = "https://api.openalex.org/works"

    params = {
        "search": search,
        "per_page": 15
    }

    try:
        timeout = aiohttp.ClientTimeout(total=10)

      
        async with session.get(url, params=params, timeout=timeout) as response:
            response.raise_for_status()
            raw_info = await response.json()

        results = raw_info.get("results", [])

        if not results:
            return []

        cleaned_info = []

        for info in results:
            location = info.get("primary_location") or {}

            cleaned_info.append({
                "title": info.get("title", ""),

  
                "pdf_url": location.get("pdf_url"),
                "doi": info.get("doi"),
                "url": info.get("id"),

                "year": info.get("publication_year") if isinstance(info.get("publication_year"), int) else 0,
                "citations": info.get("cited_by_count") if isinstance(info.get("cited_by_count"), int) else 0,
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


async def fetch_all_sources(query):

    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        results = await fetch_openalex_results(session, query)
        return results