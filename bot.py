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
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


def send_message(text):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })


def send_photo(photo, caption):

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption
    })


def load_state():

    if os.path.exists(STATE_FILE):

        with open(STATE_FILE, "r") as f:

            return json.load(f)

    return {}


def save_state(state):

    with open(STATE_FILE, "w") as f:

        json.dump(state, f)


def check_account(username, state):

    try:

        url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"

        r = requests.get(url, headers=headers, timeout=20)

        if r.status_code != 200:

            send_message(f"⚠️ Instagram не отвечает @{username}")

            return

        data = r.json()

        edges = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]

        if not edges:

            return

        post = edges[0]["node"]

        shortcode = post["shortcode"]

        photo = post["display_url"]

        last_post = state.get(username)

        if shortcode != last_post:

            link = f"https://instagram.com/p/{shortcode}"

            send_photo(photo, f"📸 Новый пост @{username}\n{link}")

            state[username] = shortcode

    except Exception as e:

        send_message(f"Ошибка @{username}: {e}")


def main():

    state = load_state()

    for account in ACCOUNTS:

        check_account(account, state)

    save_state(state)


if __name__ == "__main__":

    main()
