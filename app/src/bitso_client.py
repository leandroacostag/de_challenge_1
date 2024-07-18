import httpx
import backoff
import logging
import time

# Local imports
from config import bitso_api_url
from models import OrderBook

logger = logging.getLogger(__name__)


class BitsoApiClient:
    def __init__(self):
        self.api_url = bitso_api_url

    async def _request(self, endpoint: str, method: str, body: dict = None):
        url = f"{self.api_url}/{endpoint}"

        start_time = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                url,
                json=body,
            )

        elapsed_time = time.time() - start_time
        logger.debug(f"Request to {url} took {elapsed_time} seconds")

        return response.json()

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=5,
    )
    async def get_order_book(self, book: str = None) -> OrderBook:
        endpoint = "order_book/"

        if book:
            endpoint += f"?book={book}"

        response = await self._request(endpoint, "GET")

        if response["success"] is False:
            raise Exception(f"API Error: {response['error']['message']}")

        try:
            order_book = OrderBook(**response["payload"])
        except Exception as e:
            logger.error(f"Error parsing response: {e}")

        return order_book
