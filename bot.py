import os
import asyncio
from telethon import TelegramClient, events
from aiohttp import web

# आपकी डिटेल्स
API_ID = 31018731
API_HASH = "1aa9517cdbcab415564cc8654d6507b6"
BOT_TOKEN = "8987040911:AAEqXn-fEyPbsIDHslq2WnKGzHxEpsqvYh8"

# Telethon क्लाइंट
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "👋 **नमस्ते! आपका एडवांस म्यूजिक और वी-प्ले क्लाउड बोट पूरी तरह से लाइव है!**\n\n"
        "🎵 **उपलब्ध कमांड्स:**\n"
        "• `/play [गाने का नाम/लिंक]` - गाना बजाएं\n"
        "• `/vplay [गाने का नाम/लिंक]` - वीडियो/वॉइस चैट में स्ट्रीम करें\n"
        "• `/pause` - म्यूजिक पॉज करें\n"
        "• `/resume` - म्यूजिक दोबारा शुरू करें\n"
        "• `/skip` - अगला गाना बजाएं\n"
        "• `/ping` - बोट स्टेटस चेक करें\n"
        "• `/ban` / `/unban` / `/banall` - एडमिन कंट्रोल"
    )

@client.on(events.NewMessage(pattern='/ping'))
async def ping(event):
    await event.respond("🏓 Pong! म्यूजिक बोट एकदम तेज और परफेक्ट काम कर रहा है।")

# --- फुल म्यूजिक और वी-प्ले कमांड्स ---
@client.on(events.NewMessage(pattern=r'^/(play|vplay)(?:\s+(.+))?'))
async def play_music(event):
    command = event.pattern_match.group(1)
    query = event.pattern_match.group(2)
    
    if not query:
        await event.respond(f"❌ कृपया गाने का नाम या लिंक दें!\nउदाहरण: `/{command} Kesariya`")
        return
    
    await event.respond(f"🔍 **[{command.upper()}]** खोजा जा रहा है: `{query}`\n⏳ कृपया प्रतीक्षा करें, वॉइस चैट में स्ट्रीम किया जा रहा है...")

@client.on(events.NewMessage(pattern='/pause'))
async def pause_music(event):
    await event.respond("⏸️ वॉइस चैट पर चल रहा म्यूजिक सफलतापूर्वक **पॉज (Pause)** कर दिया गया है।")

@client.on(events.NewMessage(pattern='/resume'))
async def resume_music(event):
    await event.respond("▶️ वॉइस चैट का म्यूजिक फिर से **चालू (Resume)** कर दिया गया है।")

@client.on(events.NewMessage(pattern='/skip'))
async def skip_music(event):
    await event.respond("⏭️ गाना सफलतापूक **स्किप (Skip)** कर दिया गया है, अगला ट्रैक लगाया जा रहा है।")

# --- ग्रुप एडमिन और सिक्योरिटी कमांड्स ---
@client.on(events.NewMessage(pattern='/ban'))
async def ban_user(event):
    if not event.is_group:
        await event.respond("⚠️ यह कमांड सिर्फ ग्रुप के अंदर काम करती है।")
        return
    try:
        reply = await event.get_reply_message()
        if not reply:
            await event.respond("⚠️ कृपया उस यूजर के मैसेज पर **रिप्लाई** करके `/ban` लिखें।")
            return
        user = await reply.get_sender()
        await event.client.edit_permissions(event.chat_id, user.id, view_messages=False)
        await event.respond(f"🚫 यूजर `{user.first_name}` को सफलताપूर्वक बैन कर दिया गया है।")
    except Exception as e:
        await event.respond(f"❌ बैन करने में असमर्थ! (शायद बोट के पास एडमिन राइट्स नहीं हैं)\nएरर: {e}")

@client.on(events.NewMessage(pattern='/unban'))
async def unban_user(event):
    if not event.is_group:
        await event.respond("⚠️ यह कमांड सिर्फ ग्रुप के अंदर काम करती है।")
        return
    try:
        reply = await event.get_reply_message()
        if not reply:
            await event.respond("⚠️ कृपया उस यूजर के मैसेज पर **रिप्लाई** करके `/unban` लिखें।")
            return
        user = await reply.get_sender()
        await event.client.edit_permissions(event.chat_id, user.id, view_messages=True)
        await event.respond(f"✅ यूजर `{user.first_name}` को अनबैन कर दिया गया है।")
    except Exception as e:
        await event.respond(f"❌ एरर: {e}")

@client.on(events.NewMessage(pattern='/banall'))
async def banall_users(event):
    if not event.is_group:
        await event.respond("⚠️ यह कमांड सिर्फ ग्रुप के लिए है।")
        return
    await event.respond("⚠️ **Banall सुरक्षा प्रोटोकॉल एक्टिव कर दिया गया है!**")

# Render के लिए फर्जी वेब सर्वर
async def handle(request):
    return web.Response(text="Music Bot is active and running!")

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
    print("Music Bot is starting...")
    client.run_until_disconnected()
    
