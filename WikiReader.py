from mediawiki import MediaWiki
import time
wikipedia = MediaWiki("https://simple.wikipedia.org/w/api.php")

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

#Open text file with list of all simple wikipedia pages
with open('Simple_Wikipedia_Pages.txt', encoding='utf-8') as pages:
    start = time.time()
    pages_read = 0
    for line in pages:
        #Calls wikipedia page currently
        page = wikipedia.page(line.replace("_", " "))
        title = page.title
        if "\"" not in title:
            file = open("links/" + title.replace(" ", '_') + ".txt", "w", encoding='utf-8')
        links = page.links
        #Currently writes all links to a text file named after wikipedia page
        #Replace with generating an elastic object instead
        if not file.closed: 
            for link in links:
                file.write(link + "\n")
        file.close()
        #Currently sleeps for .1 seconds, can likely speed up.
        end = time.time()
        pages_read += 1
        print("Elapsed time: " + str(end-start))
        print("Pages read: " + str(pages_read))
