from elasticsearch import Elasticsearch
from ConnectionInterface import ConnectionInterface
import time
import operator

MAX_ITER = 24

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

        return path

    # Bidirectional BFS logic here
    def find_all_connections(self, max_iter=MAX_ITER):
        start_time = time.time()
        paths = []
        # Storing all of the links for the first and second topics separately
        first_topic_links = self.first_links.copy()
        second_topic_links = self.second_links.copy()

        # Storing the parents for each link
        first_parents = {}
        first_seen_links = {self.first_topic}
        for link in self.first_links:
            first_parents[link] = self.first_topic
            first_seen_links.add(link)

        second_parents = {}
        second_seen_links = {self.second_topic}
        for link in self.second_links:
            second_parents[link] = self.second_topic
            second_seen_links.add(link)

        # Only iterating for 1000 iterations currently
        current_iter = 0
        query_time = 0.0
        queried_links = {}
        num_queries = 0

        # Only continuing while there are still links in both topics and the maximum number of iterations
        # has not been reached yet
        while (
            len(first_topic_links) != 0 or len(second_topic_links) != 0
        ) and current_iter < max_iter:
            current_link = ""

            # pop off queue
            if len(first_topic_links) != 0:
                current_link = first_topic_links.pop(0)

                # check if the node has been seen
                if current_link in second_seen_links:
                    # if so, generate path, clear other nodes expanded from it
                    paths.append(self.generate_path(first_parents, second_parents, current_link))
                else:
                    # if not, expand
                    if current_link in queried_links:
                        queried_links[current_link] += 1
                    else:
                        queried_links[current_link] = 1
                    num_queries += 1
                    start = time.time()
                    result = self.es.search(
                        index="wikipedia_pages",
                        body={"query": {"match": {"title": current_link}}},
                    )
                    query_time += time.time() - start
                    if len(result["hits"]["hits"]) > 0:
                        result_links = result["hits"]["hits"][0]["_source"]["links"]
                        for link in result_links:
                            if link not in first_seen_links:
                                first_topic_links.append(link)
                                first_seen_links.add(link)
                                first_parents[link] = current_link

            # pop off queue
            if len(second_topic_links) != 0:
                current_link = second_topic_links.pop(0)

                # check if the node has been seen
                if current_link in first_seen_links:
                    # if so, generate path, clear other nodes expanded from it
                    paths.append(self.generate_path(first_parents, second_parents, current_link))
                else:
                    # if not, expand
                    if current_link in queried_links:
                        queried_links[current_link] += 1
                    else:
                        queried_links[current_link] = 1
                    num_queries += 1
                    start = time.time()
                    result = self.es.search(
                        index="wikipedia_pages",
                        body={"query": {"match": {"title": current_link}}},
                    )
                    query_time += time.time() - start
                    if len(result["hits"]["hits"]) > 0:
                        result_links = result["hits"]["hits"][0]["_source"]["links"]
                        for link in result_links:
                            if link not in second_seen_links:
                                second_topic_links.append(link)
                                second_seen_links.add(link)
                                second_parents[link] = current_link

            current_iter += 1

        print('Query time: %s seconds' % query_time)
        print('Runtime: %s seconds' % (time.time() - start_time))
        sorted_queried_links = dict(sorted(queried_links.items(), key=operator.itemgetter(1), reverse=True))
        new = {}
        for k, n in sorted_queried_links.items():
            if n > 1:
                new[k] = n
        print(new)
        print('Number of total queries: ' + str(num_queries))
        print('Number of distinct queries: ' + str(len(queried_links)))
        # Returning array of array of paths
        return paths
