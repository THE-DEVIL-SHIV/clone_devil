from typing import Union
import random
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton

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


def setting_markup(_):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=_["ST_B_1"], cb="AU", style=s_map[1]),
            create_btn(text=_["ST_B_3"], cb="LG", style=s_map[1]),
        ],
        [
            create_btn(text=_["ST_B_2"], cb="PM", style=s_map[2]),
        ],
        [
            create_btn(text=_["ST_B_4"], cb="VM", style=s_map[3]),
        ],
        [
            create_btn(text=_["CLOSE_BUTTON"], cb="close", style=s_map[1]),
        ],
    ]
    return buttons


def vote_mode_markup(_, current, mode: Union[bool, str] = None):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text="Vᴏᴛɪɴɢ ᴍᴏᴅᴇ ➜", cb="VOTEANSWER", style=s_map[1], no_emoji=True),
            create_btn(
                text=_["ST_B_5"] if mode == True else _["ST_B_6"],
                cb="VOMODECHANGE",
                style=s_map[1]
            ),
        ],
        [
            create_btn(text="-2", cb="FERRARIUDTI M", style=s_map[2], no_emoji=True),
            create_btn(
                text=f"ᴄᴜʀʀᴇɴᴛ : {current}",
                cb="ANSWERVOMODE",
                style=s_map[2],
                no_emoji=True
            ),
            create_btn(text="+2", cb="FERRARIUDTI A", style=s_map[2], no_emoji=True),
        ],
        [
            create_btn(
                text=_["BACK_BUTTON"],
                cb="settings_helper",
                style=s_map[3]
            ),
            create_btn(text=_["CLOSE_BUTTON"], cb="close", style=s_map[3]),
        ],
    ]
    return buttons


def auth_users_markup(_, status: Union[bool, str] = None):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=_["ST_B_7"], cb="AUTHANSWER", style=s_map[1]),
            create_btn(
                text=_["ST_B_8"] if status == True else _["ST_B_9"],
                cb="AUTH",
                style=s_map[1]
            ),
        ],
        [
            create_btn(text=_["ST_B_1"], cb="AUTHLIST", style=s_map[2]),
        ],
        [
            create_btn(
                text=_["BACK_BUTTON"],
                cb="settings_helper",
                style=s_map[3]
            ),
            create_btn(text=_["CLOSE_BUTTON"], cb="close", style=s_map[3]),
        ],
    ]
    return buttons


def playmode_users_markup(
    _,
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=_["ST_B_10"], cb="SEARCHANSWER", style=s_map[1]),
            create_btn(
                text=_["ST_B_11"] if Direct == True else _["ST_B_12"],
                cb="MODECHANGE",
                style=s_map[1]
            ),
        ],
        [
            create_btn(text=_["ST_B_13"], cb="AUTHANSWER", style=s_map[2]),
            create_btn(
                text=_["ST_B_8"] if Group == True else _["ST_B_9"],
                cb="CHANNELMODECHANGE",
                style=s_map[2]
            ),
        ],
        [
            create_btn(text=_["ST_B_14"], cb="PLAYTYPEANSWER", style=s_map[3]),
            create_btn(
                text=_["ST_B_8"] if Playtype == True else _["ST_B_9"],
                cb="PLAYTYPECHANGE",
                style=s_map[3]
            ),
        ],
        [
            create_btn(
                text=_["BACK_BUTTON"],
                cb="settings_helper",
                style=s_map[1]
            ),
            create_btn(text=_["CLOSE_BUTTON"], cb="close", style=s_map[1]),
        ],
    ]
    return buttons
