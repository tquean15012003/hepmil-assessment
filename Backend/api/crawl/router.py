import logging

from fastapi import APIRouter

from api.crawl.handler import CrawlHanlder


logger = logging.getLogger(__name__)


class CrawlRouter:
    def __init__(self):
        logger.info("CrawlRouter initialized")
        self.router = APIRouter()
        self.router.add_api_route(
            "/{no_post}/{time_filter}", self.call_get_top_post, methods=["GET"]
        )
        self.handler = CrawlHanlder()

    async def call_get_top_post(self, no_post: str, time_filter: str):
        logger.info(
            f"call_get_top_post called with arguments: no_post: {no_post}, time_filter: {time_filter}"
        )
        result = await self.handler.retrieve_top_posts(
            no_post=int(no_post), time_filter=time_filter
        )

        return result
