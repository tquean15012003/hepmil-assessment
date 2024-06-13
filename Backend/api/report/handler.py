import os
import io
from pathlib import Path
import time
import logging

import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages

from api.crawl.handler import CrawlHanlder
from utils.SessionKey import get_session_key
from helpers.TelegramManager import TelegramManager

logger = logging.getLogger(__name__)

plt.switch_backend("Agg")


class ReportHandler:
    CHANNEL = "@hepmil_assessment"

    def __init__(self):
        logger.info("TelegramHandler initialized")
        self.crawl_handler = CrawlHanlder()
        self.telegram_manager = TelegramManager()

    async def generate_report(self):
        session_key = get_session_key()
        current_unix_time = int(time.time())
        storage_location = "./storage"
        report_location = os.path.join(storage_location, session_key)

        if os.path.isdir(report_location):
            return await self._send_existing_report(
                report_location, session_key, current_unix_time
            )
        else:
            return await self._create_and_send_new_report(
                report_location, session_key, current_unix_time
            )

    async def _send_existing_report(
        self, report_location, session_key, current_unix_time
    ):
        logger.info("Retrieving old report to send!")
        excel_report_location = f"{report_location}/report.xlsx"
        visualization_location = f"{report_location}/visualization.pdf"
        report_sent_name = f"report_{session_key}_{current_unix_time}.xlsx"
        visualization_sent_name = f"visualization_{session_key}_{current_unix_time}.pdf"

        df = pd.read_excel(excel_report_location)
        buffer = self._dataframe_to_bytesio(df)
        await self.telegram_manager.send_file(
            channel=self.CHANNEL, bytes=buffer, filename=report_sent_name
        )

        pdf_buffer = self._read_pdf_to_bytesio(visualization_location)
        await self.telegram_manager.send_file(
            channel=self.CHANNEL, bytes=pdf_buffer, filename=visualization_sent_name
        )

        return f"{report_sent_name} and {visualization_sent_name} generated"

    async def _create_and_send_new_report(
        self, report_location, session_key, current_unix_time
    ):
        logger.info("Create new report to send!")
        Path(report_location).mkdir(parents=True, exist_ok=True)
        posts = await self.crawl_handler.retrieve_top_posts()

        if not posts:
            raise Exception("There is no post to generate report!")
        excel_report_location = f"{report_location}/report.xlsx"
        visualization_location = f"{report_location}/visualization.pdf"
        report_sent_name = f"report_{session_key}_{current_unix_time}.xlsx"
        visualization_sent_name = f"visualization_{session_key}_{current_unix_time}.pdf"

        df = pd.DataFrame(posts)
        df.to_excel(excel_report_location, index=False)

        buffer = self._dataframe_to_bytesio(df)
        await self.telegram_manager.send_file(
            channel=self.CHANNEL, bytes=buffer, filename=report_sent_name
        )
        with PdfPages(f"{report_location}/visualization.pdf") as pdf:
            # 1. Distribution of Upvotes
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df["upvotes"], bins=30, color="skyblue", edgecolor="black")
            ax.set_title("Distribution of Upvotes")
            ax.set_xlabel("Upvotes")
            ax.set_ylabel("Frequency")
            ax.grid(True)
            pdf.savefig(fig)
            plt.close(fig)

            # 2. Number of Comments vs Upvotes
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(df["upvotes"], df["no_comments"], alpha=0.5)
            ax.set_title("Number of Comments vs Upvotes")
            ax.set_xlabel("Upvotes")
            ax.set_ylabel("Number of Comments")
            ax.grid(True)
            pdf.savefig(fig)
            plt.close(fig)

        pdf_buffer = self._read_pdf_to_bytesio(visualization_location)
        await self.telegram_manager.send_file(
            channel=self.CHANNEL, bytes=pdf_buffer, filename=visualization_sent_name
        )
        return f"{report_sent_name} and {visualization_sent_name} generated"

    def _dataframe_to_bytesio(self, df):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        buffer.seek(0)
        return buffer

    def _read_pdf_to_bytesio(self, filepath: str):
        with open(filepath, "rb") as f:
            pdf_buffer = io.BytesIO(f.read())
        return pdf_buffer
