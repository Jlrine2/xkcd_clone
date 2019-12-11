#!/usr/bin/python
from flask import Flask, render_template, Markup
import json
import requests
import scrape
import os

app = Flask(__name__)

images = {}

def reloadJSON():
    global images
    with open("data.json") as f:
        images = json.load(f)


def getComic(num):
    if num==404:
        return "<p>the 404th XKCD retruns a 404 error </p>"
    image = images[str(num)]

    
    if num < 10 or int(os.environ['MAX_VAL'])-num < 10:
        return Markup(F"""<h1>{image['title']}</h1> <img src="../static/archive/{num}.jpg"/> <p>"{image['alt']}</p>""")
    return Markup(F"""<h1>{image['title']}</h1> <img class="lazy" data-src="../static/archive/{num}.jpg"/> <p>"{image['alt']}</p>""")
app.add_template_global(getComic, name="getComic")


@app.route("/")
def all_images():
    max_val=int(os.environ['MAX_VAL'])
    while True:
        r = requests.get(F"https://xkcd.com/{max_val + 1}")
        if r.status_code == 200:
            scrape.download(max_val + 1)
            max_val += 1
        else:
            os.environ['MAX_val'] = str(max_val)
            reloadJSON()
            break
    
    return render_template("newFirst.html", images=images, maxVal=max_val)


if __name__ == "__main__":
    reloadJSON()
    app.run()