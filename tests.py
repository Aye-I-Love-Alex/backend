# pip install pytest
# pytest tests.py
from Connection import Connection


def test_init_parents_1_normal():
    links = ['link1', 'link2', 'link3', 'link4', 'link5']
    topic = 'topic'
    parents = Connection.init_parents(None, links, topic)
    expected_parents = {'link1': 'topic', 'link2': 'topic', 'link3': 'topic', 'link4': 'topic', 'link5': 'topic'}
    assert parents == expected_parents, 'Incorrect return for dictionary of links to topics.'
    assert links == ['link1', 'link2', 'link3', 'link4', 'link5'], 'First parameter was unintentionally altered.'
    assert topic == 'topic', 'Second parameter was unintentionally altered.'


def test_init_parents_2_no_links():
    links = []
    topic = 'topic'
    parents = Connection.init_parents(None, links, topic)
    expected_parents = {}
    assert parents == expected_parents, 'Incorrect return for dictionary of links to topics.'
    assert links == [], 'First parameter was unintentionally altered.'
    assert topic == 'topic', 'Second parameter was unintentionally altered.'
