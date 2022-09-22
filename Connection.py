import wikipediaapi
from ConnectionInterface import ConnectionInterface

class Connection(ConnectionInterface):

    wikipedia = wikipediaapi.Wikipedia('en')
    
    first_text = ''
    first_links = {}
    
    second_links = {}
    second_text = ''
    def __init__(self, first_topic, second_topic):
        first_page = self.wikipedia.page(first_topic)
        self.first_text = first_page.text
        
        second_page = self.wikipedia.page(second_topic)
        self.second_text = second_page.text

        first_page_links = first_page.links
        second_page_links = second_page.links
        for key, item in first_page_links.items():
            if self.wikipedia.page(key).exists():
                #print(first_page_links[key].fullurl)
                try:
                    first_page_links[key].fullurl
                except:
                    continue
                else:
                    self.first_links[key] = first_page_links[key].fullurl
        print("Success for first")
        
        # for key, item in second_page_links.items():
        #     if self.wikipedia.page(key).exists():
        #         try:
        #             second_page_links[key].fullurl
        #         except:
        #             continue
        #         else:
        #             if "Category:" not in key and "Help:" not in key and "Template talk:" not in key and "Wikipedia:" not in key and "Template:" not in key:
        #                 self.second_links[key] = second_page_links[key].fullurl
        print("Success for second")
        
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