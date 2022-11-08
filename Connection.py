from elasticsearch import Elasticsearch
from ConnectionInterface import ConnectionInterface
import math


class Connection(ConnectionInterface):

    es = Elasticsearch("http://localhost:9200")

    first_page = {}
    first_links = []
    first_topic = ""

    second_page = {}
    second_links = []
    second_topic = ""

    result_tree = {}
    error_messages = []

    intensity = 0

    def __init__(self, first_topic, second_topic, intensity):
        self.error_messages.clear()
        self.first_page = self.es.search(
            index="wikipedia_pages", body={"query": {"match": {"title": first_topic}}}
        )
        if len(self.first_page["hits"]["hits"]) > 0:
            self.first_links = self.first_page["hits"]["hits"][0]["_source"]["links"]
            self.first_topic = self.first_page["hits"]["hits"][0]["_source"]["title"]
        else:
            # no results in database for term
            self.error_messages.append(
                '"' + first_topic + '" yielded no results in simple Wikipedia.\n'
            )

        self.second_page = self.es.search(
            index="wikipedia_pages", body={"query": {"match": {"title": second_topic}}}
        )
        if len(self.second_page["hits"]["hits"]) > 0:
            self.second_links = self.second_page["hits"]["hits"][0]["_source"]["links"]
            self.second_topic = self.second_page["hits"]["hits"][0]["_source"]["title"]
        else:
            # no results in database for term
            self.error_messages.append(
                '"' + second_topic + '" yielded no results in simple Wikipedia.\n'
            )

        self.intensity = float(intensity) / 100

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
    def find_all_connections(self, max_iter):
        paths = []

        # Initialize topic links, parents, and seen links for first and second links
        # topic links are the links we have yet to explore/expand to get more links
        # parents are dictionaries recording child:parent for path generation
        # seen links are links that have been explored/expanded
        first_topic_links = []
        first_parents = {self.first_topic: None}
        first_seen_links = {self.first_topic}

        links_to_expand = math.ceil(self.intensity * len(self.first_links))
        links_inserted = 0
        for link in self.first_links:
            if link not in first_parents:
                first_topic_links.append(link)
                first_parents[link] = self.first_topic
                links_inserted += 1
            if links_inserted == links_to_expand:
                break

        second_topic_links = []
        second_parents = {self.second_topic: None}
        second_seen_links = {self.second_topic}

        links_to_expand = math.ceil(self.intensity * len(self.second_links))
        links_inserted = 0
        for link in self.second_links:
            if link not in second_parents:
                second_topic_links.append(link)
                second_parents[link] = self.second_topic
                links_inserted += 1

            if links_inserted == links_to_expand:
                break

        # Initialize iteration counter
        current_iter = 0

        valid_max_iter = 1000 if not max_iter.isnumeric() else int(max_iter)

        # Only continuing while there are still links in both topics and the maximum number of iterations
        # has not been reached yet
        while (
            len(first_topic_links) != 0 or len(second_topic_links) != 0
        ) and current_iter < valid_max_iter:

            # pop off queue of links to explore
            if len(first_topic_links) != 0:
                current_link = first_topic_links.pop(0)

                # check if the node has been seen by the other BFS direction (second link)
                if current_link in second_parents:
                    # if so, generate a path and add to the list of paths for graph generation
                    paths.append(
                        self.generate_path(first_parents, second_parents, current_link)
                    )
                else:
                    # if not, expand and add new links if we have not already seen them from this direction
                    result = self.es.search(
                        index="wikipedia_pages",
                        body={"query": {"match": {"title": current_link}}},
                    )
                    first_seen_links.add(current_link)
                    if len(result["hits"]["hits"]) > 0:
                        result_links = result["hits"]["hits"][0]["_source"]["links"]
                        links_to_expand = math.ceil(self.intensity * len(result_links))
                        links_inserted = 0
                        for link in result_links:
                            if link not in first_parents:
                                first_topic_links.append(link)
                                first_parents[link] = current_link
                                links_inserted += 1

                            if links_inserted == links_to_expand:
                                break

            # pop off queue of links to explore
            if len(second_topic_links) != 0:
                current_link = second_topic_links.pop(0)

                # check if the node has been seen by the other BFS direction (first link)
                if current_link in first_parents:
                    # if so, generate a path and add to the list of paths for graph generation
                    paths.append(
                        self.generate_path(first_parents, second_parents, current_link)
                    )
                else:
                    # if not, expand and add new links if we have not already seen them from this direction
                    result = self.es.search(
                        index="wikipedia_pages",
                        body={"query": {"match": {"title": current_link}}},
                    )
                    second_seen_links.add(current_link)
                    if len(result["hits"]["hits"]) > 0:
                        result_links = result["hits"]["hits"][0]["_source"]["links"]
                        links_to_expand = math.ceil(self.intensity * len(result_links))
                        links_inserted = 0
                        for link in result_links:
                            if link not in second_parents:
                                second_topic_links.append(link)
                                second_parents[link] = current_link
                                links_inserted += 1

                            if links_inserted == links_to_expand:
                                break

            current_iter += 1

        # If there were no paths for the terms, append as an error message
        if len(paths) == 0 and len(self.first_topic) > 0 and len(self.second_topic) > 0:
            self.error_messages.append(
                'No connection was found between "'
                + self.first_topic
                + '" and "'
                + self.second_topic
                + '."\n'
            )

        # Returning array of array of paths
        return paths, self.error_messages
