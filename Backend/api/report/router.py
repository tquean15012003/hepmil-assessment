import logging

from fastapi import APIRouter

from api.report.handler import ReportHandler


logger = logging.getLogger(__name__)


class ReportRouter:
    def __init__(self):
        logger.info("CrawlRouter initialized")
        self.router = APIRouter()
        self.router.add_api_route("", self.generate_report, methods=["GET"])
        self.handler = ReportHandler()

    async def generate_report(self):
        logger.info("generate_report called")
        result = await self.handler.generate_report()
        return result
