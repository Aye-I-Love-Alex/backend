from elasticsearch import Elasticsearch
from ConnectionInterface import ConnectionInterface

MAX_ITER = 1000


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
        self.first_page = self.es.search(index="wikipedia_pages", body={"query": {"match": {"title": first_topic}}})
        if len(self.first_page["hits"]["hits"]) > 0:
            self.first_links = self.first_page["hits"]["hits"][0]["_source"]["links"]
            self.first_topic = self.first_page["hits"]["hits"][0]["_source"]["title"]

        self.second_page = self.es.search(index="wikipedia_pages", body={"query": {"match": {"title": second_topic}}})
        if len(self.second_page["hits"]["hits"]) > 0:
            self.second_links = self.second_page["hits"]["hits"][0]["_source"]["links"]
            self.second_topic = self.second_page["hits"]["hits"][0]["_source"]["title"]

    # Generating path when BFS finds a path
    def generate_path(self, first_parents, second_parents, common):
        path = [common]
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

        # remove front and end 'None' because of initialization of parents
        path.pop(0)
        path.pop()

        return path

    # Bidirectional BFS logic here
    def find_all_connections(self, max_iter=MAX_ITER):
        paths = []

        # Initialize topic links, parents, and seen links for first and second links
        # topic links are the links we have yet to explore/expand to get more links
        # parents are dictionaries recording child:parent for path generation
        # seen links are links that have been explored/expanded
        first_topic_links = []
        first_parents = {self.first_topic: None}
        first_seen_links = {self.first_topic}
        for link in self.first_links:
            if link not in first_parents:
                first_topic_links.append(link)
                first_parents[link] = self.first_topic

        second_topic_links = []
        second_parents = {self.second_topic: None}
        second_seen_links = {self.second_topic}
        for link in self.second_links:
            if link not in second_parents:
                second_topic_links.append(link)
                second_parents[link] = self.second_topic

        # Initialize iteration counter
        current_iter = 0

        # Only continuing while there are still links in both topics and the maximum number of iterations
        # has not been reached yet
        while (
            len(first_topic_links) != 0 or len(second_topic_links) != 0
        ) and current_iter < max_iter:

            # pop off queue of links to explore
            if len(first_topic_links) != 0:
                current_link = first_topic_links.pop(0)

                # check if the node has been seen by the other BFS direction (second link)
                if current_link in second_parents:
                    # if so, generate a path and add to the list of paths for graph generation
                    paths.append(self.generate_path(first_parents, second_parents, current_link))
                else:
                    # if not, expand and add new links if we have not already seen them from this direction
                    result = self.es.search(
                        index="wikipedia_pages",
                        body={"query": {"match": {"title": current_link}}},
                    )
                    first_seen_links.add(current_link)
                    if len(result["hits"]["hits"]) > 0:
                        result_links = result["hits"]["hits"][0]["_source"]["links"]
                        for link in result_links:
                            if link not in first_parents:
                                first_topic_links.append(link)
                                first_parents[link] = current_link

            # pop off queue of links to explore
            if len(second_topic_links) != 0:
                current_link = second_topic_links.pop(0)

                # check if the node has been seen by the other BFS direction (first link)
                if current_link in first_parents:
                    # if so, generate a path and add to the list of paths for graph generation
                    paths.append(self.generate_path(first_parents, second_parents, current_link))
                else:
                    # if not, expand and add new links if we have not already seen them from this direction
                    result = self.es.search(
                        index="wikipedia_pages",
                        body={"query": {"match": {"title": current_link}}},
                    )
                    second_seen_links.add(current_link)
                    if len(result["hits"]["hits"]) > 0:
                        result_links = result["hits"]["hits"][0]["_source"]["links"]
                        for link in result_links:
                            if link not in second_parents:
                                second_topic_links.append(link)
                                second_parents[link] = current_link

            current_iter += 1

        # Returning array of array of paths
        return paths
