from flask import *
import wikipedia
from bs4 import BeautifulSoup
import requests
import re


app = Flask(__name__)

def wiki_summary(keyword):
    try:
        summary = wikipedia.summary(keyword, auto_suggest=False, sentences=5)
        return summary
    except wikipedia.exceptions.PageError or wikipedia.exceptions.DisambiguationError:
        return -1


def wiki_title(keyword):
    try:
        url = 'https://en.wikipedia.org/wiki/' + keyword
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        words =  soup.findAll("h1")
        title = words[0].text
        return title, url
    except wikipedia.exceptions.PageError or wikipedia.exceptions.DisambiguationError:
        return -1



def img_scraper(keyword):
    keyword = keyword.replace(" ", "_")
    url = 'https://en.wikipedia.org/wiki/' + keyword
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for image in soup.findAll("img"):
        src = image.get('src')
        if re.search('wikipedia/.*/thumb/', src) and not re.search('.svg', src):
            return src
    return -1


def get_template_parameters(keyword):
    wiki_summary = wikipedia.summary(keyword)
    article_title, url = wiki_title(keyword)
    wiki_image = img_scraper(article_title)
    # video_id = video_id_lookup(article_title)
    # payload = {"videoid": video_id}
    # response = requests.get("http://flip1.engr.oregonstate.edu:65334/embedlink", params=payload)
    # embed_video_link = response.text
    SE_keyword = article_title.replace(" ", "+")
    SE_url = "https://www.seriouseats.com/search?q=" + SE_keyword
    return wiki_summary, article_title, url, wiki_image, SE_url
# also include video parameters to pass to


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
            search_info = request.form["search_input"]
            summary, title, wiki_url, image, SE_url = get_template_parameters(search_info)
            return render_template("search.html", title=title, content=summary,
                wiki=wiki_url, picture=image, SE=SE_url)
    else:
        return render_template("index.html")


@app.route("/instructions")
def instructions():
    return render_template("instructions.html")



if __name__ == "__main__":
    app.run(debug=True)


