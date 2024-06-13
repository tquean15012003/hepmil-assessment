import time
import logging
import schedule
import requests

logging.basicConfig(level=logging.INFO, force=True)

logger = logging.getLogger(__name__)


def crawl_hourly():
    url = "http://localhost:8000/api/v1/report"
    logger.info("Crawl API called")
    response = requests.get(url)
    if response.status_code == 200:
        logger.info("Crawl successully")
    else:
        logger.error(f"API call failed with status code {response.status_code}")


if __name__ == "__main__":
    logger.info("Scheduler started")
    # Schedule the API call every hour
    schedule.every().hour.do(crawl_hourly)
    while True:
        schedule.run_pending()
        time.sleep(1)
