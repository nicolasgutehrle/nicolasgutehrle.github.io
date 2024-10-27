import asyncio
import time
from random import randint
import httpx
from flask import Flask


app = Flask(__name__)

# version asynchrone de la fonction
async def get_xkcd_image(session):
    random = randint(0, 300)
    # ici on redonne le contrôle à la boucle d'événement le temps que l'API donne une réponse
    result = await session.get(f'http://xkcd.com/{random}/info.0.json') # dont wait for the response of API
    return result.json()['img']

# function converted to coroutine
async def get_multiple_images(number):
    # on ouvre la Session, qui cette fois est asynchrone
    async with httpx.AsyncClient() as session: 
        # on crée les tâches 
        tasks = [get_xkcd_image(session) for _ in range(number)]
        # on attend que les tâches soient réalisées
        result = await asyncio.gather(*tasks, return_exceptions=True)
    return result


@app.get('/comic')
async def hello():
    start = time.perf_counter()
    urls = await get_multiple_images(5)
    end = time.perf_counter()
    markup = f"Time taken: {end-start}<br><br>"
    for url in urls:
        markup += f'<img src="{url}"></img><br><br>'

    return markup


if __name__ == '__main__':
    app.run(debug=True)