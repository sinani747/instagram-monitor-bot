import requests
import json
import os

TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"
CHAT_ID = "473201462"
USERNAME = "teenageengineering"

LAST_POST_FILE = "last_post.txt"

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


def get_last_post():

    if not os.path.exists(LAST_POST_FILE):
        return None

    with open(LAST_POST_FILE, "r") as f:
        return f.read().strip()


def save_last_post(post_id):

    with open(LAST_POST_FILE, "w") as f:
        f.write(post_id)


def check_instagram():

    url = f"https://www.instagram.com/{USERNAME}/?__a=1&__d=dis"

    r = requests.get(url, headers=headers)

    data = r.json()

    post = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]

    post_id = post["id"]

    shortcode = post["shortcode"]

    photo = post["display_url"]

    caption = ""

    if post["edge_media_to_caption"]["edges"]:

        caption = post["edge_media_to_caption"]["edges"][0]["node"]["text"]

    link = f"https://instagram.com/p/{shortcode}"

    return post_id, photo, caption, link


try:

    post_id, photo, caption, link = check_instagram()

    last_post = get_last_post()

    if post_id != last_post:

        text = f"🔥 Новый пост\n\n{caption}\n\n{link}"

        send_photo(photo, text)

        save_last_post(post_id)

    else:

        send_message("Бот работает. Новых постов нет.")

except Exception as e:

    send_message(f"⚠️ Ошибка: {e}")
