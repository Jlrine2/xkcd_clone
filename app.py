#!/usr/bin/python
from flask import Flask, render_template, Markup
import json
import requests
import scrape
import os


app = Flask(__name__)


def getComic(num):
    if num==404:
        return "<p>the 404th XKCD retruns a 404 error </p>"
    image = json.load(open(f'static/archive/{num}.json'))

    
    if num < 10 or int(os.environ['MAX_VAL'])-num < 10:
        return Markup(F"""<h1>{image['title']}</h1> <img src="../static/archive/{num}.jpg"/> <p>"{image['alt']}</p>""")
    return Markup(F"""<h1>{image['title']}</h1> <img class="lazy" data-src="../static/archive/{num}.jpg"/> <p>"{image['alt']}</p>""")
app.add_template_global(getComic, name="getComic")


@app.route("/")
def all_images():
    max_val = len([name for name in os.listdir('/app/static/archive') if name.endswith('jpg')])
    while True:
        next_comic = max_val + 1
        if next_comic == 404:
            max_val +=1
            continue
        r = requests.get(F"https://xkcd.com/{next_comic}")
        if r.status_code == 200:
            scrape.download(max_val + 1)
            max_val += 1
        else:
            break
    
    return render_template("newFirst.html", maxVal=max_val)


if __name__ == "__main__":
    app.run()
