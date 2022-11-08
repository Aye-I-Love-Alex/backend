from Connection import Connection
from flask import Flask, render_template, request, send_file
import networkx as nx
from pyvis.network import Network
import pandas as pd

app = Flask(__name__, static_folder="graph")
GRAPH_LOCATION = "./graph/graph.html"


@app.route("/", methods=["POST", "GET"])
def index():
    net = ""
    messages = []
    if request.method == "POST":
        first = request.form.get("firstword")
        second = request.form.get("secondword")
        intense = request.form.get("intensity")
        if len(first) > 0 and len(second) > 0 and first.lower() != second.lower():
            connection = Connection(first, second, intense)
            path, messages = connection.find_all_connections()
            if len(path) > 0:
                graph = nx.Graph()
                nodes = []
                # Iterating through each path that was found
                for path_index in range(len(path)):
                    current_path = path[path_index]
                    parent = ""

                    # Iterating through each element in the current path
                    for element_index in range(len(current_path)):
                        # Ensuring that the current title has not already been added as a node
                        if current_path[element_index] not in nodes:
                            # Checking current index because that changes how the node's colors work
                            if (
                                element_index == 0
                                or element_index == len(current_path) - 1
                            ):
                                graph.add_node(current_path[element_index], color="red")
                            else:
                                graph.add_node(current_path[element_index])

                            # Ensuring that we don't add the node twice
                            nodes.append(current_path[element_index])

                        # Checking if an edge should be added or not. Assigning parent accordingly
                        if element_index == 0:
                            parent = current_path[element_index]
                        else:
                            # Checking current index because that changes how the edge's colors work
                            # Adding edges to graph
                            if element_index == len(current_path) - 1:
                                graph.add_edge(
                                    parent,
                                    current_path[element_index],
                                    weight=1,
                                    color="red",
                                )
                            else:
                                graph.add_edge(
                                    parent, current_path[element_index], weight=1
                                )
                            parent = current_path[element_index]

                net = Network()
                net.from_nx(graph)
                net.html = net.generate_html()
                with open(GRAPH_LOCATION, "w+") as out:
                    out.write(net.html)
        elif first.lower() == second.lower() and len(first) + len(second) > 0:
            messages.append("Please enter two different terms.")
        elif not (len(first) == 0 and len(second) == 0):
            messages.append("Please enter two terms.")

    return render_template("index.html", connection=net, messages=messages)


@app.route("/graph/graph.html")
def show_graph():
    return send_file(GRAPH_LOCATION)


if __name__ == "__main__":
    app.run(debug=True)
