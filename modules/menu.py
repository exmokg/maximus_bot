import asyncio

from modules.spambot import unfreeze_accounts
from modules.mass_report import mass_report
from modules.mass_mailing import mass_mailing
from modules.account_status import check_accounts
from modules.group_joiner import join_groups
from modules.group_parser import parse_group_members, parse_hidden_group
from modules.export import export_users

async def run_menu():
    while True:
        print("\n--- Telegram Bot Automation Menu ---")
        print("1. Разморозка аккаунтов через SpamBot")
        print("2. Массовые жалобы")
        print("3. Массовая рассылка")
        print("4. Проверка статуса аккаунтов")
        print("5. Джойнер в группы")
        print("6. Парсер участников группы")
        print("7. Парсер скрытых групп")
        print("8. Экспорт данных")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            await unfreeze_accounts()
        elif choice == '2':
            await mass_report()
        elif choice == '3':
            await mass_mailing()
        elif choice == '4':
            await check_accounts()
        elif choice == '5':
            await join_groups()
        elif choice == '6':
            await parse_group_members()
        elif choice == '7':
            await parse_hidden_group()
        elif choice == '8':
            await export_users()
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")
        await asyncio.sleep(1)