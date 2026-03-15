import time
import os
import telegram
from instagrapi import Client

# ===== ТВОИ ДАННЫЕ =====

TELEGRAM_TOKEN = "8739941878:AAF3ZvpUlmenPixhJ1_hCJuOvnfWtcKINX0"
CHAT_ID = "473201462"

IG_USERNAME = "aaron_sinani"
IG_PASSWORD = "Alina19@_"

TARGET_USER = "teenageengineering"

# =======================

SESSION_FILE = "session.json"
LAST_POST_FILE = "last_post.txt"

bot = telegram.Bot(token=TELEGRAM_TOKEN)
cl = Client()


def send(msg):
    try:
        bot.send_message(chat_id=CHAT_ID, text=msg)
    except Exception as e:
        print("Telegram error:", e)


def login():

    try:

        if os.path.exists(SESSION_FILE):

            cl.load_settings(SESSION_FILE)
            cl.login(IG_USERNAME, IG_PASSWORD)

            send("Instagram session восстановлена")

        else:

            cl.login(IG_USERNAME, IG_PASSWORD)
            cl.dump_settings(SESSION_FILE)

            send("Создана новая Instagram session")

    except Exception as e:

        send(f"Login error: {e}")

        time.sleep(60)

        cl.login(IG_USERNAME, IG_PASSWORD)
        cl.dump_settings(SESSION_FILE)

        send("Повторный login успешный")


def get_last_post():

    if not os.path.exists(LAST_POST_FILE):
        return None

    with open(LAST_POST_FILE, "r") as f:
        return f.read().strip()


def save_last_post(post_id):

    with open(LAST_POST_FILE, "w") as f:
        f.write(post_id)


def check_new_post():

    try:

        user_id = cl.user_id_from_username(TARGET_USER)

        medias = cl.user_medias(user_id, 1)

        if not medias:
            return

        current_post = str(medias[0].pk)

        last_post = get_last_post()

        if current_post != last_post:

            save_last_post(current_post)

            link = f"https://instagram.com/p/{medias[0].code}"

            send(f"🔥 Новый пост @{TARGET_USER}\n{link}")

    except Exception as e:

        send(f"Instagram error: {e}")


def main():

    send("Бот запущен")

    login()

    check_new_post()


if __name__ == "__main__":
    main()
