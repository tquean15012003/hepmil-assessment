import os
import logging
import asyncio

from io import BytesIO
from telegram import Bot
from dotenv import load_dotenv


class TelegramManager:

    def __init__(
        self,
    ):
        self.bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

    async def send_message(self, channel: str, message: str):
        await self.bot.send_message(chat_id=channel, text=message)

    async def send_file(self, bytes: BytesIO, channel: str, filename=str):
        await self.bot.send_document(chat_id=channel, document=bytes, filename=filename)


async def main():
    # Initialize the bot
    telegram_manager = TelegramManager()
    await telegram_manager.send_message("@hepmil_assessment", "Hello. I am a bot")


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO, force=True)
    asyncio.run(main())
