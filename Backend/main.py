# main.py
from flask import Flask, request, jsonify
from db import (
    create_tables,
    insert_student,
    get_student_id,
    save_papers,
    get_papers_by_user,
    delete_paper_by_id
)
from search import search_papers
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

create_tables()


@app.route("/search", methods=["GET"])
def search():

    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query parameter 'q' required"}), 400

    try:
        results =  search_papers(query)

        if not results:
            return jsonify([]), 200
        
        return jsonify(results)
        
        

    except Exception as e:
        print("SEARCH ERROR:", e)
        return jsonify({"error": "Something went wrong"}), 500
       

        

@app.route("/login", methods=["POST"])
def login():

    
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "username required"}), 400

    user_id = get_student_id(username)

    if not user_id:
        user_id = insert_student(username)

    return jsonify({
        "user_id": user_id,
        "username": username
    })



@app.route("/save", methods=["POST"])
def save():

    data = request.json

    user_id = data.get("user_id")
    query = data.get("query")
    papers = data.get("papers")

    if not user_id or not papers:
        return jsonify({"error": "user_id and papers required"}), 400

    try:
        save_papers(user_id, query, papers)
        return jsonify({"message": "papers saved"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/saved/<int:user_id>", methods=["GET"])
def saved(user_id):

    try:
        results = get_papers_by_user(user_id)
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/papers/<int:paper_id>", methods=["DELETE", "OPTIONS"])
def delete_paper(paper_id):

    if request.method == "OPTIONS":
        return "", 200

    try:
        delete_paper_by_id(paper_id)
        return jsonify({"message": "Paper deleted"}), 200

    except Exception as e:
        print("DELETE ERROR:", e)
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)