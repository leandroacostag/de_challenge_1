import asyncio
import logging
import sys

# Local imports
from src.process_data import process_book
from config import logs_level

# Logging
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logs_level,
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

books_to_process = ["btc_mxn", "usd_mxn"]


async def run_book_task(book):
    while True:
        try:
            await process_book(book)
        except Exception as e:
            logger.error(f"Error processing book {book}: {e}")
        await asyncio.sleep(1)  # Optional: delay before restarting task


async def run_tasks():
    logger.info(
        f"Starting the data processing tasks for books: {','.join(books_to_process)}"
    )
    tasks = [asyncio.create_task(run_book_task(book)) for book in books_to_process]
    await asyncio.gather(*tasks)


def main():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(run_tasks())
    else:
        loop.run_until_complete(run_tasks())


# Ensure the script can be run as a standalone program
if __name__ == "__main__":
    main()
