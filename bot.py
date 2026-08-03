import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# लॉगिंग सेट अप
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# आपका बोट टोकन
BOT_TOKEN = "8987040911:AAEqXn-fEyPbsIDHslq2WnKGzHxEpsqvYh8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 नमस्ते! बोट बिल्कुल सही तरीके से लाइव और चालू है।")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong! सब ठीक ठाक है।")

if __name__ == '__main__':
    # नया और 100% सेफ तरीका जो कभी एरर नहीं देगा
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ping', ping))
    
    print("Bot is starting...")
    application.run_polling()
    
