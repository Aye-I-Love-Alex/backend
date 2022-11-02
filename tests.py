import unittest
from comparator import add_a_node, add_a_edge, build_network

class fake_graph():
    def __init__(self):
        self.nodes = 0
        self.edges = 0

    def add_node(self, string, color='blue'):
        self.nodes = self.nodes + 1
        print("add node called")

    def add_edge(self, string_1, string_2, weight, color = 'blue'):
        self.edges = self.edges + 1
        print("add edge called")

def test_example():
    assert True

def test_add_node_not_in_nodes():
    current_path = ["String"]
    element_index = 0
    graph = fake_graph()
    nodes = set()
    add_a_node(current_path, element_index, graph, nodes)
    assert len(nodes) == 1, "Should be 1"

def test_add_node_in_nodes():
    current_path = ["String"]
    element_index = 0
    graph = fake_graph()
    nodes = {"String"}
    add_a_node(current_path, element_index, graph, nodes)
    assert len(nodes) == 1, "Should be 1"

def main():
    test_example()
    test_add_node_not_in_nodes()
    test_add_node_in_nodes()

if __name__ == "__main__":
    main()
    print("All tests passed")