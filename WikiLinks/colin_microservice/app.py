from flask import *
import wikipedia


app = Flask(__name__)

def wiki_summary(keyword):
    keyword = keyword.replace(" ", "_")
    try:
        summary = wikipedia.summary(keyword, auto_suggest=False, sentences=5)
        return summary
    except wikipedia.exceptions.PageError or wikipedia.exceptions.DisambiguationError:
        return -1

@app.route('/')
def greeting():
    return "Hello, welcome to Colin's summary scraper. Please search via the route /get_scraped/<keyword>"

@app.route('/get_scraped/<keyword>')
def get_summary(keyword):
    sum_scrape = wiki_summary(keyword)
    return jsonify(sum_scrape)

if __name__ == '__main__':
    app.run(host="localhost", port=6989, debug=True)