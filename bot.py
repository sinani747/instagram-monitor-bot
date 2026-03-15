print("NEW VERSION STARTED")

import requests
import xml.etree.ElementTree as ET
import os

TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"
CHAT_ID = "473201462"
USERNAME = "teenageengineering"

STATE_FILE = "last.txt"

rss_url = f"https://rsshub.app/instagram/user/{USERNAME}"


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


def save_last(value):
    with open(STATE_FILE, "w") as f:
        f.write(value)


try:

    r = requests.get(rss_url, timeout=20)

    if r.status_code != 200:
        print("RSS не отвечает")
        exit()

    data = r.text.strip()

    if data == "":
        print("RSS пустой")
        exit()

    if "<rss" not in data:
        print("RSS неправильный")
        exit()

    root = ET.fromstring(data)

    item = root.find(".//item")

    if item is None:
        print("Нет постов")
        exit()

    link = item.find("link").text
    guid = item.find("guid").text
    photo = item.find(".//enclosure").attrib["url"]

    last = load_last()

    if guid != last:

        send_photo(photo, f"📸 Новый пост\n{link}")

        save_last(guid)

except Exception as e:

    print("Ошибка:", e)
