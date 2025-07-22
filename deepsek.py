import logging
import html
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from google import generativeai as genai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Bot setup
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Logger
logging.basicConfig(level=logging.INFO)

@dp.message(F.text)
async def gemini_chat(message: Message):
    try:
        # Ask Gemini
        response = model.generate_content(message.text)
        safe_text = html.escape(response.text)
        await message.answer(safe_text)
    except Exception as e:
        await message.answer(f"⚠️ Error:\n<code>{html.escape(str(e))}</code>")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
