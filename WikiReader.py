from http.client import REQUEST_TIMEOUT
from mediawiki import MediaWiki
from elasticsearch import Elasticsearch
import time
import re
from bs4 import BeautifulSoup

es = Elasticsearch("http://localhost:9200")

#Attempt with wikipedia data dump
#Open simple wikipedia data dump
with open('simplewiki-latest-pages-articles-multistream.xml', encoding='utf-8') as file:
    title = ""
    links = []
    # pages = {}
    start_time = time.time()
    pages_parsed = 0
    print("starting execution")

    # Read line by line
    pages_to_store = []
    incoming_links = {}
    num_pages = 0
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

            beg = {"index": {"_index": 'wikipedia_pages', "_id": title}}
            page = {"title": title, "links": links, "incoming_links": 0}
            pages_to_store.append(beg)
            pages_to_store.append(page)
            # es.index(index="wikipedia_pages", document=page)
            num_pages += 1
            # pages[title] = links
            title = ""
            links = []
        
        if num_pages == 100:
            es.bulk(index="wikipedia_pages", operations=pages_to_store, request_timeout=60)
            num_pages = 0
            pages_to_store = []

        # Used to track program execution time
        end_time = time.time()
        if end_time - start_time > 10.0:
            print("\nPages read: " + str(pages_parsed) + "\n")
            start_time = time.time()
    
    pages_to_store = []
    num_pages = 0
    for page in incoming_links:
        search_result = es.get(index="wikipedia_pages", id=page)
        if search_result['found']:
            es_page = search_result['_source']
            incoming_numbs = []
            ordered_links = []
            for link in es_page['links']:
                current_numb = incoming_links[link]
                index = 0
                while index < len(incoming_numbs) and incoming_numbs >= incoming_numbs[index]:
                    index += 1
                incoming_numbs.insert(index, current_numb)
                ordered_links.insert(index, link['title'])

            beg = {"index": {"_index": 'wikipedia_pages', "_id": title}}
            pages_to_store.append(beg)
            es_page['links'] = ordered_links
            es_page['incoming_links'] = incoming_links[page]
            pages_to_store.append(es_page)

            num_pages += 1
            if num_pages == 100:
                es.bulk(index="wikipedia_pages", operations=pages_to_store, request_timeout=60)
