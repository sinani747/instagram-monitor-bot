import requests
import json
import os

TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"
CHAT_ID = "473201462"

USERNAME = "teenageengineering"

url = f"https://www.instagram.com/{USERNAME}/?__a=1&__d=dis"

headers = {
    "User-Agent": "Mozilla/5.0"
}

data = requests.get(url, headers=headers).json()

post = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]

post_id = post["id"]
caption = ""

if post["edge_media_to_caption"]["edges"]:
    caption = post["edge_media_to_caption"]["edges"][0]["node"]["text"]

photo = post["display_url"]
link = f"https://instagram.com/p/{post['shortcode']}"

# файл памяти
file = "last_post.txt"

last_post = ""

if os.path.exists(file):
    with open(file, "r") as f:
        last_post = f.read()

if post_id != last_post:

    message = f"📸 Новый пост\n\n{caption}\n\n{link}"

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
        data={
            "chat_id": CHAT_ID,
            "photo": photo,
            "caption": message
        }
    )

    with open(file, "w") as f:
        f.write(post_id)
