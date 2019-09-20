import logging
import asyncio
from src.parser import parse


def run():
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(parse(url="https://ru.wikipedia.org", max_depth=2))


if __name__ == "__main__":
    run()
