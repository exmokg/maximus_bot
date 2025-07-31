import os
import asyncio
from aiogram import types, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from config import FILES_DIR, SCRIPTS_DIR

broadcast_router = Router()
BROADCAST_SCRIPT = os.path.join(SCRIPTS_DIR, "send_media.py")

class BroadcastSteps(StatesGroup):
    waiting_for_users = State()
    waiting_for_proxies = State()
    waiting_for_photo = State()
    waiting_for_text = State()
    confirm_preview = State()

@broadcast_router.callback_query(F.data == "broadcast")
async def start_broadcast_process(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("📎 Пожалуйста, отправьте файл <b>users.txt</b> (получатели).")
    await state.set_state(BroadcastSteps.waiting_for_users)

@broadcast_router.message(BroadcastSteps.waiting_for_users, F.document)
async def receive_users(message: types.Message, state: FSMContext):
    if message.document.file_name != "users.txt":
        return await message.answer("❌ Ожидался файл с именем <code>users.txt</code>.")
    dest = os.path.join(FILES_DIR, "users.txt")
    await message.document.download(destination=dest)
    await message.answer("✅ Файл users.txt получен. Теперь отправьте файл <b>proxies.txt</b>.")
    await state.set_state(BroadcastSteps.waiting_for_proxies)

@broadcast_router.message(BroadcastSteps.waiting_for_proxies, F.document)
async def receive_proxies(message: types.Message, state: FSMContext):
    if message.document.file_name != "proxies.txt":
        return await message.answer("❌ Ожидался файл <code>proxies.txt</code>.")
    dest = os.path.join(FILES_DIR, "proxies.txt")
    await message.document.download(destination=dest)
    await message.answer("🖼 Теперь отправьте фото (jpg/png), которое будет прикреплено к рассылке.")
    await state.set_state(BroadcastSteps.waiting_for_photo)

@broadcast_router.message(BroadcastSteps.waiting_for_photo, F.photo)
async def receive_photo(message: types.Message, state: FSMContext):
    dest = os.path.join(FILES_DIR, "media.jpg")
    await message.photo[-1].download(destination=dest)
    await message.answer("✏️ Теперь отправьте текст рассылки.")
    await state.set_state(BroadcastSteps.waiting_for_text)

@broadcast_router.message(BroadcastSteps.waiting_for_text, F.text)
async def receive_text(message: types.Message, state: FSMContext):
    text_file = os.path.join(FILES_DIR, "message.txt")
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(message.text)

    photo = FSInputFile(os.path.join(FILES_DIR, "media.jpg"))
    preview_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Приступить", callback_data="start_mass_send")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_mass_send")]
    ])

    await message.answer_photo(photo, caption=message.text, reply_markup=preview_kb)
    await state.set_state(BroadcastSteps.confirm_preview)

@broadcast_router.callback_query(F.data == "start_mass_send")
async def execute_broadcast(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("🚀 Рассылка началась...")

    proc = await asyncio.create_subprocess_exec(
        "python3", BROADCAST_SCRIPT,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    output = "<b>📤 Рассылка завершена.</b>\n"
    if stdout:
        output += f"<pre>{stdout.decode().strip()}</pre>"
    if stderr:
        output += f"\n⚠️ <pre>{stderr.decode().strip()}</pre>"

    await call.message.answer(output[:4096])
    await state.clear()

@broadcast_router.callback_query(F.data == "cancel_mass_send")
async def cancel_broadcast(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("❌ Рассылка отменена.")
    await state.clear()