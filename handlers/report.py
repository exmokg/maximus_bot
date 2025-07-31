import asyncio
import os
from aiogram import types, Router
from config import SCRIPTS_DIR, FILES_DIR

report_router = Router()
REPORT_SCRIPT = os.path.join(SCRIPTS_DIR, "report_sender.py")
TARGET_FILE = os.path.join(FILES_DIR, "target.txt")

pending_targets = set()

async def run_script(script_path: str, target: str) -> tuple[str, str]:
    proc = await asyncio.create_subprocess_exec(
        "python3", script_path, target,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    return stdout.decode(), stderr.decode()

@report_router.callback_query(lambda c: c.data == "report" or c.data == "report_start")
async def ask_target(call: types.CallbackQuery):
    pending_targets.add(call.from_user.id)
    await call.message.answer("⚠️ Введите username цели (без @), например: <code>OperKS247</code>")

@report_router.message(lambda msg: msg.text is not None)
async def receive_target(message: types.Message):
    if message.from_user.id not in pending_targets:
        return

    target = message.text.strip().lstrip('@')
    if not target.isalnum():
        return await message.answer("❌ Некорректный username. Только буквы и цифры.")

    pending_targets.remove(message.from_user.id)

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(target)

    await message.answer(f"🎯 Цель установлена: <b>@{target}</b>\n🚀 Начинаю отправку жалоб...")

    stdout, stderr = await run_script(REPORT_SCRIPT, target)

    text = f"<b>📣 Жалобы отправлены.</b>\n"
    if stdout:
        text += f"\n<pre>{stdout.strip()}</pre>"
    if stderr:
        text += f"\n⚠️ <pre>{stderr.strip()}</pre>"

    await message.answer(text[:4096])