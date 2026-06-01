import os
import re
import random
import math  # Added for waveform calculations
import aiofiles
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps)
from py_yt import VideosSearch
from PritiMusic import app
from PritiMusic.utils.database import clonebotdb

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_glowing_circle(image):
    """
    Crops the image into a circle and applies a multi-layered glow:
    Yellow -> White -> Pink -> White, with a solid white border.
    """
    img = image.convert("RGBA")
    size = min(img.size)
    
    # 1. Crop image into a perfect circle
    img = ImageOps.fit(img, (size, size), centering=(0.5, 0.5))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    circular_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    circular_img.paste(img, (0, 0), mask)

    # 2. Setup canvas for the glow effect
    offset = 50  # Padding for the glow
    glow_size = size + (offset * 2)
    glow = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
    draw_glow = ImageDraw.Draw(glow)

    # 3. Draw concentric circles for the glow effect
    draw_glow.ellipse((5, 5, glow_size-5, glow_size-5), fill=(255, 255, 0, 60))        # Outer Yellow
    draw_glow.ellipse((15, 15, glow_size-15, glow_size-15), fill=(255, 255, 255, 80))  # Outer White
    draw_glow.ellipse((25, 25, glow_size-25, glow_size-25), fill=(255, 105, 180, 150)) # Pink
    draw_glow.ellipse((35, 35, glow_size-35, glow_size-35), fill=(255, 255, 255, 200)) # Inner White
    
    # Apply Gaussian Blur to make the glow smooth
    glow = glow.filter(ImageFilter.GaussianBlur(15))
    
    # 4. Draw a solid white border directly around the image
    draw_border = ImageDraw.Draw(glow)
    draw_border.ellipse((offset - 4, offset - 4, size + offset + 4, size + offset + 4), outline="white", width=8)

    # 5. Paste the circular image on top of the glowing background
    glow.paste(circular_img, (offset, offset), circular_img)
    
    return glow, offset

def clear(text, max_length=25):
    text = text.strip()
    return text[:max_length].rstrip() + "..." if len(text) > max_length else text

def blend_rgb(color_a, color_b, ratio: float):
    ratio = max(0.0, min(1.0, ratio))
    return tuple(
        int((color_a[index] * (1.0 - ratio)) + (color_b[index] * ratio))
        for index in range(3)
    )

def text_width(draw, text: str, font) -> float:
    try:
        return draw.textlength(text, font=font)
    except Exception:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0]

def draw_waveform(draw, x_start, y, width, height, accent_color, base_color, progress_ratio=0.37, segments=72):
    segment_width = width / max(segments - 1, 1)
    active_x = x_start + (width * progress_ratio)
    accent_rgb = accent_color[:3]
    base_rgb = base_color[:3]

    for i in range(segments):
        center_x = x_start + (i * segment_width)
        distance = abs(center_x - active_x) / max(width, 1)
        envelope = math.exp(-((distance / 0.135) ** 2))
        ripple = 0.45 + (0.55 * abs(math.sin((i * 0.39) + 0.8)))
        bar_height = max(2, int(height * (0.08 + (envelope * ripple))))
        strength = max(0.12, min(1.0, 0.16 + (envelope * 1.1)))
        color = (*blend_rgb(base_rgb, accent_rgb, strength), int(70 + (185 * strength)))

        if bar_height <= 4:
            draw.ellipse([(center_x - 1.5, y - 1.5), (center_x + 1.5, y + 1.5)], fill=color)
            continue

        draw.rounded_rectangle([(center_x - 1.5, y - bar_height), (center_x + 1.5, y)], radius=2, fill=color)

