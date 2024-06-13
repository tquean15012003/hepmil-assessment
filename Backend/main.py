import logging

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from api.ping.router import PingRouter
from api.crawl.router import CrawlRouter
from api.report.router import ReportRouter


load_dotenv()

logging.basicConfig(level=logging.INFO, force=True)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROUTE_BASE = "api/v1"

app.include_router(PingRouter().router, prefix=f"/{ROUTE_BASE}/ping")
app.include_router(CrawlRouter().router, prefix=f"/{ROUTE_BASE}/crawl")
app.include_router(ReportRouter().router, prefix=f"/{ROUTE_BASE}/report")
