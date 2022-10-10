from mediawiki import MediaWiki
import time
import re
wikipedia = MediaWiki("https://simple.wikipedia.org/w/api.php")
from bs4 import BeautifulSoup

# test_topics = [
#     "Cincinnati Reds",
#     "World Series",
#     "Ohio",
#     "William Howard Taft",
#     "Cincinnati",
#     "Charles Manson",
#     "Barack Obama",
#     "Joe Biden",
# ]

# #Open text file with list of all simple wikipedia pages
# with open('Simple_Wikipedia_Pages.txt', encoding='utf-8') as pages:
#     start = time.time()
#     pages_read = 0
#     for line in pages:
#         #Calls wikipedia page currently
#         page = wikipedia.page(line.replace("_", " "))
#         title = page.title
#         if "\"" not in title:
#             file = open("links/" + title.replace(" ", '_') + ".txt", "w", encoding='utf-8')
#         links = page.links
#         #Currently writes all links to a text file named after wikipedia page
#         #Replace with generating an elastic object instead
#         if not file.closed: 
#             for link in links:
#                 file.write(link + "\n")
#         file.close()
#         #Currently sleeps for .1 seconds, can likely speed up.
#         end = time.time()
#         pages_read += 1
#         print("Elapsed time: " + str(end-start))
#         print("Pages read: " + str(pages_read))

#Attempt with wikipedia data dump

#Open simple wikipedia data dump
with open('simplewiki-20221001-pages-articles-multistream.xml', encoding='utf-8') as file:
    title = ""
    links = []
    pages = {}
    # start_time = time.time()
    # pages_parsed = 0
    # print("starting execution")
    
    # Read line by line
    for line in file:
        # Check for title tag(i.e. new page)
        if "<title>" in line:
            pages_parsed += 1
            title = re.search('<title>(.*)</title>', line).group(1)
        # Check for links if currently parsing a page and not the void in between
        if "</page>" not in line and title != "" and ":" not in line:
            unparsed_links = re.split("]]", line)
            unparsed_links.pop()
            for link in unparsed_links:
                links.append(link.split('[[',1)[-1].split("|")[0])
        # Check if end of page
        elif "</page>" in line:
            links = sorted(links, key=str.lower)
            pages[title] = links
            title = ""
            links = []
        # Used to track program execution time
        # end_time = time.time()
        # if end_time - start_time > 10.0:
        #     print("\nPages read: " + str(pages_parsed) + "\n")
        #     start_time = time.time()