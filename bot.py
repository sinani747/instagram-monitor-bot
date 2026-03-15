import requests
import os

TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"
CHAT_ID = "473201462"

ACCOUNTS = [
    "teenageengineering",
    "instagram"
]

LAST_POST_FILE = "last_posts.json"

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


def load_last_posts():

    if not os.path.exists(LAST_POST_FILE):
        return {}

    import json

    with open(LAST_POST_FILE) as f:
        return json.load(f)


def save_last_posts(data):

    import json

    with open(LAST_POST_FILE, "w") as f:
        json.dump(data, f)


def check_account(username):

    url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"

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

    last_posts = load_last_posts()

    for account in ACCOUNTS:

        post_id, photo, caption, link = check_account(account)

        last_post = last_posts.get(account)

        if post_id != last_post:

            text = f"🔥 Новый пост @{account}\n\n{caption}\n\n{link}"

            send_photo(photo, text)

            last_posts[account] = post_id

        else:

            send_message(f"✅ @{account} — новых постов нет")

    save_last_posts(last_posts)

except Exception as e:

    send_message(f"⚠️ Ошибка бота: {e}")
