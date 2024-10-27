import time
from random import randint
import requests as requests
from flask import Flask


app = Flask(__name__)


def get_xkcd_image():
    # choisi un identifiant au hasard et collecte une image sur une API
    random = randint(0, 300)
    response = requests.get(f'http://xkcd.com/{random}/info.0.json')
    return response.json()['img']


@app.get('/comic')
def hello():
    # on démarre le compteur, pour voir le temps que prend le process
    start = time.perf_counter()

    url = get_xkcd_image()
    end = time.perf_counter()
    return f"""
        Time taken: {end-start}<br><br>
        <img src="{url}"></img>
    """

def get_multiple_images(number):
    return [get_xkcd_image() for _ in range(number)]


@app.get('/comic2')
def hello2():
    start = time.perf_counter()
    # ici on télécharge 5 images, ce qui va prendre beaucoup plus de temps
    urls = get_multiple_images(5)
    end = time.perf_counter()

    markup = f"Time taken: {end-start}<br><br>"
    for url in urls:
        markup += f'<img src="{url}"></img><br><br>'

    return markup


if __name__ == '__main__':
    app.run(debug=True)