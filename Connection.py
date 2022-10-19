from elasticsearch import Elasticsearch
from ConnectionInterface import ConnectionInterface


class Connection(ConnectionInterface):

    es = Elasticsearch("http://localhost:9200")

    first_page = {}
    first_links = []
    first_topic = ""

    second_page = {}
    second_links = []
    second_topic = ""

    result_tree = {}

    def __init__(self, first_topic, second_topic):
        self.first_page, self.first_links, self.first_topic = self.get_page_info(first_topic)
        self.second_page, self.second_links, self.second_topic = self.get_page_info(second_topic)

    def get_page_info(self, topic):
        page = self.es.search(
            index="wikipedia_pages", body={"query": {"match": {"title": topic}}}
        )
        hits = page["hits"]["hits"]
        links = []
        title = []
        # if there are no hits in the database, leave arrays blank
        if len(hits) > 0:
            # return the info for the hit with the most outgoing links
            max_links = 0
            for hit in hits:
                if max_links < len(hit["_source"]["links"]):
                    max_links = len(hit["_source"]["links"])
                    links = hit["_source"]["links"]
                    title = hit["_source"]["title"]
        return page, links, title

    # Generating path when BFS finds a path
    def generate_path(self, first_parents, second_parents, common):
        path = []
        path.append(common)
        child = common

        # Adding to front for first topic's path
        while child in first_parents:
            parent = first_parents[child]
            path.insert(0, parent)
            child = parent

        child = common
        # Adding to back for second topic's path
        while child in second_parents:
            parent = second_parents[child]
            path.append(parent)
            child = parent

        return path

    # Bidirectional BFS logic here
    def find_all_connections(self):

        paths = []
        # Storing all of the links for the first and second topics separately
        first_topic_links = self.first_links.copy()
        second_topic_links = self.second_links.copy()

        # Storing the parents for each link
        first_parents = {}
        for link in self.first_links:
            first_parents[link] = self.first_topic

        second_parents = {}
        for link in self.second_links:
            second_parents[link] = self.second_topic

        # Storing the seen links for the first and second topic separately
        first_seen_links = []
        first_seen_links.append(self.first_topic)
        second_seen_links = []
        second_seen_links.append(self.second_topic)

        # Only iterating for 1000 iterations currently
        max_iter = 1000
        current_iter = 0

        # Only continuing while there are still links in both topics and the maximum number of iterations
        # has not been reached yet
        while (
            len(first_topic_links) != 0 or len(second_topic_links) != 0
        ) and current_iter < max_iter:
            current_link = ""

            # Only continuing if there are links remaining for the first topic
            if len(first_topic_links) != 0:
                current_link = first_topic_links.pop(0)

                # Path found in this case, appending to list of completed paths
                if current_link in second_seen_links:
                    paths.append(
                        self.generate_path(first_parents, second_parents, current_link)
                    )

                # Appending to seen links
                if current_link not in first_seen_links:
                    first_seen_links.append(current_link)

                # Expanding current_link and storing for future work
                result = self.es.search(
                    index="wikipedia_pages",
                    body={"query": {"match": {"title": current_link}}},
                )

                # Ensuring there are actual results, storing links from the current page and
                # storing the children for future expansion and saving the parents of the children
                if len(result["hits"]["hits"]) > 0:
                    result_links = result["hits"]["hits"][0]["_source"]["links"]
                    for link in result_links:
                        if link not in first_seen_links:
                            first_topic_links.append(link)
                            first_parents[link] = current_link

            # Only continuing if there are links remaining for the second topic
            if len(second_topic_links) != 0:
                current_link = second_topic_links.pop(0)
                if current_link in first_seen_links:
                    # Path found in this case
                    paths.append(
                        self.generate_path(first_parents, second_parents, current_link)
                    )

                # Appending to seen links if necessary
                if current_link not in second_seen_links:
                    second_seen_links.append(current_link)

                # Ensuring there are actual results, storing links from the current page and
                # storing the children for future expansion and saving the parents of the children
                result = self.es.search(
                    index="wikipedia_pages",
                    body={"query": {"match": {"title": current_link}}},
                )
                if len(result["hits"]["hits"]) > 0:
                    result_links = result["hits"]["hits"][0]["_source"]["links"]
                    for link in result_links:
                        if link not in second_seen_links:
                            second_topic_links.append(link)
                            second_parents[link] = current_link

            current_iter += 1

        # Returning array of array of paths
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
