import requests
from bs4 import BeautifulSoup
import time

TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"
CHAT_ID = "473201462"

URL = "https://www.instagram.com/teenageengineering/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

last_post = None

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def check_instagram():
    global last_post

    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.find_all("a")

    for link in links:
        href = link.get("href", "")
        if "/p/" in href:
            post_link = "https://instagram.com" + href

            if last_post is None:
                last_post = post_link
                return

            if post_link != last_post:
                last_post = post_link
                send(f"📸 Новый пост!\n{post_link}")
                return

while True:
    check_instagram()
    time.sleep(60)
