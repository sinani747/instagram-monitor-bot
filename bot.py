import requests
import os

TOKEN = os.environ["8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"]
CHAT_ID = os.environ["473201462"]

message = "🤖 Instagram monitor работает"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message
})
