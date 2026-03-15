import requests
import json
import os
from bs4 import BeautifulSoup

TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"
CHAT_ID = "473201462"

ACCOUNTS = [
    "teenageengineering",
    "instagram"
]

STATE_FILE = "state.json"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def send_message(text):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url, data=data)


def send_photo(photo, caption):

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    data = {
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption
    }

    requests.post(url, data=data)


def load_state():

    if not os.path.exists(STATE_FILE):
        return {}

    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(data):

    with open(STATE_FILE, "w") as f:
        json.dump(data, f)


def check_account(username):

    url = f"https://www.instagram.com/{username}/"

    r = requests.get(url, headers=headers, timeout=20)

    if r.status_code != 200:
        raise Exception(f"{username} не отвечает")

    soup = BeautifulSoup(r.text, "html.parser")

    images = soup.find_all("img")

    if len(images) < 2:
        raise Exception(f"{username} фото не найдено")

    photo = images[1]["src"]

    link = f"https://instagram.com/{username}"

    return photo, link


try:

    state = load_state()

    for account in ACCOUNTS:

        photo, link = check_account(account)

        last = state.get(account)

        if last != photo:

            caption = f"🔥 Новый пост @{account}\n{link}"

            send_photo(photo, caption)

            state[account] = photo

        else:

            send_message(f"✅ @{account} — новых постов нет")

    save_state(state)

except Exception as e:

    send_message(f"⚠️ Ошибка: {e}")
