# /root/bot_manager/scripts/report_sender.py
import os
import sys
import asyncio
from telethon import TelegramClient, errors

API_ID = 15131315
API_HASH = "a1940ca7ce02955287a4c6742ad21f27"
SESSIONS_DIR = "/root/bot_manager/sessions"

async def send_report(username: str, reason: str):
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
    if len(sys.argv) < 3:
        print("❌ Укажите username и reason")
        sys.exit(1)
    asyncio.run(send_report(sys.argv[1], sys.argv[2]))