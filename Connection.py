import wikipediaapi
from ConnectionInterface import ConnectionInterface

class Connection(ConnectionInterface):

    wikipedia = wikipediaapi.Wikipedia('en')
    first_links = {}
    second_links = {}
    def __init__(self, first_topic, second_topic):
        first_page = self.wikipedia.page(first_topic)
        for key, item in first_page.links.items():
            self.first_links[key] = item.fullurl
        
        second_page = self.wikipedia.page(second_topic)
        for key, item in second_page.links.items():
            self.second_links[key] = item.fullurl
        
    #BFS logic will go here
    def find_connection(self):
        # first_links = set(first_page.links.keys())
        # second_links = set(second_page.links.keys())
        # common_links = first_links.intersection(second_links)

        # if second_topic in first_links:
        #     common_links.add(second_topic)

        # if first_topic in second_links:
        #     common_links.add(first_topic)
        return ""