from elasticsearch import Elasticsearch
sample_topics = []

sample_topics.append({
    "title": "Cincinnati Reds",
    "full_text": "The Cincinnati Reds are a Major League Baseball from Cincinnati, Ohio, are the oldest team in professional baseball, established in 1869. The was knowns as the Cincinnati Red Stockings until 1878, when the team changed the name to the current Cincinnati Reds. The Reds joined the National League in 1876 The Reds have won World Series championships in 1919, 1940, 1975, 1976 and 1990. The strong Reds teams of the 1970s were nicknamed \"The Big Red Machine\". From 1912 to 1970, the Reds home stadium was Crosley Field, from 1970-2002 home games were played at Riverfront Stadium. Since 2003 the Reds have played home games at Great American Ballpark",
    "links": {
        "Major League Baseball": "https://simple.wikipedia.org/wiki/Major_League_Baseball",
        "Cincinnati": "https://simple.wikipedia.org/wiki/Cincinnati,_Ohio",
        "Ohio": "https://simple.wikipedia.org/wiki/Ohio",
        "World Series": "https://simple.wikipedia.org/wiki/World_Series"
    }
})

sample_topics.append({
    "title": "World Series",
    "full_text": "The World Series in Major League Baseball, is when the best team from the American League (the winner of the American League Championship Series) and the best team from the National League (the winner of the National League Championship Series) keep playing games of baseball until one of the two teams wins four games total. The winners of the most recent World Series in 2021 were the Atlanta Braves. They defeated the Houston Astros 4 games to 2. The New York Yankees have 27 World Series championships, the most of any team. The Cleveland Indians currently hold the longest active drought, having last won the Series before expansion teams were formed. Recently, the three longest championship droughts were ended by the Boston Red Sox, Chicago White Sox, and the Chicago Cubs.",
    "links": {
        "Major League Baseball": "https://simple.wikipedia.org/wiki/Major_League_Baseball"
    }
})

sample_topics.append({
    "title": "Ohio",
    "full_text": "Ohio is one of the 50 states in the United States. Its capital is Columbus. Columbus is also the largest city in Ohio. Other large cities in Ohio are Cleveland, Cincinnati, Dayton, Akron, Toledo, and Youngstown. Some famous people from Ohio include golfer Jack Nicklaus, Wilbur and Orville Wright, astronauts John Glenn and Neil Armstrong, authors Sherwood Anderson and Toni Morrison,[12] and actors Clark Gable and Katie Holmes. There have also been seven American presidents from Ohio: Ulysses S. Grant, Rutherford Hayes, James Garfield, Benjamin Harrison, William McKinley, William Howard Taft, Warren G. Harding. Ohio is important in elections because it is a swing state. Candidates often campaign a lot there and prior to 2020, the last time they voted for the losing candidate was 1960. Also, no Republican has ever won the presidency without carrying this state. Ohio has both farmland and cities, and there is a lot of discrimination against black people.[13] It is a part of the Midwest. Ohio is the 7th most populated state in the United States of America.",
    "links": {
        "Cincinnati": "https://simple.wikipedia.org/wiki/Cincinnati,_Ohio",
        "William Howard Taft": "https://simple.wikipedia.org/wiki/William_Howard_Taft"

    }
})
sample_topics.append({
    "title": "William Howard Taft",
    "full_text": "William Howard Taft (September 15, 1857 – March 8, 1930) was the 27th president of the United States. He was the only president who also served as a Supreme Court chief justice. He was 5 feet 11 inches (1.80 m) tall and weighed over 350 pounds (160 kg) at the end of his presidency.",
    "links": {}
})

sample_topics.append({
    "title": "Cincinnati",
    "full_text": "Cincinnati is a city in the southwestern corner of the state of Ohio near the states of Kentucky and Indiana. The city is in Hamilton County, Ohio. Cincinnati is home to major sports teams including the Cincinnati Reds and the Cincinnati Bengals, as well as events like the Cincinnati Masters and the Thanksgiving Day race. The University of Cincinnati traces its foundation to the Medical College of Ohio, which was founded in 1819.[6] Cincinnati was named after the Roman leader Lucius Quinctius Cincinnatus and was an early major city in the midwestern United States. Many Germans settled in the city and the Over-the-Rhine neighborhood gets its name from the river in Germany. Soap and machine tools are major industries in the area, which is home to the company Procter & Gamble as well as Macy's. Cincinnati's economy and population declined in the late 1900s, but the city is on the upswing. The Over-The-Rhine neighborhood has seen a lot of new businesses and development in recent years.",
    "links": {
        "Charles Manson": "https://simple.wikipedia.org/wiki/Charles_Manson",
        "William Howard Taft": "https://simple.wikipedia.org/wiki/William_Howard_Taft"
    }
})

# First, execute docker run --name es01-test --net elastic -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.17.6
# This starts elasticsearch instance on Docker

es = Elasticsearch("http://localhost:9200")
es.info().body

# Creating index for pages
mappings = {
    "properties": {
        "title": {"type": "text", "analyzer": "english"},
        "full_text": {"type": "text", "analyzer": "standard"},
        "links": {
            "type": "object",
            "properties": {
                "key": {"type": "text", "index": "false"},
                "value": {"type": "text", "index": "false"},
            }
        }
    }
}

es.indices.create(index="wikipedia_pages", mappings=mappings)
# first_doc = {
#     "title": first_topic,
#     "full_text": conn.first_text,
#     "links": conn.first_links
# }
# es.index(index="wikipedia_pages", document=first_doc)

for page in sample_topics:
    es.index(index="wikipedia_pages", document=page)

resp = es.search(
    index="wikipedia_pages",
    body={}
)
print(resp)