def draw_transport_controls(draw, center_x: int, center_y: int, accent_color):
    ring_color = (*blend_rgb(accent_color[:3], (255, 255, 255), 0.34), 195)
    center_ring = (*blend_rgb(accent_color[:3], (255, 255, 255), 0.18), 225)
    fill_color = (18, 24, 34, 220)
    inner_fill = (*blend_rgb((18, 24, 34), accent_color[:3], 0.18), 235)
    icon_color = (242, 245, 249, 230)

    positions = ((center_x - 65, 20, "prev"), (center_x, 24, "pause"), (center_x + 65, 20, "next"))

    for x, radius, icon in positions:
        outline = center_ring if icon == "pause" else ring_color
        draw.ellipse([(x - radius, center_y - radius), (x + radius, center_y + radius)], fill=fill_color, outline=outline, width=2)
        draw.ellipse([(x - radius + 3, center_y - radius + 3), (x + radius - 3, center_y + radius - 3)], fill=inner_fill)

        if icon == "pause":
            draw.rounded_rectangle([(x - 8, center_y - 10), (x - 3, center_y + 10)], radius=2, fill=icon_color)
            draw.rounded_rectangle([(x + 3, center_y - 10), (x + 8, center_y + 10)], radius=2, fill=icon_color)
        elif icon == "prev":
            draw.polygon([(x + 8, center_y - 10), (x - 2, center_y), (x + 8, center_y + 10)], fill=icon_color)
            draw.polygon([(x - 2, center_y - 10), (x - 12, center_y), (x - 2, center_y + 10)], fill=icon_color)
            draw.rounded_rectangle([(x + 10, center_y - 11), (x + 12, center_y + 11)], radius=1, fill=icon_color)
        else:
            draw.polygon([(x - 8, center_y - 10), (x + 2, center_y), (x - 8, center_y + 10)], fill=icon_color)
            draw.polygon([(x + 2, center_y - 10), (x + 12, center_y), (x + 2, center_y + 10)], fill=icon_color)
            draw.rounded_rectangle([(x - 12, center_y - 11), (x - 10, center_y + 11)], radius=1, fill=icon_color)

async def download_user_photo(user_id):
    try:
        async for photo in app.get_chat_photos(user_id, limit=1):
            return await app.download_media(photo.file_id, file_name=f"cache/{user_id}.jpg")
    except: return None
    return None

