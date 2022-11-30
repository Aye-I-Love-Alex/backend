from Connection import Connection
from flask import Flask, render_template, request, send_file
import networkx as nx
from pyvis.network import Network

app = Flask(__name__, static_folder="graph")
GRAPH_LOCATION = "./graph/graph.html"
PATH_LOCATION = "./graph/paths.html"


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("index.html")


@app.route("/bengals.html", methods=["POST", "GET"])
def bengals():
    messages = []
    candidate_paths = []
    if request.method == "POST":
        head_con = 'cincinnati bengals'
        candidate_paths = find_paths(head_con, request.form)

    return render_template("bengals.html", connections=candidate_paths, messages=messages)

@app.route("/browns.html", methods=["POST", "GET"])
def browns():
    messages = []
    candidate_paths = []
    if request.method == "POST":
        head_con = 'cleveland browns'
        candidate_paths = find_paths(head_con, request.form)

    return render_template("browns.html", connections=candidate_paths, messages=messages)

@app.route("/dolphins.html", methods=["POST", "GET"])
def raiders():
    messages = []
    candidate_paths = []
    if request.method == "POST":
        head_con = 'miami dolphins'
        candidate_paths = find_paths(head_con, request.form)

    return render_template("dolphins.html", connections=candidate_paths, messages=messages)

# Method to find the paths for the connections
def find_paths(first_connection, form):
    paths = []
    candidates = form.get("candidates").split(",")
    max_iterations = form.get("maximumiterations")
    intense = form.get("intensity")
    for candidate in candidates:
        if len(candidate) > 0 and first_connection.lower() != candidate.lower():
            connection = Connection(first_connection, candidate, intense)
            path, messages = connection.find_all_connections(max_iter = max_iterations)
            if len(path) > 0:
                paths.append(', '.join(stop for stop in path))
    return paths

@app.route("/graph/graph.html")
def show_graph():
    return send_file(GRAPH_LOCATION)


if __name__ == "__main__":
    app.run(debug=True)
