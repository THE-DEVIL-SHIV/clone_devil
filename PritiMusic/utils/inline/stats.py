import random
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

# 🔘 Smart Colored Button Creator
def create_btn(text, cb=None, url=None, style=ButtonStyle.PRIMARY, no_emoji=False):
    kwargs = {"text": text, "style": style}
    if cb: kwargs["callback_data"] = cb
    if url: kwargs["url"] = url
    if not no_emoji: kwargs["icon_custom_emoji_id"] = random.choice(PREMIUM_EMOJIS)
    return InlineKeyboardButton(**kwargs)


def stats_buttons(_, status):
    s_map = get_style_map()
    
    not_sudo = [
        create_btn(
            text=_["SA_B_1"],
            cb="TopOverall",
            style=s_map[1]
        )
    ]
    
    sudo = [
        create_btn(
            text=_["SA_B_2"],
            cb="bot_stats_sudo",
            style=s_map[2]
        ),
        create_btn(
            text=_["SA_B_3"],
            cb="TopOverall",
            style=s_map[2]
        ),
    ]
    
    upl = InlineKeyboardMarkup(
        [
            sudo if status else not_sudo,
            [
                create_btn(
                    text=_["CLOSE_BUTTON"],
                    cb="close",
                    style=s_map[1],
                    no_emoji=True
                ),
            ],
        ]
    )
    return upl


def back_stats_buttons(_):
    s_map = get_style_map()
    
    upl = InlineKeyboardMarkup(
        [
            [
                create_btn(
                    text=_["BACK_BUTTON"],
                    cb="stats_back",
                    style=s_map[2],
                    no_emoji=True
                ),
                create_btn(
                    text=_["CLOSE_BUTTON"],
                    cb="close",
                    style=s_map[2],
                    no_emoji=True
                ),
            ],
        ]
    )
    return upl
