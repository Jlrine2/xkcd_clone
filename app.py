#!/usr/bin/python
from flask import Flask, render_template, Markup
import json
import requests
import scrape
import os
app = Flask(__name__)

images = {}
with open("data.json") as f:
    images = json.load(f)


def getComic(num):
    if num==404:
        return "<p>the 404th XKCD retruns a 404 error </p>"
    image = images[str(num)]
    
    if num < 10 or os.environ["MAX_VAL"]-num < 10:
        return Markup(F"""<h1>{image['title']}</h1> <img src="../static/archive/{num}.jpg"/> <p>"{image['alt']}</p>""")
    return Markup(F"""<img class="lazy" data-src="../static/archive/{num}.jpg" title="{image['alt']}" alt="{image['title']}" />""")


@app.route("/")
def all_images():
    max_val=os.environ["MAX_VAL"]
    r = requests.get(F"https://xkcd.com/{max_val + 1}")
    if r.status_code == 200:
        scrape.download(max_val + 1)
        os.environ["MAX_VAL"] = max_val + 1

    
    return render_template("newFirst.html", images=images, maxVal=max_val)


if __name__ == "__main__":
    app.add_template_global(getComic, name="getComic")
    app.run()