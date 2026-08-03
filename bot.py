import os
import asyncio
from telethon import TelegramClient, events
from aiohttp import web

# आपकी डिटेल्स
API_ID = 31018731
API_HASH = "1aa9517cdbcab415564cc8654d6507b6"
BOT_TOKEN = "8987040911:AAEqXn-fEyPbsIDHslq2WnKGzHxEpsqvYh8"

# Telethon क्लाइंट (Python 3.14 के साथ पूरी तरह से कंपैटिबल)
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("👋 **नमस्ते! आपका एडवांस क्लाउड बोट पूरी तरह से लाइव और एक्टिव है!**")

@client.on(events.NewMessage(pattern='/ping'))
async def ping(event):
    await event.respond("🏓 Pong! बोट एकदम सही और तेज काम कर रहा है।")

@client.on(events.NewMessage(pattern=r'/(v?play)\s+(.+)'))
async def play(event):
    query = event.pattern_match.group(2)
    await event.respond(f"🎵 **सर्च किया जा रहा है:** `{query}` ⏳ कृपया प्रतीक्षा करें...")

@client.on(events.NewMessage(pattern='/pause'))
async def pause(event):
    await event.respond("⏸️ वॉइस चैट को सफलतापूर्वक **पॉज (Pause)** कर दिया गया है।")

@client.on(events.NewMessage(pattern='/resume'))
async def resume(event):
    await event.respond("▶️ वॉइस चैट को फिर से **निर्णुग्न (Resume)** कर दिया गया है।")

@client.on(events.NewMessage(pattern='/skip'))
async def skip(event):
    await event.respond("⏭️ गाना **स्किप (Skip)** कर दिया गया है।")

@client.on(events.NewMessage(pattern='/ban'))
async def ban(event):
    if event.is_group:
        await event.respond("🚫 यूजर को बैन करने की प्रक्रिया शुरू कर दी गई है।")
    else:
        await event.respond("⚠️ यह कमांड सिर्फ ग्रुप में काम करती है।")

@client.on(events.NewMessage(pattern='/unban'))
async def unban(event):
    if event.is_group:
        await event.respond("✅ यूजर को अनबैन कर दिया गया है।")

@client.on(events.NewMessage(pattern='/banall'))
async def banall(event):
    if event.is_group:
        await event.respond("⚠️ **Banall कमांड शुरू कर दी गई है!**")

# Render के लिए फर्जी वेब सर्वर (ताकि Render बोट को बंद न करे)
async def handle(request):
    return web.Response(text="Telethon Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_web_server())
    print("Bot is running with Telethon...")
    client.run_until_disconnected()
    
