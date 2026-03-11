# main.py
from flask import Flask, request, jsonify
from src.fetch import fetch_semantic_papers
from src.utils import initialize_file

app = Flask(__name__)

# Initialize JSON file at startup
initialize_file()

# --- Internal logic (main function) ---
def search_papers(query):
    """
    Main backend function for searching papers.
    Only Semantic Scholar for now.
    """
    results, status = fetch_semantic_papers(query)
    return results, status


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