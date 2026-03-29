# main.py
from flask import Flask, request, jsonify
from src.db import create_tables
from src.search import search_papers

# Bug fix : removed the old Flask app code and replaced it with a new implementation that initializes the file, sets up a single /search endpoint, and uses asynchronous calls to fetch data from all sources. This new structure ensures better performance and a cleaner separation of concerns, while also providing more robust error handling and response formatting.

app = Flask(__name__)

create_tables()



@app.route("/search", methods=["GET"])
async def search():
   
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query parameter 'q' required"}), 400

    try:

        results = await search_papers(query)
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

