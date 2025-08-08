import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAKE_WEBHOOK = os.getenv("MAKE_WEBHOOK")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")

if not MAKE_WEBHOOK:
    raise ValueError("❌ MAKE_WEBHOOK не найден в .env")
