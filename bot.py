import requests

TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"
CHAT_ID = "473201462"

USER = "teenageengineering"

url = f"https://www.instagram.com/{USER}/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:

    r = requests.get(url, headers=headers)

    if r.status_code == 200:

        text = f"🤖 Бот работает\n\nПроверен аккаунт:\nhttps://instagram.com/{USER}"

    else:

        text = "Instagram не отвечает"

except Exception as e:

    text = f"Ошибка: {e}"

send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": text
}

requests.post(send_url, data=data)
