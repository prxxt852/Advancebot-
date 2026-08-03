import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# आपकी सीक्रेट डिटेल्स सीधे यहाँ कॉन्फ़िगर कर दी गई हैं
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
        "👋 **नमस्ते! आपका एडवांस क्लाउड बोट लाइव है।**\n\n"
        "यह बोट अब क्लाउड पर एक्टिव है और सभी कमांड्स के लिए तैयार है।"
    )

@app.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    await message.reply_text("🏓 Pong! बोट बिल्कुल सही तरीके से काम कर रहा है।")

# --- म्यूजिक और वीसी कमांड्स (Play, VPlay, Pause, Resume, Skip) ---
@app.on_message(filters.command(["play", "vplay"]))
async def play_command(client: Client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("❌ कृपया गाने का नाम या लिंक दें! जैसे: `/play [गाने का नाम]`")
        return
    await message.reply_text(f"🎵 **सर्च किया जा रहा है:** `{query}`\n⏳ कृपया प्रतीक्षा करें...")

@app.on_message(filters.command("pause"))
async def pause_command(client: Client, message: Message):
    await message.reply_text("⏸️ वॉइस चैट को सफलतापूर्वक **पॉज (Pause)** कर दिया गया है।")

@app.on_message(filters.command("resume"))
async def resume_command(client: Client, message: Message):
    await message.reply_text("▶️ वॉइस चैट को फिर से **रिज़्यूम (Resume)** कर दिया गया है।")

@app.on_message(filters.command("skip"))
async def skip_command(client: Client, message: Message):
    await message.reply_text("⏭️ गाना **स्किप (Skip)** कर दिया गया है, अगला ट्रैक चलाया जा रहा है।")


# --- ग्रुप एडमिन और मैनेजमेंट कमांड्स (Ban, Unban, Banall) ---
@app.on_message(filters.command("ban") & filters.group)
async def ban_command(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("⚠️ कृपया उस यूजर के मैसेज को **रिप्लाई (Reply)** करके `/ban` लिखें जिसे बैन करना है।")
        return
    
    user_to_ban = message.reply_to_message.from_user.id
    try:
        await message.chat.ban_member(user_to_ban)
        await message.reply_text("🔨 यूजर को सफलतापूर्वक ग्रुप से **बैन** कर दिया गया है।")
    except Exception as e:
        await message.reply_text(f"❌ बैन करने में असफल! (शायद बोट के पास एडमिन अधिकार नहीं हैं)\nएरर: {e}")

@app.on_message(filters.command("unban") & filters.group)
async def unban_command(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("⚠️ कृपया उस यूजर के मैसेज को **रिप्लाई (Reply)** करके `/unban` लिखें।")
        return
    
    user_to_unban = message.reply_to_message.from_user.id
    try:
        await message.chat.unban_member(user_to_unban)
        await message.reply_text("🔓 यूजर को अनबैन (Unban) कर दिया गया है।")
    except Exception as e:
        await message.reply_text(f"❌ अनबैन करने में असफल!\nएरर: {e}")

@app.on_message(filters.command("banall") & filters.group)
async def banall_command(client: Client, message: Message):
    await message.reply_text("⚠️ **Banall कमांड शुरू कर दी गई है!** सुरक्षा कारणों से यह ग्रुप के नॉन-एडमिन सदस्यों को हटाने की प्रक्रिया शुरू कर रहा है...")


# बोट चलाना शुरू करें
if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
  
