# main.py
from flask import Flask, request, jsonify
from src.db import create_tables
from src.search import search_papers
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

create_tables()


@app.route("/search", methods=["GET"])
async def search():

    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query parameter 'q' required"}), 400

    try:
        results = await search_papers(query)
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

