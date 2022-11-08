from http.client import REQUEST_TIMEOUT
from mediawiki import MediaWiki
from elasticsearch import Elasticsearch, exceptions
import time
import re
from bs4 import BeautifulSoup

es = Elasticsearch("http://localhost:9200")

#Attempt with wikipedia data dump
#Open simple wikipedia data dump
with open('simplewiki-latest-pages-articles-multistream.xml', encoding='utf-8') as file:
    title = ""
    links = []
    start_time = time.time()
    pages_parsed = 0
    print("starting execution")

    # Read line by line
    # pages_to_store = []
    pages_to_store = {}
    incoming_links = {}
    # num_pages = 0
    for line in file:
        # Check for title tag(i.e. new page)
        if "<title>" in line:
            pages_parsed += 1
            title = re.search("<title>(.*)</title>", line).group(1)
        # Check for links if currently parsing a page and not the void in between
        if "</page>" not in line and title != "" and ":" not in line:
            unparsed_links = re.split("]]", line)
            unparsed_links.pop()
            for link in unparsed_links:
                links.append(link.split("[[", 1)[-1].split("|")[0])
        # Check if end of page
        elif "</page>" in line:
            links = sorted(links, key=str.lower)
            for link in links:
                if link in incoming_links:
                    incoming_links[link] += 1
                else:
                    incoming_links[link] = 1
            
            if title not in incoming_links:
                incoming_links[title] = 0

            beg = {"index": {"_index": 'wikipedia_pages', "_id": title}}
            page = {"title": title, "links": links, "incoming_links": 0}
            pages_to_store[title] = []
            pages_to_store[title].append(beg)
            pages_to_store[title].append(page)
            title = ""
            links = []

        # Used to track program execution time
        end_time = time.time()
        if end_time - start_time > 10.0:
            print("\nPages read: " + str(pages_parsed) + "\n")
            start_time = time.time()
    
    print("***Initial parsing finished***")
    print()
    num_pages = 0
    no_pages = []
    finished_pages = []
    pages_parsed = 0
    for title, page in pages_to_store.items():
        pages_parsed += 1
        
        # Getting only relevant info
        # First element is just the newline separated junk Elastic makes us have
        es_page = page[1]

        # Incoming numbs stores the number of incoming links, while ordered links stores the links corresponding to these incoming links in an ordered fashion
        incoming_numbs = []
        ordered_links = []
        for link in es_page['links']:
            # Ensuring the link actually has a page on Simple Wikipedia
            if link in pages_to_store:
                current_inc = incoming_links[link]
                index = 0
                while index < len(incoming_numbs) and current_inc >= incoming_numbs[index]:
                    index += 1
                incoming_numbs.insert(index, current_inc)
                ordered_links.insert(index, link)
     
        # Adding newline header stuff first
        finished_pages.append(page[0])

        # Adding actual page next
        es_page['links'] = ordered_links
        es_page['incoming_links'] = incoming_links[title]
        finished_pages.append(es_page)

        num_pages += 1

    if num_pages == 100:
        es.bulk(index="wikipedia_pages", operations=pages_to_store, request_timeout = 120)
        num_pages = 0
        pages_to_store = []

    # Used to track program execution time
    end_time = time.time()
    if end_time - start_time > 10.0:
        print("\nPages read: " + str(pages_parsed) + "\n")
        start_time = time.time()


    # pages_to_store = []
    # num_pages = 0
    # no_pages = []
    # pages_parsed = 0
    # print('incoming links: ' + str(len(incoming_links)))
    # for page in incoming_links:
    #     try:
    #         if len(page) > 0:
    #             pages_parsed += 1
    #             search_result = es.get(index="wikipedia_pages", id=page)
    #             es_page = search_result['_source']
    #             incoming_numbs = []
    #             ordered_links = []
    #             for link in es_page['links']:
    #                 if link not in no_pages:
    #                     current_numb = incoming_links[link]
    #                     index = 0
    #                     while index < len(incoming_numbs) and current_numb >= incoming_numbs[index]:
    #                         index += 1
    #                     incoming_numbs.insert(index, current_numb)
    #                     ordered_links.insert(index, link)

    #             beg = {"index": {"_index": 'wikipedia_pages', "_id": title}}
    #             pages_to_store.append(beg)
    #             es_page['links'] = ordered_links
    #             es_page['incoming_links'] = incoming_links[page]
    #             pages_to_store.append(es_page)

    #             num_pages += 1
    #         if num_pages == 100:
    #             es.bulk(index="wikipedia_pages", operations=pages_to_store, request_timeout = 120)
    #             num_pages = 0
    #             pages_to_store = []

    #         # Used to track program execution time
    #         end_time = time.time()
    #         if end_time - start_time > 10.0:
    #             print("\nPages read: " + str(pages_parsed) + "\n")
    #             start_time = time.time()

    #     except exceptions.NotFoundError:
    #         no_pages.append(page)
