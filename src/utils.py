# utils.py
import unicodedata
import re



# normalize a single string
def normalize_string(text):

    if not text:
        return ""

    text = text.lower()

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")


    # bug fix: Cleaned text by removing punctuation and extra spaces, so words are neat and searchable.
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()


    text = text.strip()

    return text


# normalize list of papers
def normalize_results(results):

    for paper in results:

        if "title" in paper:
            paper["title"] = normalize_string(paper["title"])

    return results

# Upgrade : Added a new function normalize_and_score that not only normalizes the results but also assigns a relevance score based on keyword matches, recency, citation count, and source credibility. This allows for more meaningful sorting and ranking of search results, providing users with the most relevant papers at the top of the list. The function also limits the number of results returned to a specified maximum for better performance and user experience.
def normalize_and_score(results, query , max_results = 50):

    normalized_results = []
    seen_titles = set()
    



    query_lower = normalize_string(query)
    query_keywords = set(query_lower.split())

    current_year = 2026

    for paper in results:
        title = normalize_string(paper.get("title", ""))
        year = int(paper.get("year") or 0)
        citations = int(paper.get("citations") or 0)
        source = paper.get("source", "")

        if not title or len(title) < 5 or title in seen_titles:
            continue
        seen_titles.add(title)

        if not title or len(title.strip()) < 5:
            continue

        if source == "crossrref" and citations == 0 and len(title.split()) < 3 :
            continue

        if year and year < 2000:
            continue

        score = 0

        # Keyword relevance
        if any(word in title for word in query_keywords):
            score += 10


        # Recency

        if year:
            score += max(0, 10 - (current_year - year))

        # Citation count
        if citations:
            score += min(citations, 30)

        # Source weight
        if source:
            score += 5 if source == "openalex" else 3 if source == "crossref" else 1

        normalized_results.append({
            "title": title,
            "year": year,
            "citations": citations,
            "source": source,
            "score": score
        })

    # Sorted by score descending, then year descending
    normalized_results.sort(key=lambda x: (x["score"], x["year"]), reverse=True)

    return normalized_results[:max_results]

    

