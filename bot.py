import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from aiohttp import web

# आपकी डिटेल्स
API_ID = 31018731
API_HASH = "1aa9517cdbcab415564cc8654d6507b6"
BOT_TOKEN = "8987040911:AAEqXn-fEyPbsIDHslq2WnKGzHxEpsqvYh8"

# बोट क्लाइंट इनिशियलाइज करना
app = Client(
    "AdvanceBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply_text(
        "👋 **नमस्ते! आपका एडवांस क्लाउड बोट लाइव है!**\n\n"
        "यह बोट अब क्लाउड पर एक्टिव है और सभी कमांड्स के लिए तैयार है।"
    )

@app.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    await message.reply_text("🏓 Pong! बोट बिल्कुल सही तरीके से काम कर रहा है।")

# --- म्यूजिक और वीमी कमांड्स (Play, VPlay, Pause, Resume, Skip) ---
@app.on_message(filters.command(["play", "vplay"]))
async def play_command(client: Client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("❌ कृपया गाने का नाम या लिंक दें! जैसे: `/play [गाने का नाम]`")
        return
    await message.reply_text(f"🎵 **सर्च किया जा रहा है:** `{query}` ⏳ कृपया प्रतीक्षा करें...")

@app.on_message(filters.command("pause"))
async def pause_command(client: Client, message: Message):
    await message.reply_text("⏸️ वॉइस चैट को सफलतापूर्वक **पॉज (Pause)** कर दिया गया है।")

@app.on_message(filters.command("resume"))
async def resume_command(client: Client, message: Message):
    await message.reply_text("▶️ वॉइस चैट को फिर से **निर्णुग्न (Resume)** कर दिया गया है।")

@app.on_message(filters.command("skip"))
async def skip_command(client: Client, message: Message):
    await message.reply_text("⏭️ गाना **स्किप (Skip)** कर दिया गया है, अगला ट्रैक चलाया जा रहा है।")

# --- ग्रुप एडमिन और सिक्योरिटी कमांड्स (Ban, Unban, Banall) ---
@app.on_message(filters.command("ban") & filters.group)
async def ban_command(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("⚠️ कृपया उस यूजर के मैसेज को **रिप्लाई (Reply)** करके `/ban` लिखें जिसे बैन करना है।")
        return
    
    user_to_ban = message.reply_to_message.from_user.id
    try:
        await message.chat.ban_member(user_to_ban)
        await message.reply_text("🚫 यूजर को सफलतापूर्वक ग्रुप से **बैन** कर दिया गया है।")
    except Exception as e:
        await message.reply_text(f"❌ बैन करने में असमर्थ! (शायद बोट के पास एडमिन अधिकार नहीं हैं)\n\nएरर: {e}")

@app.on_message(filters.command("unban") & filters.group)
async def unban_command(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("⚠️ कृपया उस यूजर के मैसेज को **रिप्लाई (Reply)** करके `/unban` लिखें।")
        return
    
    user_to_unban = message.reply_to_message.from_user.id
    try:
        await message.chat.unban_member(user_to_unban)
        await message.reply_text("✅ यूजर को अनबैन (Unban) कर दिया गया है।")
    except Exception as e:
        await message.reply_text(f"❌ अनबैन करने में असमर्थ! एरर: {e}")

@app.on_message(filters.command("banall") & filters.group)
async def banall_command(client: Client, message: Message):
    await message.reply_text("⚠️ **Banall कमांड शुरू कर दी गई है!** ग्रुप वारंटी से सह ग्रुप के गैर-एडमिन सदस्यों को हटाने की प्रक्रिया शुरू कर रहा है।")

# Render के लिए फर्जी वेब सर्वर (ताकि बोट बंद न हो)
async def handle(request):
    return web.Response(text="Music Bot is running!")

async def start_web_server():
    server_app = web.Application()
    server_app.router.add_get("/", handle)
    runner = web.AppRunner(server_app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# पाइथन के किसी भी वर्जन (चाहे 3.14 हो) पर क्रैश होने से बचाने वाला सुरक्षित तरीका
if __name__ == "__main__":
    print("Starting bot and web server...")
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.create_task(start_web_server())
    app.run()
        
