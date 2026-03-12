import requests
import time
from bs4 import BeautifulSoup
import os

TOKEN = os.environ["8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"]
CHAT_ID = os.environ["473201462"]

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

send("🚀 Instagram монитор запущен")

while True:

    try:

        r = requests.get(URL, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        scripts = soup.find_all("script")
        text = str(scripts)

        start = text.find("/p/")
        shortcode = text[start+3:start+14]

        if last_post is None:
            last_post = shortcode

        if shortcode != last_post:

            last_post = shortcode
            link = f"https://instagram.com/p/{shortcode}"

            send("🔥 Новый пост\n" + link)

        time.sleep(60)

    except Exception as e:

        send("⚠️ Ошибка: " + str(e))
        time.sleep(120)
