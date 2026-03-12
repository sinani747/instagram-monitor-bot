import requests

# ВСТАВЬ СЮДА СВОЙ ТОКЕН
TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"

# ВСТАВЬ СЮДА CHAT ID
CHAT_ID = "473201462"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)

send("🚀 Instagram monitor работает!")
