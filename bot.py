import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from news import format_articles, get_tech_news, get_top_news

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "👋 <b>Benvenuto nel News Bot!</b>\n\n"
        "Ecco i comandi disponibili:\n\n"
        "📰 /notizie — Le 5 notizie più importanti del giorno in Italia\n"
        "💻 /tech — Le 5 notizie tech/informatica del giorno\n\n"
        "Buona lettura!"
    )
    await update.message.reply_text(text, parse_mode="HTML")


async def notizie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("⏳ Recupero le notizie in corso...")
    try:
        articles = get_top_news(NEWS_API_KEY)
        text = format_articles(articles, "📰 *Notizie del giorno*")
        await update.message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        logger.error("Errore nel recupero notizie: %s", e, exc_info=True)
        await update.message.reply_text(f"❌ Errore: {e}")


async def tech(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("⏳ Recupero le notizie tech in corso...")
    try:
        articles = get_tech_news(NEWS_API_KEY)
        text = format_articles(articles, "💻 *Notizie Tech*")
        await update.message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        logger.error("Errore nel recupero notizie tech: %s", e, exc_info=True)
        await update.message.reply_text(f"❌ Errore: {e}")


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN non impostato nel file .env")
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY non impostato nel file .env")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("notizie", notizie))
    app.add_handler(CommandHandler("tech", tech))

    logger.info("Bot avviato. In ascolto...")
    app.run_polling()


if __name__ == "__main__":
    main()
