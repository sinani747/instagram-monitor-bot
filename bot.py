import requests
import os

TOKEN = os.environ["8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"]
CHAT_ID = os.environ["473201462"]

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

send("🚀 Instagram monitor работает")
