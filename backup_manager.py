import os
import sys
from app_production import get_backup_info, restore_from_backup, create_backup


def show_backup_menu():
    """Меню управления бэкапами"""
    while True:
        print("\n" + "=" * 50)
        print("        УПРАВЛЕНИЕ БЭКАПАМИ")
        print("=" * 50)

        backup_info = get_backup_info()
        print(f"Всего бэкапов: {backup_info['count']}")
        print("\nСписок бэкапов:")
        for i, backup in enumerate(backup_info['backups'], 1):
            print(f"{i}. {backup['filename']} ({backup['size']} bytes) - {backup['modified']}")

        print("\nДоступные действия:")
        print("1 - Создать новый бэкап")
        print("2 - Восстановить из бэкапа")
        print("3 - Показать информацию о бэкапах")
        print("4 - Выйти")

        choice = input("\nВыберите действие: ").strip()

        if choice == '1':
            create_new_backup()
        elif choice == '2':
            restore_backup_menu(backup_info)
        elif choice == '3':
            show_backup_info(backup_info)
        elif choice == '4':
            break
        else:
            print("Неверный выбор!")


def create_new_backup():
    """Создание нового бэкапа"""
    print("\nСоздание нового бэкапа...")
    if create_backup():
        print("✅ Бэкап создан успешно!")
    else:
        print("❌ Ошибка создания бэкапа!")


def restore_backup_menu(backup_info):
    """Меню восстановления из бэкапа"""
    if backup_info['count'] == 0:
        print("Нет доступных бэкапов для восстановления")
        return

    print("\nВыберите бэкап для восстановления:")
    for i, backup in enumerate(backup_info['backups'], 1):
        print(f"{i}. {backup['filename']} - {backup['modified']}")

    try:
        choice = int(input("\nНомер бэкапа: ")) - 1
        if 0 <= choice < len(backup_info['backups']):
            selected_backup = backup_info['backups'][choice]['path']

            confirm = input(
                f"Вы уверены, что хотите восстановить данные из {backup_info['backups'][choice]['filename']}? (y/N): ")
            if confirm.lower() == 'y':
                print("Восстановление данных...")
                if restore_from_backup(selected_backup):
                    print("✅ Данные успешно восстановлены!")
                else:
                    print("❌ Ошибка восстановления данных!")
        else:
            print("Неверный номер бэкапа!")
    except ValueError:
        print("Неверный ввод!")


def show_backup_info(backup_info):
    """Показать подробную информацию о бэкапах"""
    print("\n" + "=" * 50)
    print("        ИНФОРМАЦИЯ О БЭКАПАХ")
    print("=" * 50)
    print(f"Всего бэкапов: {backup_info['count']}")
    print(f"Директория бэкапов: backups/")

    total_size = sum(backup['size'] for backup in backup_info['backups'])
    print(f"Общий размер: {total_size} bytes ({total_size / 1024 / 1024:.2f} MB)")

    if backup_info['count'] > 0:
        oldest = backup_info['backups'][-1]['modified']
        newest = backup_info['backups'][0]['modified']
        print(f"Самый старый бэкап: {oldest}")
        print(f"Самый новый бэкап: {newest}")


if __name__ == '__main__':
    show_backup_menu()