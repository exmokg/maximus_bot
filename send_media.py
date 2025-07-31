import os
import asyncio
from telethon import TelegramClient, errors
from config import FILES_DIR, SESSIONS_DIR
from glob import glob

USERS_FILE = os.path.join(FILES_DIR, "users.txt")
MEDIA_FILE = os.path.join(FILES_DIR, "media.jpg")
MESSAGE_FILE = os.path.join(FILES_DIR, "message.txt")

API_ID = 15131315
API_HASH = 'a1940ca7ce02955287a4c6742ad21f27'

async def send_from_session(session_path, users, message, media_path=None):
    name = os.path.splitext(os.path.basename(session_path))[0]
    try:
        client = TelegramClient(session_path, API_ID, API_HASH)
        await client.start()
        for user in users:
            try:
                if media_path:
                    await client.send_file(user, media_path, caption=message)
                else:
                    await client.send_message(user, message)
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[{name}] ❌ Не удалось отправить {user}: {e}")
        await client.disconnect()
        print(f"[{name}] ✅ Готово.")
    except Exception as e:
        print(f"[{name}] ❌ Ошибка клиента: {e}")

async def main():
    if not os.path.exists(USERS_FILE):
        print("❌ Файл users.txt не найден")
        return

    with open(USERS_FILE, encoding='utf-8') as f:
        users = [line.strip() for line in f if line.strip()]

    message = ""
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, encoding='utf-8') as f:
            message = f.read().strip()

    media = MEDIA_FILE if os.path.exists(MEDIA_FILE) else None

    sessions = glob(os.path.join(SESSIONS_DIR, "*.session"))
    print(f"📨 Найдено {len(sessions)} аккаунтов, начинаю рассылку...")

    tasks = [send_from_session(sess, users, message, media) for sess in sessions]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())