import requests
import os

TOKEN = os.environ["8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"]
CHAT_ID = os.environ["473201462"]

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

username = "teenageengineering"

url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        send("🤖 Бот проверил Instagram — работает")
    else:
        send("⚠️ Instagram не ответил")

except Exception as e:
    send("❌ Ошибка: " + str(e))
