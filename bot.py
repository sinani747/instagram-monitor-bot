print("BOT STARTED")

import requests
import xml.etree.ElementTree as ET
import os

TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0
"
CHAT_ID = "473201462"
USERNAME = "teenageengineering"

STATE_FILE = "last.txt"
RSS_URL = f"https://rsshub.app/instagram/user/{USERNAME}"


def send_photo(photo, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption
    })


def load_last():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return f.read().strip()
    return ""


def save_last(v):
    with open(STATE_FILE, "w") as f:
        f.write(v)


try:
    r = requests.get(RSS_URL, timeout=20)

    if r.status_code != 200:
        exit()

    data = r.text.strip()

    # если RSSHub вернул HTML или пустоту
    if not data.startswith("<"):
        exit()

    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        exit()

    item = root.find(".//item")
    if item is None:
        exit()

    link = item.find("link").text
    guid = item.find("guid").text

    enclosure = item.find(".//enclosure")
    if enclosure is None:
        exit()

    photo = enclosure.attrib.get("url")

    last = load_last()

    if guid != last:
        send_photo(photo, f"📸 Новый пост\n{link}")
        save_last(guid)

except:
    # никаких сообщений об ошибке в Telegram
    pass
