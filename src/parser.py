import logging
import asyncio, aiohttp
from bs4 import BeautifulSoup
from src.database import Session
from src.models import Pages, Dependencies
from urllib.parse import urlparse


async def parse(url, current_depth=1, max_depth=4, from_page_id=None):
    """ Recursive function for saving links """

    if current_depth <= max_depth:
        links = await _get_links_from_url(url)
        logging.debug("deep: {}, links: {}, url: {}".format(current_depth, len(links), url))

        session = Session()
        if from_page_id is None:
            from_page = Pages(URL=url, request_depth=current_depth)
            session.add(from_page)
            session.flush()
            from_page_id = from_page.id
            session.commit()

        tasks = []
        for link in links:
            # save url to page table
            to_page = Pages(URL=link, request_depth=current_depth)
            session.add(to_page)
            session.flush()

            # save dependencies values
            session.add(Dependencies(from_page_id=from_page_id, link_id=to_page.id))
            session.flush()

            # generate new async tasks
            task = asyncio.create_task(
                parse(link, max_depth=max_depth, current_depth=current_depth + 1, from_page_id=to_page.id))
            tasks.append(task)

        session.commit()
        session.close()
        return await asyncio.gather(*tasks)


async def _get_links_from_url(main_url):
    """Return list of links from url"""
    links = []
    try:
        async with aiohttp.request('GET', url=main_url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, features="html.parser")

            parsed_uri = urlparse(main_url)
            domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            for link in soup.findAll('a'):
                url = str(link.get('href'))
                # search links only for wiki page
                if url.startswith("/wiki"):
                    links.append(domain + url)

    except Exception as ex:
        logging.error(str(ex))
    finally:
        return links
