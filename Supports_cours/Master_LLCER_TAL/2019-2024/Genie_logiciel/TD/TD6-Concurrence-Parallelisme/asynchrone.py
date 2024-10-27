import asyncio
import time
import aiohttp


async def download_site(session, url):
    async with session.get(url) as response:
        print("Read {0} from {1}".format(response.content_length, url))


async def download_all_sites(sites):
    # contrairement à Threading, on peut partager la Session avec les différentes tâches
    # on la crée donc via un context manager (with)
    async with aiohttp.ClientSession() as session:

        tasks = []
        # asyncio.ensure_future crée une liste de tâche à réaliser, et s'assure de les déclencher 
        for url in sites:
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        # asyncio.gather attend que toutes les tâches soient terminées, avant de ferme la Session
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    # déclenche la boucle d'événements, qui tournera jusqu'à ce que la tâche soit accomplie
    asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")