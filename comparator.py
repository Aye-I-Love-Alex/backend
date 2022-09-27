from Connection import Connection
from elasticsearch import Elasticsearch

# first_topic = input("First topic: ")
# second_topic = input("Second topic: ")

# conn = Connection(first_topic, second_topic)

# print(conn.first_links)
# print(conn.second_links)

# print(test.hyperlinks())

# print(current_page.exists())

es = Elasticsearch("http://localhost:9200")
es.info().body

# mappings = {
#     "properties": {
#         "title": {"type": "text", "analyzer": "english"},
#         "full_text": {"type": "text", "analyzer": "standard"},
#         "links": {
#             "type": "object",
#             "properties": {
#                 "key": {"type": "text", "index": "false"},
#                 "value": {"type": "text", "index": "false"},
#             }
#         }
#     }
# }

# es.indices.create(index="wikipedia_pages", mappings=mappings)

# first_doc = {
#     "title": first_topic,
#     "full_text": conn.first_text,
#     "links": conn.first_links
# }
# es.index(index="wikipedia_pages", document=first_doc)


# second_doc = {
#     "title": first_topic,
#     "full_text": conn.first_text,
#     "links": conn.first_links
# }
# es.index(index="wikipedia_pages", document=second_doc)

resp = es.search(index="wikipedia_pages", body={})
print(resp)
