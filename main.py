import os
from pyrogram import Client, filters
from pyrogram.types import Message
from aiohttp import web

# आपकी डिटेल्स
API_ID = 31018731
API_HASH = "1aa9517cdbcab415564cc8654d6507b6"
BOT_TOKEN = "8987040911:AAEqXn-fEyPbsIDHslq2WnKGzHxEpsqvYh8"

# बोट क्लाइंट
app = Client(
    "AdvanceBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply_text("👋 नमस्ते! आपका एडवांस बोट सफलतापूर्वक लाइव और चालू है।")

@app.on_message(filters.command("ping"))
async def ping_handler(client, message: Message):
    await message.reply_text("🏓 Pong! बोट बिल्कुल सही काम कर रहा है।")

# Render के लिए फर्जी वेब सर्वर (ताकि बोट बंद न हो)
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    server_app = web.Application()
    server_app.router.add_get("/", handle)
    runner = web.AppRunner(server_app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

if __name__ == "__main__":
    import asyncio
    print("Starting bot and dummy server...")
    loop = asyncio.get_event_loop()
    loop.create_task(start_web_server())
    app.run()
    
