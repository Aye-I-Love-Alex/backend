import time
import re
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

# Open simple wikipedia data dump
with open('simplewiki-latest-pages-articles-multistream.xml', encoding='utf-8') as file:
    title = ""
    links = []
    pages = {}
    start_time = time.time()
    original_time = start_time
    pages_parsed = 0
    print("starting execution")

    # Read line by line
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
            page = {"title": title, "links": links}
            es.index(index="wikipedia_pages", document=page)
            pages[title] = links
            title = ""
            links = []

        # Used to track program execution time
        end_time = time.time()

        hour = 0

        if end_time - start_time > 10.0:
            start_time = time.time()

            # DateTime Object
            start_time_dt = datetime.fromtimestamp(start_time)
            # start_time_formated = start_time_dt.strftime('%H:%M:%S')

            # DateTime Object
            original_time_dt = datetime.fromtimestamp(original_time)
            # original_time_formated = original_time_dt.strftime('%H:%M:%S')

            # Time Delta Object
            elapsed_time = start_time_dt - original_time_dt

            '''
            if elapsed_time.minute == 59 and elapsed_time.second == 59:
                hour += 1
        
            formated_hour = str(hour) + ':' + str(elapsed_time_formated)
            
            
            '''

            # datetime.fromtimestamp(elapsed_time).strftime('%H:%M:%S')

            elapsed_time_formated = str(elapsed_time)

            print("\nPages read: " + str(pages_parsed))
            print("Elapsed Time: " + elapsed_time_formated + "\n")
