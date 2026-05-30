import random 
import config
from PritiMusic import app

# Yahan styled_button aur ButtonStyle import kiya gaya hai
from button import styled_button, ButtonStyle


def start_panel(_):
    buttons = [
        [
            styled_button(
                text=_["SO_B_1"], 
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.SUCCESS
            ),
            styled_button(
                text=_["S_B_2"], 
                url=config.SUPPORT_CHAT, 
                style=ButtonStyle.PRIMARY
            ),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            styled_button(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.SUCCESS
            )
        ],
        [
            styled_button(
                text=_["S_B_5"], 
                user_id=config.OWNER_ID, 
                style=ButtonStyle.PRIMARY
            ),
            styled_button(
                text="ᴄʟᴏɴᴇ", 
                callback_data="clone_page", 
                style=ButtonStyle.SUCCESS
            )
        ],
        [
            styled_button(
                text="sᴜᴘᴘᴏʀᴛ", 
                callback_data="support_page", 
                style=ButtonStyle.PRIMARY
            ),
            styled_button(
                text=" sᴏᴜʀᴄᴇ", 
                callback_data="gib_source", 
                style=ButtonStyle.PRIMARY
            )
        ],
        [
            styled_button(
                text=_["S_B_4"], 
                callback_data="settings_back_helper", 
                style=ButtonStyle.PRIMARY
            )
        ],
    ]
    return buttons


def support_panel(_):
    buttons = [
        [
            styled_button(
                text=_["S_B_2"], 
                url=config.SUPPORT_CHAT, 
                style=ButtonStyle.PRIMARY
            ),
            styled_button(
                text=_["S_B_6"], 
                url=config.SUPPORT_CHANNEL, 
                style=ButtonStyle.PRIMARY
            ),
        ],
        [
            styled_button(
                text=_["BACK_BUTTON"], 
                callback_data="settingsback_helper", 
                style=ButtonStyle.PRIMARY
            )
        ]
    ]
    return buttons


def about_panel(_):
    buttons = [
        [
            styled_button(
                text=_["S_B_5"], 
                user_id=config.OWNER_ID, 
                style=ButtonStyle.PRIMARY
            ),
            styled_button(
                text=_["S_B_11"], 
                url=config.GITHUB, 
                style=ButtonStyle.PRIMARY
            ),
        ],
        [
            styled_button(
                text=_["S_B_6"], 
                url=config.SUPPORT_CHANNEL, 
                style=ButtonStyle.PRIMARY
            ),
            styled_button(
                text=_["S_B_2"], 
                url=config.SUPPORT_CHAT, 
                style=ButtonStyle.PRIMARY
            )
        ],
        [
            styled_button(
                text=_["BACK_BUTTON"], 
                callback_data="settingsback_helper", 
                style=ButtonStyle.PRIMARY
            )
        ]
    ]
    return buttons
