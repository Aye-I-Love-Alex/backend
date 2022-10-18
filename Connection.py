from elasticsearch import Elasticsearch
from ConnectionInterface import ConnectionInterface


class Connection(ConnectionInterface):

    es = Elasticsearch("http://localhost:9200")

    first_page = {}
    second_page = {}

    result_tree = {}

    def __init__(self, first_topic, second_topic):
        self.first_page = self.es.search(
            index="wikipedia_pages", body={"query": {"match": {"title": first_topic}}}
        )
        self.second_page = self.es.search(
            index="wikipedia_pages", body={"query": {"match": {"title": second_topic}}}
        )

    # BFS logic here for MVP
    def find_connection(self):
        first_links = self.first_page["hits"]["hits"][0]["_source"]["links"]
        first_topic = self.first_page["hits"]["hits"][0]["_source"]["title"]
        parent_queue = [first_topic] * len(first_links)

        second_topic = self.second_page["hits"]["hits"][0]["_source"]["title"]

        path = []
        seen_links = first_links.copy()
        seen_links.append(first_topic)
        cont = True
        while len(first_links) != 0 and cont:
            current_link = first_links.pop(0)
            self.result_tree[current_link] = parent_queue.pop(0)
            if current_link == second_topic:
                iter_back = current_link
                while iter_back != first_topic:
                    path.append(iter_back)
                    iter_back = self.result_tree[iter_back]
                path.append(first_topic)
                cont = False
            else:
                result_links = self.es.search(
                    index="wikipedia_pages",
                    body={"query": {"match": {"title": current_link}}},
                )["hits"]["hits"][0]["_source"]["links"]
                for link in result_links:
                    if link not in seen_links:
                        seen_links.append(link)
                        first_links.append(link)
                        parent_queue.append(current_link)
        path.reverse()
        return path
