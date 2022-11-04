from Connection import Connection
from flask import Flask, render_template, request, send_file
import networkx as nx
from pyvis.network import Network

app = Flask(__name__, static_folder='graph')

def get_word(word_index):
    return request.form.get(word_index)

def add_a_node(current_path, element_index, graph, nodes):
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
        nodes.add(current_path[element_index])

def add_a_edge(element_index, current_path, graph, parent):
    # Checking if an edge should be added or not. Assigning parent accordingly
    if element_index == 0:
        return current_path[element_index]
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
            return ""
        else:
            graph.add_edge(
                parent, current_path[element_index], weight=1
            )
        return current_path[element_index]

def build_network(path):
    graph = nx.Graph()
    nodes = set()
    # Iterating through each path that was found
    for path_index in range(len(path)):
        current_path = path[path_index]
        parent = ""

        # Iterating through each element in the current path
        for element_index in range(len(current_path)):
            add_a_node(current_path, element_index, graph, nodes)
            temp = add_a_edge(element_index, current_path, graph, parent)
            if not temp == "":
                parent = temp
    return graph

@app.route("/", methods=["POST", "GET"])
def index():
    net = ""
    if request.method == "POST":
        first = get_word("firstword")
        second = get_word("secondword")
        if len(first) > 0 and len(second) > 0:
            connection = Connection(first, second)
            path = connection.find_all_connections()
            if len(path) > 0:
                graph = build_network(path)
                net = Network()
                net.from_nx(graph)
                net.save_graph("./graph/graph.html")
                
    return render_template("index.html", connection=net)


@app.route("/graph/graph.html")
def show_graph():
    return send_file("./graph/graph.html")


if __name__ == "__main__":
    app.run(debug=True)

