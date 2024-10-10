import asyncio
from typing import List

import aiohttp
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from apps.movies.models import Movie, Actor

base_url = "https://www.csfd.cz"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}


async def fetch_page(session, url, semaphore):
    try:
        async with semaphore:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None


async def fetch_all_pages(links):
    semaphore = asyncio.Semaphore(10)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for link in links:
            full_url = base_url + link
            tasks.append(fetch_page(session, full_url, semaphore))

        pages_content = await asyncio.gather(*tasks)
        return pages_content


class Command(BaseCommand):
    help = "Download the top 300 movies from csfd.cz"

    def download_links(self, links: List, url: str):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            container = soup.find('div', class_='box-content box-content-striped-articles')
            if not container:
                self.stdout.write(self.style.ERROR("Could not find the container div."))

            articles = container.find_all('article')

            for article in articles:
                a_tag = article.find('a', class_='film-title-name')
                if a_tag and 'href' in a_tag.attrs:
                    links.append(a_tag['href'])

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching page: {e}"))

    def handle(self, *args, **options):
        links_base_url = base_url + "/zebricky/filmy/nejlepsi/"
        links = []

        for page in range(0, 3):
            page_url = links_base_url + f"?from={page*100}" if page > 0 else links_base_url
            self.download_links(links=links, url=page_url)

        loop = asyncio.get_event_loop()
        pages_content = loop.run_until_complete(fetch_all_pages(links))

        for index, page in enumerate(pages_content):
            self.stdout.write(f"Processing movie {index+1}/300")
            soup = BeautifulSoup(page, 'html.parser')
            movie_name = soup.find('div', class_='film-header-name').find('h1').text.strip()
            movie = Movie(name=movie_name)
            movie.save()

            actors_div = soup.find_all('div')
            actors = []
            for div in actors_div:
                h4_tag = div.find('h4')
                if h4_tag and h4_tag.text.strip() == "Hrají:":
                    actor_links = div.find_all('a')
                    actors = [actor.text.strip() for actor in actor_links if actor.text.strip() != 'více']
                    break

            for actor_ in actors:
                actor, _ = Actor.objects.get_or_create(name=actor_)
                movie.actors.add(actor)
