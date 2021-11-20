from flask import *
import wikipedia
import requests
# from bs4 import BeautifulSoup


app = Flask(__name__)

def wiki_title(keyword):
    """
    Returns a Wikipedia URL based on user input
    """
    try:
        url = 'https://en.wikipedia.org/wiki/' + keyword
        page = requests.get(url)
        return page
    except wikipedia.exceptions.PageError or wikipedia.exceptions.DisambiguationError:
        return "Sorry, could not find page"
    # this is only if there is no matching Wikipedia url or spelling error

@app.route('/')
def home():
    """
    Opens home page for scraper
    """
    return "You have reached Victoria's Wikipedia URL and Title scraper. Please use the route /get_url/<keyword> when " \
           "making requests. Have a great day!"

@app.route('/get_url')
def oops():
    """
    Instructions for using the scraper
    """
    return "Please use the route /get_url/<keyword> when " \
           "making requests."

@app.route('/get_url/<keyword>')
def title_url(keyword):
    """
    Returns JSON data for teammate
    """
    scraped_info = wiki_title(keyword)
    return jsonify(scraped_info)

if __name__ == '__main__':
    app.run(host="localhost", port=1995, debug=True)