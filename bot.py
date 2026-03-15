import requests
import json
import os

TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"
CHAT_ID = "473201462"

ACCOUNTS = [
    "teenageengineering"
]

STATE_FILE = "state.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "X-IG-App-ID": "936619743392459"
}


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


def send_photo(photo, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption
    })


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def check_account(username, state):

    url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"

    r = requests.get(url, headers=headers, timeout=20)

    if r.status_code != 200:
        send_message(f"⚠️ Instagram не отвечает @{username}")
        return

    data = r.json()

    posts = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]

    if not posts:
        return

    post = posts[0]["node"]

    shortcode = post["shortcode"]
    photo = post["display_url"]

    last = state.get(username)

    if shortcode != last:

        link = f"https://instagram.com/p/{shortcode}"

        send_photo(photo, f"📸 Новый пост @{username}\n{link}")

        state[username] = shortcode


def main():

    state = load_state()

    for account in ACCOUNTS:
        try:
            check_account(account, state)
        except Exception as e:
            send_message(f"Ошибка @{account}: {e}")

    save_state(state)


if __name__ == "__main__":
    main()
