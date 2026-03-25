# main.py
from flask import Flask, request, jsonify
from src.utils import initialize_file
from src.fetch import fetch_all_sources
from src.utils import normalize_results

# Bug fix : removed the old Flask app code and replaced it with a new implementation that initializes the file, sets up a single /search endpoint, and uses asynchronous calls to fetch data from all sources. This new structure ensures better performance and a cleaner separation of concerns, while also providing more robust error handling and response formatting.

app = Flask(__name__)

initialize_file()

@app.route("/search", methods=["GET"])
async def search():
   
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query parameter 'q' required"}), 400

    try:
  
        all_results = await fetch_all_sources(query)

  
        if not all_results:
            return jsonify({"error": "No papers found"}), 404


        all_results = normalize_results(all_results)

        # 4️⃣ Optionally: ranking & sorting logic can go here
        # sorted_results = rank_and_sort(all_results)

        return jsonify(all_results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

