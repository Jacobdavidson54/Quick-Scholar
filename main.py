from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route("/search", methods=["GET"])
def search():
    dummy_results = [{"Title":"The full history of African colonization", "link":"wwww.gogglescholar/history.com"},
                     {"Title":"Psychological and human behavior", "link":"www.psyinstitute.org"},
                     {"Title":"Universal software development framework", "link":"www.ABDinc.com"},
                     {"Title":"The analysis of human behavior", "link":"www.psyinstitute.org"}
                    ]
    return jsonify(dummy_results),200

if __name__ == "__main__" :
    app.run(debug=True)
    

