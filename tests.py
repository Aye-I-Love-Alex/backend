# pip install pytest
# pytest tests.py
from Connection import Connection

def test_find_connection_1():
    conn = Connection('Hawaii','Barack Obama')
    a = (conn.first_page["hits"]["hits"][0]["_source"]["links"])
    b = conn.second_page["hits"]["hits"]
    for thing in b:
        print(thing["_source"]["title"] + ': ' + str(len(thing["_source"]["links"])))
    assert False, len(b) > 0
