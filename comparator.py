from Connection import Connection

first_topic = input("First topic: ")
second_topic = input("Second topic: ")

conn = Connection(first_topic, second_topic)

print(conn.first_links)
print(conn.second_links)

# print(test.hyperlinks())

# print(current_page.exists())

# print(common_links)