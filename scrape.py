import requests
import argparse
import re
import html.parser
import json


def download(num):
    webpage = requests.get(F"https://xkcd.com/{num}")

    if webpage.status_code != 200:
        print("error")

    # get image tag from webpage
    image_tag = re.findall("<img[^>]*/>", str(webpage.content))[1]
    image_data = parse_Data(image_tag)

    image = requests.get(image_data['url'])
    if image.status_code == 200:
        with open("static/archive/" + str(num) + ".jpg", "wb+") as f:
            for chunk in image:
                f.write(chunk)
        populate_JSON(image_data, num)



def parse_Data(imageTag):
    items = re.split('"', imageTag)
    image_url = "https:" + items[1]
    image_title = items[5]
    image_hover_text = html.unescape(items[3])
    data =  {
        "url": image_url,
        "title": image_title,
        "alt": image_hover_text
    }
    return data

def populate_JSON(image_data, num):
    with open("data.json") as f:
        data = json.load(f)
    data[str(num)] = image_data
    with open("data.json", "w") as f:
        json.dump(data, f)

        
