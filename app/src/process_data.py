import pandas as pd
import time
from datetime import datetime
import os
import logging

# Local imports
from src.bitso_client import BitsoApiClient
from config import data_path

logger = logging.getLogger(__name__)


async def process_book(book_name: str):
    logger.info(f"{book_name}: Starting new chunk of data processing")
    start_dt = datetime.now()
    bitso_client = BitsoApiClient()

    # (orderbook_timestamp: string, book: string, bid :float, ask: float, spread: float)
    output = []

    for i in range(5):  # Loop to run 600 times (10 minutes with 1-second intervals)
        request_start_time = time.time()  # Record the start time

        # Get the order book
        order_book = await bitso_client.get_order_book(book_name)

        # Extract best bid and best ask
        best_bid = float(order_book.bids[0].price)
        best_ask = float(order_book.asks[0].price)

        # Calculate the spread (show upto 3 decimal places)
        spread = (best_ask - best_bid) * 100 / best_ask
        spread = round(spread, 3)

        # Append the data to the output dataframe
        output.append(
            {
                "orderbook_timestamp": order_book.updated_at,
                "book": book_name,
                "bid": best_bid,
                "ask": best_ask,
                "spread": spread,
            }
        )

        # Calculate elapsed time for the iteration
        request_elapsed_time = time.time() - request_start_time

        if request_elapsed_time > 1:
            logger.warning(
                f"{book_name}: Processing took {round(request_elapsed_time, 2)} seconds."
            )

        # Sleep for the remaining time to ensure 1-second intervals
        time.sleep(max(0, 1 - request_elapsed_time))
        logger.debug(f"{book_name}: Iteration {i+1} completed")

    output_df = pd.DataFrame(output)

    # Get the date components for the output directory
    year = start_dt.year
    month = start_dt.month
    day = start_dt.day
    hour = start_dt.hour
    minute = start_dt.minute

    # Create the directory structure
    output_dir = os.path.join(
        data_path,
        f"book={book_name}",
        f"year={year}",
        f"month={month:02d}",
        f"day={day:02d}",
        f"hour={hour:02d}",
        f"minute={minute:02d}",
    )
    os.makedirs(output_dir, exist_ok=True)

    # Save the output to a csv file
    output_path = os.path.join(output_dir, "order_book.csv")
    output_df.to_csv(output_path, index=False)

    logger.info(f"--> {book_name}: Data saved to {output_path}")
