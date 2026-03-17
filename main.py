# main.py

from flask import Flask, request, jsonify
from src.utils import initialize_file
from src.search import search_papers
app = Flask(__name__)

# Initialize JSON file at startup
initialize_file()

# bug fix: Removed the old search logic from main.py and imported the search_papers function from search.py to handle all search logic. This keeps main.py clean and focused on routing, while search.py manages the core functionality of fetching and normalizing paper data.

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