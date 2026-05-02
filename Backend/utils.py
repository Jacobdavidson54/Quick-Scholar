# utils.py
import unicodedata
import re



def normalize_string(text):
    if not text:
        return ""

    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text



def resolve_link(paper):
   

    if paper.get("pdf_url"):
        return paper["pdf_url"]

    if paper.get("doi"):
        doi = paper["doi"].replace("https://doi.org/", "")
        return f"https://doi.org/{doi}"

    return ""  



def normalize_results(results):

    cleaned = []
    seen_titles = set()  

    for paper in results:
        title_raw = paper.get("title", "")
        title = normalize_string(title_raw)

      
        if not title or len(title) < 5:
            continue


        if title in seen_titles:
            continue
        seen_titles.add(title)

        year = paper.get("year")
        year = year if isinstance(year, int) else 0

        citations = paper.get("citations")
        citations = citations if isinstance(citations, int) else 0

        source = paper.get("source", "openalex")

        link = resolve_link(paper)

   
        if not link:
            continue

      
        if year and year < 2000:
            continue

        cleaned.append({
            "title": title,
            "link": link,
            "year": year,
            "citations": citations,
            "source": source
        })

    return cleaned



def sort_by_year(results):
    return sorted(
        results,
        key=lambda x: x["year"] if x["year"] else 0,
        reverse=True
    )