import os
import asyncio
from telethon import TelegramClient, errors
from glob import glob

SESSIONS_DIR = "sessions"

async def check_session(path):
    name = os.path.splitext(os.path.basename(path))[0]
    try:
        client = TelegramClient(path, 15131315, 'a1940ca7ce02955287a4c6742ad21f27')
        await client.connect()
        me = await client.get_me()
        status = "✅ Работает"
        await client.disconnect()
    except errors.FloodWaitError as e:
        status = f"⚠️ FloodWait {e.seconds}s"
    except errors.UserDeactivatedBanError:
        status = "❌ Заблокирован"
    except Exception as e:
        status = f"❌ Ошибка: {e}"
    print(f"{name}: {status}")

async def main():
    sessions = glob(f"{SESSIONS_DIR}/*.session")
    print(f"🔍 Найдено {len(sessions)} сессий. Начинаю проверку...")
    tasks = [check_session(sess) for sess in sessions]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())