import wikipediaapi
from elasticsearch import Elasticsearch
from ConnectionInterface import ConnectionInterface


class Connection(ConnectionInterface):

    wikipedia = wikipediaapi.Wikipedia("en")
    es = Elasticsearch("http://localhost:9200")

    first_page = {}
    first_links = []
    first_topic = ''

    second_page = {}
    second_links = []
    second_topic = ''

    result_tree = {}

    def __init__(self, first_topic, second_topic):
        self.first_page = self.es.search(
            index="wikipedia_pages", body={"query": {"match": {"title": first_topic}}}
        )
        self.first_links = self.first_page["hits"]["hits"][0]["_source"]["links"]
        self.first_topic = self.first_page["hits"]["hits"][0]["_source"]["title"]
        
        self.second_page = self.es.search(
            index="wikipedia_pages", body={"query": {"match": {"title": second_topic}}}
        )
        self.second_links = self.second_page["hits"]["hits"][0]["_source"]["links"]
        self.second_topic = self.second_page["hits"]["hits"][0]["_source"]["title"]

    def generate_path(self):
        return ''

    # Bidirectional BFS logic here for MVP
    def find_all_connections(self):

        paths = {}
        first_topic_links = self.first_links.copy()
        second_topic_links = self.first_links.copy()
        seen_links = self.first_links.copy()
        seen_links.append(self.first_topic)
        seen_links.append(self.second_links.copy())
        seen_links.append(self.second_topic)
        max_iter = 1000
        current_iter = 0
        while (len(first_topic_links) != 0 or len(second_topic_links) != 0) and current_iter < max_iter:
            current_link = ''
            links_to_expand = []
            if len(first_topic_links) != 0:
                current_link = first_topic_links.pop(0) 
                links_to_expand.append(current_link)           
                if current_link in seen_links:
                    # Path found in this case
                    paths.append(self.generate_path())
                seen_links[current_link] = 1
            
            if len(second_topic_links) != 0:
                current_link = second_topic_links.pop(0) 
                links_to_expand.append(current_link)
                if current_link in seen_links:
                    # Path found in this case
                    paths.append(self.generate_path())
                seen_links[current_link] = 2

            for key, value in links_to_expand.items():
                result_links = self.es.search(
                    index="wikipedia_pages",
                    body={"query": {"match": {"title": current_expansion}}},
                )["hits"]["hits"][0]["_source"]["links"]
                for link in result_links:
                    if link not in seen_links:
                        if value == 0:
                            first_topic_links.append(link)
                        else:
                            second_topic_links.append(link)


            self.result_tree[current_link] = parent_queue.pop(0)
            if current_link == second_topic:
                iter_back = current_link
                while iter_back != first_topic:
                    path.append(iter_back)
                    iter_back = self.result_tree[iter_back]
                path.append(first_topic)
            else:

        path.reverse()
        current_iter += 1
        return paths

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