# ==========================================
# MAIN THUMBNAIL FUNCTION
# ==========================================
async def get_thumb(videoid, user_id, client):
    # 1. Fetch Bot & Owner
    me = await client.get_me()
    bot_name = me.first_name.upper()
    bot_id = me.id
    owner_name = "OWNER"
    try:
        bot_data = await clonebotdb.find_one({"bot_id": bot_id})
        if bot_data:
            owner = await client.get_users(bot_data.get("user_id"))
            owner_name = owner.first_name.upper()
    except: owner_name = "ADMIN"

    # 2. Setup Files
    os.makedirs("cache", exist_ok=True)
    filename = f"cache/{videoid}_{bot_id}.png"
    if os.path.isfile(filename): return filename

    # 3. Download YT Data
    results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
    data = await results.next()
    result = data["result"][0]
    title = re.sub(r"\W+", " ", result["title"]).title()
    duration = result.get("duration", "00:00")
    views = result.get("viewCount", {}).get("short", "Unknown")
    channel = result.get("channel", {}).get("name", "Unknown Artist")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(result["thumbnails"][0]["url"].split("?")[0]) as resp:
            f = await aiofiles.open(f"cache/temp_{videoid}.jpg", mode="wb")
            await f.write(await resp.read())
            await f.close()

    # 4. Drawing Logic
    bg = Image.open(f"cache/temp_{videoid}.jpg").convert("RGBA").resize((1920, 1080))
    background = bg.filter(ImageFilter.GaussianBlur(25)).point(lambda p: p * 0.4)
    
    # --- SOLID BLACK CARD ---
    black_card = Image.new("RGBA", background.size, (0, 0, 0, 0))
    draw_card = ImageDraw.Draw(black_card)
    # Fill is now solid black (0, 0, 0, 255)
    draw_card.rounded_rectangle((40, 40, 1880, 940), radius=60, fill=(0, 0, 0, 255), outline=(132, 224, 240, 200), width=6)
    
    # Paste black card onto blurred background
    background = Image.alpha_composite(background, black_card)
    draw = ImageDraw.Draw(background)

    # --- RAIN EFFECT ---
    for _ in range(300):
        rx = random.randint(50, 1870)
        ry = random.randint(50, 930)
        length = random.randint(10, 30)
        draw.line([(rx, ry), (rx + 5, ry + length)], fill=(255, 255, 255, 50), width=1)
    
    try:
        f1 = ImageFont.truetype("PritiMusic/assets/font.ttf", 65)
        f2 = ImageFont.truetype("PritiMusic/assets/font2.ttf", 45)
        br = ImageFont.truetype("PritiMusic/assets/font2.ttf", 50)
    except:
        f1 = f2 = br = ImageFont.load_default()

    # --- GLOWING IMAGES ---
    # YouTube Thumbnail
    yt_img_glowing, yt_offset = get_glowing_circle(bg.resize((500, 500)))
    background.paste(yt_img_glowing, (80 - yt_offset, 250 - yt_offset), yt_img_glowing)
    
    # User Profile Image
    u_photo = await download_user_photo(user_id)
    if u_photo:
        u_img_glowing, u_offset = get_glowing_circle(Image.open(u_photo).resize((450, 450)))
        background.paste(u_img_glowing, (1350 - u_offset, 250 - u_offset), u_img_glowing)

    # Fetch User Name
    try:
        user_info = await client.get_users(user_id)
        user_name = user_info.first_name
    except: user_name = "User"

    # Text Placement
    draw.text((650, 300), clear(title, 25), fill="white", font=f1)
    draw.text((650, 400), f"Artist: {channel}", fill=(200, 200, 200), font=f2)
    draw.text((650, 470), f"Views: {views}", fill=(150, 150, 150), font=f2)
    draw.text((650, 530), f"Duration: {duration}", fill=(150, 150, 150), font=f2)
    
    # Branding & Request
    draw.text((100, 100), f"BOT: {bot_name}", fill="yellow", font=br)
    draw.text((1400, 100), f"OWNER: {owner_name}", fill="cyan", font=br)
    draw.text((1350, 880), f"Requested by: {user_name[:15]}", fill="white", font=f2)

    # ==========================================
    # NEW PLAYBACK UI WIDGET (SOLID BLACK BG)
    # ==========================================
    PLAYBACK_BOX = (650, 630, 1750, 790)  # Box positioning
    playback_accent = (132, 224, 240)    # Cyan accent to match borders
    progress_time_font = f2

    # 1. Base dark rounded box for playback UI (SOLID BLACK)
    draw.rounded_rectangle(
        PLAYBACK_BOX,
        radius=28,
        fill=(0, 0, 0, 255),  # <-- Solid Black 
        outline=(255, 255, 255, 60),
        width=2
    )

    # 2. Setup calculations for the playback progress line
    progress_left = PLAYBACK_BOX[0] + 40
    bar_y = PLAYBACK_BOX[1] + 65
    bar_x_start = progress_left
    bar_x_end = PLAYBACK_BOX[2] - 40
    bar_width = bar_x_end - bar_x_start
    progress_ratio = 0.40  # 40% completed
    prog_x = bar_x_start + int(bar_width * progress_ratio)

    # 3. Base line and Filled progress line
    draw.line([(bar_x_start, bar_y), (bar_x_end, bar_y)], fill=(255, 255, 255, 80), width=4)
    draw.line([(bar_x_start, bar_y), (prog_x, bar_y)], fill=(*playback_accent, 255), width=5)
    
    # 4. Waveform visualization (Draws above the line)
    draw_waveform(
        draw,
        bar_x_start,
        bar_y - 4,
        bar_width,
        45,  # Height of the wave
        playback_accent,
        (255, 255, 255),
        progress_ratio=progress_ratio,
        segments=95,
    )

    # 5. Playhead thumb on the progress line
    draw.ellipse([(prog_x - 14, bar_y - 14), (prog_x + 14, bar_y + 14)], fill=(*playback_accent, 70))
    draw.ellipse([(prog_x - 8, bar_y - 8), (prog_x + 8, bar_y + 8)], fill=(255, 255, 255), outline=playback_accent, width=3)

    # 6. Start time (00:00) and End time
    time_y = PLAYBACK_BOX[1] + 85
    draw.text((bar_x_start, time_y), "00:00", fill=(255, 255, 255), font=progress_time_font)
    duration_text_width = text_width(draw, duration, progress_time_font)
    draw.text((bar_x_end - duration_text_width, time_y), duration, fill=(255, 255, 255), font=progress_time_font)

    # 7. Transport Controls (Previous, Pause, Next)
    draw_transport_controls(
        draw,
        center_x=(PLAYBACK_BOX[0] + PLAYBACK_BOX[2]) // 2,
        center_y=PLAYBACK_BOX[1] + 110,
        accent_color=playback_accent,
    )
    # ==========================================

    background.convert("RGB").save(filename)
    if os.path.exists(f"cache/temp_{videoid}.jpg"):
        os.remove(f"cache/temp_{videoid}.jpg")
    if u_photo and os.path.exists(u_photo): 
        os.remove(u_photo)
    return filename
