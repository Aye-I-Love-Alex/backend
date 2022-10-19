from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup
import os.path

es = Elasticsearch("http://localhost:9200")

result = es.search(
    index="wikipedia_pages", body={"query": {"match": {"title": "ohio"}}}
)
print(result["hits"]["hits"][0]["_source"])
# test_topics = [
#     "Cincinnati Reds",
#     "World Series",
#     "Ohio",
#     "William Howard Taft",
#     "Cincinnati",
#     "Charles Manson",
#     "Barack Obama",
#     "Joe Biden",
# ]

# for topic in test_topics:
#     with open(
#         "testTopics/Documents/" + topic.replace(" ", "_") + ".html", encoding="utf8"
#     ) as fp:
#         current_links = []
#         soup = BeautifulSoup(fp, "html.parser")
#         text = soup.get_text()
#         for link in soup.find_all("a"):
#             if "id" in link.attrs and "xolnki" in link.get("id"):
#                 if (
#                     link.text in test_topics
#                     and link.text not in current_links
#                     and link.text != topic
#                 ):
#                     current_links.append(link.text)
#         page = {"title": topic, "full_text": text, "links": current_links}
#         es.index(index="wikipedia_pages", document=page)

# Sample query to return information from ElasticSearch after insertion
# resp = es.search(
#     index="wikipedia_pages", body={"query": {"match": {"title": "Cincinnati Reds"}}}
# )
# print(resp)


# Creating index for pages
# mappings = {
#     "properties": {
#         "title": {"type": "text", "analyzer": "english"},
#         "full_text": {"type": "text", "analyzer": "standard"},
#         "links": {"type": "text", "analyzer": "standard"},
#     }
# }
# es.indices.create(index="wikipedia_pages", mappings=mappings)

# Simple line to delete index, if necessary
# es.options(ignore_status=[400,404]).indices.delete(index='wikipedia_pages')
