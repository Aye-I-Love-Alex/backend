import wikipediaapi
from flask import Flask, render_template, request

wikipedia = wikipediaapi.Wikipedia('en')
app = Flask(__name__)


def connection(first_topic, second_topic):
    first_page = wikipedia.page(first_topic)
    second_page = wikipedia.page(second_topic)

    first_links = set(first_page.links.keys())
    second_links = set(second_page.links.keys())
    common_links = first_links.intersection(second_links)

    if second_topic in first_links:
        common_links.add(second_topic)

    if first_topic in second_links:
        common_links.add(first_topic)

    return common_links


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        first = request.form.get('firstword')
        second = request.form.get('secondword')
        response = ''
        if len(first) > 0 and len(second) > 0:
            response = connection(first, second)
        return render_template('index.html', connection=response)
    else:
        return render_template('index.html', connection='')


if __name__ == "__main__":
    app.run(debug=True)





