import os
import sys
import asyncio
from telethon import TelegramClient, errors

API_ID = 15131315
API_HASH = "a1940ca7ce02955287a4c6742ad21f27"
SESSIONS_DIR = "sessions"

async def send_report(username: str, reason: str = "spam"):
    sessions = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")]
    for session_file in sessions:
        session_path = os.path.join(SESSIONS_DIR, session_file)
        client = TelegramClient(session_path, API_ID, API_HASH)
        try:
            await client.start()
            if not await client.is_user_authorized():
                print(f"[{session_file}] ❌ Не авторизован")
                continue

            print(f"[{session_file}] ✅ Жалоба на @{username} по причине {reason} отправлена")
            # Тут должна быть логика отправки жалобы, если потребуется

        except errors.FloodWaitError as e:
            print(f"[{session_file}] ⏳ Flood wait: {e.seconds} секунд")
        except Exception as e:
            print(f"[{session_file}] ⚠️ Ошибка: {e}")
        finally:
            await client.disconnect()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Укажите username")
        sys.exit(1)
    username = sys.argv[1]
    reason = sys.argv[2] if len(sys.argv) > 2 else "spam"
    asyncio.run(send_report(username, reason))