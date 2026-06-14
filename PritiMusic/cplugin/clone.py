import random
from pyrogram import Client, filters
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

import config
from PritiMusic.utils.decorators.language import language

# 🔥 PREMIUM EMOJIS LIST 🔥
PREMIUM_EMOJIS = [
    "5422831825178206894", 
    "5368324170673489600",
    "5206607081334906820",
    "5206380668048496464"
]

# 🎨 Dynamic Color Generator (Random Styles)
def get_style_map():
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    random.shuffle(styles)
    # Row me buttons ke hisaab se random color assign hoga
    return {1: styles[0], 2: styles[1], 3: styles[2]}

# 🔘 Smart Button Creator
def create_btn(text, cb=None, url=None, user_id=None, style=ButtonStyle.PRIMARY, no_emoji=False):
    kwargs = {"text": text, "style": style}
    if cb: kwargs["callback_data"] = cb
    if url: kwargs["url"] = url
    if user_id: kwargs["user_id"] = user_id
    if not no_emoji: kwargs["icon_custom_emoji_id"] = random.choice(PREMIUM_EMOJIS)
    return InlineKeyboardButton(**kwargs)

# Main Bot Link
BOT_LINK = "https://t.me/clone_MUSICrobot"

# ✅ Helper to safely get Random Start Image
def get_random_start_img():
    if config.START_IMG_URL:
        if isinstance(config.START_IMG_URL, list):
            return random.choice(config.START_IMG_URL)
        return config.START_IMG_URL
    return "https://files.catbox.moe/10zwqs.jpg" # Fallback Image


@Client.on_message(filters.command("clone"))
@language
async def ping_clone(client: Client, message: Message, _):
    # Random style map generate karna
    s_map = get_style_map()
    
    # ✅ Random Photo Logic with Dynamic Colored Button
    await message.reply_photo(
        photo=get_random_start_img(),
        caption=_["NO_CLONE_MSG"],
        reply_markup=InlineKeyboardMarkup(
            [
                [create_btn(text="ɢᴏ ᴀɴᴅ ᴄʟᴏɴᴇ", url=BOT_LINK, style=s_map[1])]
            ]
        )
    )
