import requests
import argparse
import re
import html.parser
import json


def download(num):
    try:
        webpage = requests.get(F"https://xkcd.com/{num}")

        if webpage.status_code != 200:
            print("error")

        # get image tag from webpage
        image_tag = re.findall("<img[^>]*/>", str(webpage.content))[1]
        populate_JSON(image_tag, num)

        image = requests.get(image_url)
        if image.status_code == 200:
            with open("archive/" + str(num) + ".jpg", "wb") as f:
                for chunk in image:
                    f.write(chunk)
    except:
        pass


def populate_JSON(imageTag, num):
    data = {}
    with open("data.json") as f:
        data = json.load(f)
    items = re.split('"', imageTag)
    image_url = "https:" + items[1]
    image_title = items[5]
    image_hover_text = html.unescape(items[3])
    data[num] = {
        "url": image_url,
        "title": image_title,
        "alt": image_hover_text
    }
    with open("data.json", "w") as f:
        json.dump(data, f)

        
