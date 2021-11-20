from flask import *
import wikipedia
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)


def wiki_summary(keyword):
    """
    Makes an HTTP Request to Colin's microservice in order to return a summary scraped from Wikipedia
    """
    keyword = keyword.replace(" ", "_")
    try:
        response = requests.get('http://localhost:6989/get_scraped/' + keyword)
        # sending a response to colin's microservice (running on localhost) using keyword as parameter
        return jsonify(response)
    except wikipedia.exceptions.PageError or wikipedia.exceptions.DisambiguationError:
        # if the wikipedia article does not exist or parameter is possible spelled wrong
        return -1


def wiki_title(keyword):
    """
    Makes an HTTP request via Wikipedia api to display the title and url of an article based on user's keyword
    """
    try:
        url = 'https://en.wikipedia.org/wiki/' + keyword
        # looking for matching wikipedia article using keyword
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # extracting html data
        words = soup.findAll("h1")
        # h1 = title of article
        title = words[0].text
        return title, url
    # presents a clickable link with the title of the article displayed
    except wikipedia.exceptions.PageError or wikipedia.exceptions.DisambiguationError:
        return -1


def get_template_parameters(keyword):
    """
    Assigns variable names for rendering page
    """
    wiki_summary = wikipedia.summary(keyword)
    article_title, url = wiki_title(keyword)
    return wiki_summary, article_title, url


@app.route("/")
def home():
    """
    First page that opens when you run webapp
    """
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    This is the route that handles all search queries
    """
    if request.method == "POST":
        search_info = request.form["search_input"]
        # grabs user input and displays matching information
        summary, title, wiki_url = get_template_parameters(search_info)
        return render_template("search.html", title=title, content=summary,
                               wiki=wiki_url)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
