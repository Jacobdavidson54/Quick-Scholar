# main.py

from flask import Flask, request, jsonify
from src.fetch import fetch_crossref_metadata, fetch_semantic_papers, fetch_openalex_results
from src.utils import initialize_file

app = Flask(__name__)

# Initialize JSON file at startup
initialize_file()


# --- Internal logic (main function) ---
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

    if not all_results:
        return [], 404

    return all_results, 200


# --- Flask route ---
@app.route("/search", methods=["GET"])
def search():

    query = request.args.get("q")

    if not query:
        return jsonify({"error": "Query parameter 'q' required"}), 400

    results, status = search_papers(query)

    return jsonify(results), status


if __name__ == "__main__":
    app.run(debug=True)