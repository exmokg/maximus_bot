import os
import asyncio
from telethon import TelegramClient, errors

API_ID = 15131315
API_HASH = "a1940ca7ce02955287a4c6742ad21f27"
SESSIONS_DIR = "sessions"

async def check_and_unblock(session_path):
    client = TelegramClient(session_path, API_ID, API_HASH)
    try:
        await client.start()
        if not await client.is_user_authorized():
            print(f"[{session_path}] ❌ Не авторизован")
            return
        print(f"[{session_path}] ✅ Аккаунт в порядке")
    except Exception as e:
        print(f"[{session_path}] ⚠️ Ошибка: {e}")
    finally:
        await client.disconnect()

async def main():
    sessions = [os.path.join(SESSIONS_DIR, f) for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")]
    await asyncio.gather(*(check_and_unblock(sess) for sess in sessions))

if __name__ == "__main__":
    asyncio.run(main())