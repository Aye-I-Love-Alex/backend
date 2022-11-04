import unittest
from comparator import add_a_node, add_a_edge, build_network

# pytest tests.py
from Connection import Connection


def test_example():
    assert True


def test_find_connection_1():
    connection = Connection('Hawaii', 'Barack Obama')
    b = connection.second_page["hits"]["hits"]
    
    '''
    for element in b:
        print(element["_source"]["title"] + ': ' +
              str(len(element["_source"]["links"])))
    '''
    assert True, len(b) > 0


def test_init_parents_1_normal():
    links = ['link1', 'link2', 'link3', 'link4', 'link5']
    topic = 'topic'
    parents = Connection.init_parents(None, links, topic)
    expected_parents = {'link1': 'topic', 'link2': 'topic',
                        'link3': 'topic', 'link4': 'topic', 'link5': 'topic'}

    assert parents == expected_parents, 'Incorrect return for dictionary of links to topics.'
    assert links == ['link1', 'link2', 'link3', 'link4',
                     'link5'], 'First parameter was unintentionally altered.'
    assert topic == 'topic', 'Second parameter was unintentionally altered.'


def test_init_parents_2_no_links():
    links = []
    topic = 'topic'
    parents = Connection.init_parents(None, links, topic)
    expected_parents = {}

    assert parents == expected_parents, 'Incorrect return for dictionary of links to topics.'
    assert links == [], 'First parameter was unintentionally altered.'
    assert topic == 'topic', 'Second parameter was unintentionally altered.'


class fake_graph():
    def __init__(self):
        self.nodes = 0
        self.edges = 0

    def add_node(self, string, color='blue'):
        self.nodes = self.nodes + 1
        print("add node called")

    def add_edge(self, string_1, string_2, weight, color='blue'):
        self.edges = self.edges + 1
        print("add edge called")


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
    test_find_connection_1()
    test_init_parents_1_normal()
    test_init_parents_2_no_links


if __name__ == "__main__":
    main()
    print("All tests passed")
