import requests
import time
import json

# ===== НАСТРОЙКИ =====

TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"
CHAT_ID = "473201462"
USERNAME = "instagram_username"

CHECK_URL = f"https://www.instagram.com/{USERNAME}/?__a=1&__d=dis"

TELEGRAM_MESSAGE = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
TELEGRAM_PHOTO = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

LAST_POST_FILE = "last_post.txt"


# ===== функции =====

def send_message(text):
    try:
        requests.post(TELEGRAM_MESSAGE, data={
            "chat_id": CHAT_ID,
            "text": text
        })
    except:
        pass


def send_photo(photo, caption):
    try:
        requests.post(TELEGRAM_PHOTO, data={
            "chat_id": CHAT_ID,
            "photo": photo,
            "caption": caption
        })
    except:
        pass


def get_last_post():
    try:
        with open(LAST_POST_FILE, "r") as f:
            return f.read().strip()
    except:
        return None


def save_last_post(post_id):
    with open(LAST_POST_FILE, "w") as f:
        f.write(post_id)


def check_instagram():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(CHECK_URL, headers=headers)
    data = r.json()

    post = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]

    post_id = post["id"]
    caption = ""

    if post["edge_media_to_caption"]["edges"]:
        caption = post["edge_media_to_caption"]["edges"][0]["node"]["text"]

    photo = post["display_url"]
    link = f"https://www.instagram.com/p/{post['shortcode']}/"

    return post_id, photo, caption, link


# ===== старт =====

send_message("🤖 Instagram bot started")

while True:

    try:

        post_id, photo, caption, link = check_instagram()

        last_post = get_last_post()

        if post_id != last_post:

            text = f"🔥 Новый пост\n\n{caption}\n\n{link}"

            send_photo(photo, text)

            save_last_post(post_id)

    except Exception as e:
        send_message(f"⚠️ ошибка: {e}")

    time.sleep(300)
