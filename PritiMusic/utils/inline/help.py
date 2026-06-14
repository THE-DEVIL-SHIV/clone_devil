import random
from typing import Union

from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from PritiMusic import app

# 🔥 PREMIUM EMOJIS LIST 🔥
# Yahan aap apne pasand ke Premium Emojis ke IDs daal sakte hain.
PREMIUM_EMOJIS = [
    "5422831825178206894", 
    "5368324170673489600", 
    "5206607081334906820", 
    "5206380668048496464", 
]

# 🎨 Dynamic Color Generator
def get_style_map():
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    random.shuffle(styles)
    # Row me buttons ke hisaab se random color assign hoga
    return {1: styles[0], 2: styles[1], 3: styles[2]}

# 🔘 Smart Button Creator
def create_btn(text, cb=None, url=None, style=ButtonStyle.PRIMARY, no_emoji=False):
    kwargs = {"text": text, "style": style}
    if cb: kwargs["callback_data"] = cb
    if url: kwargs["url"] = url
    if not no_emoji: kwargs["icon_custom_emoji_id"] = random.choice(PREMIUM_EMOJIS)
    return InlineKeyboardButton(**kwargs)


def help_pannel(_, START: Union[bool, int] = None):
    s_map = get_style_map()
    first = [
        [
            create_btn(text=_["H_B_1"], cb="help_callback hb1", style=s_map[3]),
            create_btn(text=_["H_B_2"], cb="help_callback hb2", style=s_map[3]),
            create_btn(text=_["H_B_3"], cb="help_callback hb3", style=s_map[3]),
        ],
        [
            create_btn(text=_["H_B_4"], cb="help_callback hb4", style=s_map[3]),
            create_btn(text=_["H_B_5"], cb="help_callback hb5", style=s_map[3]),
            create_btn(text=_["H_B_6"], cb="help_callback hb6", style=s_map[3]),
        ],
        [
            create_btn(text=_["H_B_7"], cb="help_callback hb7", style=s_map[3]),
            create_btn(text=_["H_B_8"], cb="help_callback hb8", style=s_map[3]),
            create_btn(text=_["H_B_9"], cb="help_callback hb9", style=s_map[3]),
        ],
        [
            create_btn(text=_["H_B_10"], cb="help_callback hb10", style=s_map[3]),
            create_btn(text=_["H_B_11"], cb="help_callback hb11", style=s_map[3]),
            create_btn(text=_["H_B_12"], cb="help_callback hb12", style=s_map[3]),
        ],
        [
            create_btn(text=_["H_B_13"], cb="help_callback hb13", style=s_map[3]),
            create_btn(text=_["H_B_14"], cb="help_callback hb14", style=s_map[3]),
            create_btn(text=_["H_B_15"], cb="help_callback hb15", style=s_map[3]),
        ],
        [
            create_btn(text=_["BACK_BUTTON"], cb="settingsback_helper", style=s_map[1]),
        ],
    ]
    return InlineKeyboardMarkup(first)


def first_page(_, is_owner: bool = False):
    s_map = get_style_map()
    first = [
        [
            create_btn(text=_["H_B_1"], cb="help_callback hb1", style=s_map[3]),
            create_btn(text=_["H_B_2"], cb="help_callback hb2", style=s_map[3]),
            create_btn(text=_["H_B_3"], cb="help_callback hb3", style=s_map[3]),
        ],
        [
            create_btn(text=_["H_B_11"], cb="help_callback hb11", style=s_map[3]),
            create_btn(text=_["H_B_8"], cb="help_callback hb8", style=s_map[3]),
            create_btn(text=_["H_B_6"], cb="help_callback hb6", style=s_map[3]),
        ],
        [
            create_btn(text=_["H_B_13"], cb="help_callback hb13", style=s_map[3]),
            create_btn(text=_["H_B_12"], cb="help_callback hb12", style=s_map[3]),
            create_btn(text=_["H_B_9"], cb="help_callback cloghelp", style=s_map[3]),
        ],
        [
            create_btn(text=_["H_B_10"], cb="help_callback hb10", style=s_map[3]),
            create_btn(text=_["H_B_14"], cb="help_callback hb14", style=s_map[3]),
            create_btn(text=_["H_B_15"], cb="help_callback hb15", style=s_map[3]),
        ],
    ]
    
    if is_owner:
        first.append([create_btn(text="🛠 ᴄʟᴏɴᴇ ғᴇᴀᴛᴜʀᴇ", cb="help_callback chelp", style=s_map[1])])

    first.append([create_btn(text=_["BACK_BUTTON"], cb="settingsback_home", style=s_map[1])])
    return InlineKeyboardMarkup(first)


def clone_help_panel(_):
    s_map = get_style_map()
    buttons = [
        [create_btn(text="ᴍᴀɴᴀɢᴇ", cb="help_callback clone_manage", style=s_map[1])],
        [
            create_btn(text="sᴛᴀʀᴛ", cb="help_callback clone_start", style=s_map[2]),
            create_btn(text="ᴘɪɴɢ", cb="help_callback clone_ping", style=s_map[2]),
        ],
        [
            create_btn(text="ᴘʟᴀʏ ᴍᴏᴅᴇ", cb="help_callback clone_play", style=s_map[2]),
            create_btn(text="ʟᴏɢɢᴇʀ", cb="help_callback clone_logger", style=s_map[2]),
        ],
        [create_btn(text="ʙᴜᴛᴛᴏɴs & ʀᴇɴᴀᴍᴇ", cb="help_callback clone_buttons", style=s_map[1])],
        [create_btn(text=_["BACK_BUTTON"], cb="settings_back_helper", style=s_map[1])],
    ]
    return InlineKeyboardMarkup(buttons)


def clone_back_markup(_):
    s_map = get_style_map()
    return InlineKeyboardMarkup([
        [create_btn(text=_["BACK_BUTTON"], cb="help_callback chelp", style=s_map[1])]
    ])


def help_back_markup(_):
    s_map = get_style_map()
    return InlineKeyboardMarkup([
        [create_btn(text=_["BACK_BUTTON"], cb="settings_back_helper", style=s_map[1])]
    ])


def private_help_panel(_):
    s_map = get_style_map()
    return InlineKeyboardMarkup([
        [create_btn(text=_["S_B_4"], url=f"https://t.me/{app.username}?start=help", style=s_map[1])]
    ])
