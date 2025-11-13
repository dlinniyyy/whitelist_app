from flask import Flask, render_template, request, jsonify
import json
import os
import logging
import shutil
import datetime
from logging.handlers import RotatingFileHandler


# Настройка логирования
def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    file_handler = RotatingFileHandler(
        'logs/whitelist.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Whitelist application startup')


app = Flask(__name__)

# Файл для хранения данных
DATA_FILE = 'data/resources.json'
BACKUP_DIR = 'backups'


def create_backup():
    """Создание бэкапа файла данных"""
    try:
        if not os.path.exists(DATA_FILE):
            app.logger.warning("Файл данных не существует, бэкап не создан")
            return False

        # Создаем директорию для бэкапов если ее нет
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
            app.logger.info(f"Создана директория для бэкапов: {BACKUP_DIR}")

        # Генерируем имя файла с timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"resources_backup_{timestamp}.json")

        # Копируем файл
        shutil.copy2(DATA_FILE, backup_file)

        # Также создаем симлинк на последний бэкап
        latest_backup = os.path.join(BACKUP_DIR, "resources_backup_latest.json")
        if os.path.exists(latest_backup):
            os.remove(latest_backup)
        shutil.copy2(DATA_FILE, latest_backup)

        app.logger.info(f"Создан бэкап: {backup_file}")

        # Очищаем старые бэкапы (оставляем последние 10)
        cleanup_old_backups()

        return True

    except Exception as e:
        app.logger.error(f"Ошибка создания бэкапа: {e}")
        return False


def cleanup_old_backups(max_backups=10):
    """Очистка старых бэкапов, оставляет только последние max_backups"""
    try:
        if not os.path.exists(BACKUP_DIR):
            return

        # Получаем все файлы бэкапов
        backup_files = []
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith("resources_backup_") and filename.endswith(".json") and "latest" not in filename:
                filepath = os.path.join(BACKUP_DIR, filename)
                if os.path.isfile(filepath):
                    backup_files.append((filepath, os.path.getmtime(filepath)))

        # Сортируем по дате изменения (старые первыми)
        backup_files.sort(key=lambda x: x[1])

        # Удаляем старые бэкапы
        if len(backup_files) > max_backups:
            files_to_delete = backup_files[:len(backup_files) - max_backups]
            for filepath, _ in files_to_delete:
                os.remove(filepath)
                app.logger.info(f"Удален старый бэкап: {filepath}")

    except Exception as e:
        app.logger.error(f"Ошибка очистки старых бэкапов: {e}")


def restore_from_backup(backup_file=None):
    """Восстановление данных из бэкапа"""
    try:
        if backup_file is None:
            backup_file = os.path.join(BACKUP_DIR, "resources_backup_latest.json")

        if not os.path.exists(backup_file):
            app.logger.error(f"Файл бэкапа не найден: {backup_file}")
            return False

        shutil.copy2(backup_file, DATA_FILE)
        app.logger.info(f"Данные восстановлены из бэкапа: {backup_file}")
        return True

    except Exception as e:
        app.logger.error(f"Ошибка восстановления из бэкапа: {e}")
        return False


def get_backup_info():
    """Получение информации о бэкапах"""
    try:
        if not os.path.exists(BACKUP_DIR):
            return {"count": 0, "backups": []}

        backups = []
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith("resources_backup_") and filename.endswith(".json"):
                filepath = os.path.join(BACKUP_DIR, filename)
                if os.path.isfile(filepath):
                    stat = os.stat(filepath)
                    backups.append({
                        "filename": filename,
                        "path": filepath,
                        "size": stat.st_size,
                        "modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    })

        # Сортируем по дате изменения (новые первыми)
        backups.sort(key=lambda x: x["modified"], reverse=True)

        return {
            "count": len(backups),
            "backups": backups
        }

    except Exception as e:
        app.logger.error(f"Ошибка получения информации о бэкапах: {e}")
        return {"count": 0, "backups": []}


def load_resources():
    """Загрузка ресурсов из JSON файла"""
    # Создаем директорию если ее нет
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    if not os.path.exists(DATA_FILE):
        # Создаем начальные данные если файла нет
        app.logger.info("Файл данных не найден, создание начальных данных")
        return create_initial_data()

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                # Если файл пустой, создаем начальные данные
                app.logger.warning("Файл данных пуст, создание начальных данных")
                return create_initial_data()
            data = json.loads(content)
            # Пересчитываем номера при загрузке
            return renumber_resources(data)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        app.logger.error(f"Ошибка загрузки JSON: {e}")
        # Пытаемся восстановить из бэкапа
        app.logger.info("Попытка восстановления из бэкапа...")
        if restore_from_backup():
            return load_resources()
        else:
            # Если файл поврежден, создаем заново
            app.logger.info("Создание новых начальных данных")
            return create_initial_data()


def create_initial_data():
    """Создает начальные данные со всеми ресурсами из HTML"""
    initial_data = {
        "groups": [
            {
                "name": "Справочники",
                "resources": [
                    {
                        "number": 1,
                        "logo": "https://www.rlsnet.ru/favicon.ico",
                        "url": "https://www.rlsnet.ru",
                        "description": "Регистр лекарственных средств России - информация о лекарственных препаратах"
                    },
                    {
                        "number": 2,
                        "logo": "https://www.vidal.ru/favicon.ico",
                        "url": "https://www.vidal.ru",
                        "description": "Справочник лекарственных препаратов Vidal"
                    },
                    {
                        "number": 3,
                        "logo": "http://web.ref003.ru/images/favicon.ico",
                        "url": "http://web.ref003.ru/",
                        "description": "Справочник аптек - ГУП РО Фармацевтический центр"
                    }
                ]
            },
            {
                "name": "Калькуляторы",
                "resources": [
                    {
                        "number": 4,
                        "logo": "https://www.rlsnet.ru/favicon.ico",
                        "url": "https://www.rlsnet.ru/med-calculators",
                        "description": "Медицинские калькуляторы на RLSnet - расчет доз, индексов и других медицинских показателей"
                    }
                ]
            },
            {
                "name": "Другие информационные системы",
                "resources": [
                    {
                        "number": 5,
                        "logo": "https://rostov-tfoms.ru/favicon.ico",
                        "url": "https://rostov-tfoms.ru",
                        "description": "Территориальный фонд обязательного медицинского страхования Ростовской области"
                    },
                    {
                        "number": 6,
                        "logo": "https://edu.rosminzdrav.ru/favicon.ico",
                        "url": "https://edu.rosminzdrav.ru",
                        "description": "Образовательный портал Министерства здравоохранения РФ"
                    },
                    {
                        "number": 7,
                        "logo": "https://tmk.minzdrav.gov.ru/favicon.ico",
                        "url": "https://tmk.minzdrav.gov.ru",
                        "description": "Телемедицинская консультация Министерства здравоохранения РФ"
                    },
                    {
                        "number": 8,
                        "logo": "https://vimis.egisz.rosminzdrav.ru/favicon.ico",
                        "url": "https://vimis.egisz.rosminzdrav.ru",
                        "description": "Ведомственная интегрированная медицинская информационная система ЕГИСЗ"
                    },
                    {
                        "number": 9,
                        "logo": "https://orph.egisz.rosminzdrav.ru/favicon.ico",
                        "url": "https://orph.egisz.rosminzdrav.ru",
                        "description": "Федеральный регистр лиц, страдающих орфанными заболеваниями"
                    },
                    {
                        "number": 10,
                        "logo": "https://cr.minzdrav.gov.ru/favicon.ico",
                        "url": "https://cr.minzdrav.gov.ru",
                        "description": "Рубрикатор Клинических рекомендаций"
                    },
                    {
                        "number": 11,
                        "logo": "https://portalmr.egisz.rosminzdrav.ru/favicon.ico",
                        "url": "https://portalmr.egisz.rosminzdrav.ru",
                        "description": "ФРМР Федеральный регистр медицинских работников"
                    },
                    {
                        "number": 12,
                        "logo": "https://lkmr.egisz.rosminzdrav.ru/favicon.ico",
                        "url": "https://lkmr.egisz.rosminzdrav.ru",
                        "description": "ЛК ФРМР - Личный кабинет медицинского работника"
                    },
                    {
                        "number": 13,
                        "logo": "https://diaregistry.ru/favicon.ico",
                        "url": "https://diaregistry.ru",
                        "description": "Федеральный регистр сахарного диабета"
                    },
                    {
                        "number": 14,
                        "logo": "https://www.gosuslugi.ru/favicon.ico",
                        "url": "https://www.gosuslugi.ru",
                        "description": "Портал государственных услуг Российской Федерации"
                    },
                    {
                        "number": 15,
                        "logo": "https://grls.rosminzdrav.ru/favicon.ico",
                        "url": "https://grls.rosminzdrav.ru",
                        "description": "Государственный реестр лекарственных средств"
                    },
                    {
                        "number": 16,
                        "logo": "https://roszdravnadzor.gov.ru/favicon.ico",
                        "url": "https://roszdravnadzor.gov.ru/",
                        "description": "Федеральная служба по надзору в сфере здравоохранения"
                    }
                ]
            },
            {
                "name": "Честный знак",
                "resources": [
                    {
                        "number": 17,
                        "logo": "https://mdlp.crpt.ru/favicon.ico",
                        "url": "https://mdlp.crpt.ru",
                        "description": "Мониторинг движения лекарственных препаратов"
                    },
                    {
                        "number": 18,
                        "logo": "https://честныйзнак.рф/favicon.ico",
                        "url": "https://честныйзнак.рф",
                        "description": "Официальный портал системы маркировки \"Честный знак\""
                    },
                    {
                        "number": 19,
                        "logo": "https://support.crpt.ru/ws-crpt-login/images/favicon.png",
                        "url": "https://support.crpt.ru",
                        "description": "Техническая поддержка системы \"Честный знак\""
                    },
                    {
                        "number": 20,
                        "logo": "https://markirovka.crpt.ru/favicon.ico",
                        "url": "https://markirovka.crpt.ru",
                        "description": "Личный кабинет системы \"Честный знак\""
                    }
                ]
            },
            {
                "name": "Другие медицинские организации",
                "resources": [
                    {
                        "number": 21,
                        "logo": "https://www.center-zdorovie.ru/sites/all/themes/health/images/2022_head_logo_kdc_1.png",
                        "url": "https://center-zdorovie.ru",
                        "description": "ГБУ РО «КДЦ «Здоровье» в г. Ростове-на-Дону"
                    },
                    {
                        "number": 22,
                        "logo": "https://rokdc.ru/favicon.ico",
                        "url": "https://rokdc.ru",
                        "description": "Областной консультативно-диагностический центр"
                    },
                    {
                        "number": 23,
                        "logo": "https://legeartis-don.ru/favicon.ico",
                        "url": "https://legeartis-don.ru",
                        "description": "Медицинский центр \"Леге Артис\" в Ростове-на-Дону"
                    }
                ]
            }
        ]
    }

    save_resources(initial_data)
    return initial_data


def save_resources(data):
    """Сохранение ресурсов в JSON файл"""
    try:
        # Создаем бэкап перед сохранением
        create_backup()

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        app.logger.info('Данные успешно сохранены')
        return True
    except Exception as e:
        app.logger.error(f"Ошибка сохранения: {e}")
        return False


def renumber_resources(data):
    """Перенумеровывает все ресурсы последовательно"""
    counter = 1
    for group in data['groups']:
        for resource in group['resources']:
            resource['number'] = counter
            counter += 1
    return data


# API endpoints для управления бэкапами
@app.route('/api/backup/create', methods=['POST'])
def api_create_backup():
    """Ручное создание бэкапа"""
    try:
        if create_backup():
            return jsonify({"success": True, "message": "Бэкап создан успешно"})
        else:
            return jsonify({"success": False, "message": "Ошибка создания бэкапа"})
    except Exception as e:
        app.logger.error(f"Ошибка API создания бэкапа: {e}")
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"})


@app.route('/api/backup/list', methods=['GET'])
def api_list_backups():
    """Получение списка бэкапов"""
    try:
        backup_info = get_backup_info()
        return jsonify({"success": True, "data": backup_info})
    except Exception as e:
        app.logger.error(f"Ошибка API списка бэкапов: {e}")
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"})


@app.route('/api/backup/restore', methods=['POST'])
def api_restore_backup():
    """Восстановление из бэкапа"""
    try:
        backup_file = request.json.get('backup_file')

        if restore_from_backup(backup_file):
            return jsonify({"success": True, "message": "Данные восстановлены из бэкапа"})
        else:
            return jsonify({"success": False, "message": "Ошибка восстановления из бэкапа"})
    except Exception as e:
        app.logger.error(f"Ошибка API восстановления бэкапа: {e}")
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"})


@app.route('/')
def index():
    """Основная страница с ресурсами"""
    try:
        data = load_resources()
        return render_template('index.html', groups=data['groups'])
    except Exception as e:
        app.logger.error(f"Ошибка загрузки данных: {e}")
        return "Ошибка загрузки данных", 500


@app.route('/admin')
def admin():
    """Страница администрирования"""
    try:
        data = load_resources()
        return render_template('admin.html', groups=data['groups'])
    except Exception as e:
        app.logger.error(f"Ошибка загрузки данных: {e}")
        return "Ошибка загрузки данных", 500


# Все API endpoints остаются такими же как в предыдущей версии
# [здесь должны быть все ваши API endpoints из предыдущего кода]
@app.route('/api/add_group', methods=['POST'])
def add_group():
    """Добавление новой группы"""
    try:
        data = load_resources()
        group_name = request.json.get('name')

        if not group_name or not group_name.strip():
            return jsonify({"success": False, "message": "Не указано название группы"})

        group_name = group_name.strip()

        # Проверяем, нет ли уже группы с таким названием
        for group in data['groups']:
            if group['name'].lower() == group_name.lower():
                return jsonify({"success": False, "message": "Группа с таким названием уже существует"})

        new_group = {
            "name": group_name,
            "resources": []
        }
        data['groups'].append(new_group)

        if save_resources(data):
            return jsonify({"success": True, "message": "Группа добавлена"})
        else:
            return jsonify({"success": False, "message": "Ошибка сохранения данных"})

    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"})


@app.route('/api/edit_group', methods=['POST'])
def edit_group():
    """Редактирование группы"""
    try:
        data = load_resources()
        group_index = request.json.get('group_index')
        new_name = request.json.get('name')

        if group_index is None or not new_name or not new_name.strip():
            return jsonify({"success": False, "message": "Не указаны данные для редактирования"})

        try:
            group_index = int(group_index)
            if group_index < 0 or group_index >= len(data['groups']):
                return jsonify({"success": False, "message": "Неверный индекс группы"})

            new_name = new_name.strip()

            # Проверяем, нет ли уже группы с таким названием (кроме текущей)
            for i, group in enumerate(data['groups']):
                if i != group_index and group['name'].lower() == new_name.lower():
                    return jsonify({"success": False, "message": "Группа с таким названием уже существует"})

            data['groups'][group_index]['name'] = new_name

            if save_resources(data):
                return jsonify({"success": True, "message": "Группа обновлена"})
            else:
                return jsonify({"success": False, "message": "Ошибка сохранения данных"})

        except (ValueError, IndexError):
            return jsonify({"success": False, "message": "Неверный индекс группы"})

    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"})


@app.route('/api/add_resource', methods=['POST'])
def add_resource():
    """Добавление нового ресурса"""
    try:
        data = load_resources()

        group_index = request.json.get('group_index')
        logo = request.json.get('logo', '').strip()
        url = request.json.get('url', '').strip()
        description = request.json.get('description', '').strip()

        if group_index is None or not url or not description:
            return jsonify({"success": False, "message": "Не все обязательные поля заполнены"})

        try:
            group_index = int(group_index)
            if group_index < 0 or group_index >= len(data['groups']):
                return jsonify({"success": False, "message": "Неверный индекс группы"})

            # Добавляем ресурс
            new_resource = {
                "number": 0,  # Временно 0, пересчитается при сохранении
                "logo": logo,
                "url": url,
                "description": description
            }

            data['groups'][group_index]['resources'].append(new_resource)
            # Перенумеровываем все ресурсы
            data = renumber_resources(data)

            if save_resources(data):
                return jsonify({"success": True, "message": "Ресурс добавлен"})
            else:
                return jsonify({"success": False, "message": "Ошибка сохранения данных"})

        except (ValueError, IndexError):
            return jsonify({"success": False, "message": "Неверный индекс группы"})

    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"})


@app.route('/api/edit_resource', methods=['POST'])
def edit_resource():
    """Редактирование ресурса"""
    try:
        data = load_resources()

        group_index = request.json.get('group_index')
        resource_index = request.json.get('resource_index')
        logo = request.json.get('logo', '').strip()
        url = request.json.get('url', '').strip()
        description = request.json.get('description', '').strip()

        if group_index is None or resource_index is None or not url or not description:
            return jsonify({"success": False, "message": "Не все обязательные поля заполнены"})

        try:
            group_index = int(group_index)
            resource_index = int(resource_index)

            if group_index < 0 or group_index >= len(data['groups']):
                return jsonify({"success": False, "message": "Неверный индекс группы"})

            if resource_index < 0 or resource_index >= len(data['groups'][group_index]['resources']):
                return jsonify({"success": False, "message": "Неверный индекс ресурса"})

            # Обновляем ресурс
            resource = data['groups'][group_index]['resources'][resource_index]
            resource['logo'] = logo
            resource['url'] = url
            resource['description'] = description

            if save_resources(data):
                return jsonify({"success": True, "message": "Ресурс обновлен"})
            else:
                return jsonify({"success": False, "message": "Ошибка сохранения данных"})

        except (ValueError, IndexError):
            return jsonify({"success": False, "message": "Неверные индексы"})

    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"})


@app.route('/api/move_resource', methods=['POST'])
def move_resource():
    """Перемещение ресурса вверх/вниз в группе"""
    try:
        data = load_resources()

        group_index = request.json.get('group_index')
        resource_index = request.json.get('resource_index')
        direction = request.json.get('direction')  # 'up' или 'down'

        if group_index is None or resource_index is None or direction not in ['up', 'down']:
            return jsonify({"success": False, "message": "Неверные параметры"})

        try:
            group_index = int(group_index)
            resource_index = int(resource_index)

            if group_index < 0 or group_index >= len(data['groups']):
                return jsonify({"success": False, "message": "Неверный индекс группы"})

            resources = data['groups'][group_index]['resources']

            if resource_index < 0 or resource_index >= len(resources):
                return jsonify({"success": False, "message": "Неверный индекс ресурса"})

            if direction == 'up' and resource_index > 0:
                # Перемещаем вверх
                resources[resource_index], resources[resource_index - 1] = resources[resource_index - 1], resources[
                    resource_index]
            elif direction == 'down' and resource_index < len(resources) - 1:
                # Перемещаем вниз
                resources[resource_index], resources[resource_index + 1] = resources[resource_index + 1], resources[
                    resource_index]
            else:
                return jsonify({"success": False, "message": "Невозможно переместить ресурс"})

            # Перенумеровываем все ресурсы
            data = renumber_resources(data)

            if save_resources(data):
                return jsonify({"success": True, "message": "Ресурс перемещен"})
            else:
                return jsonify({"success": False, "message": "Ошибка сохранения данных"})

        except (ValueError, IndexError):
            return jsonify({"success": False, "message": "Неверные индексы"})

    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"})


@app.route('/api/delete_resource', methods=['POST'])
def delete_resource():
    """Удаление ресурса"""
    try:
        data = load_resources()

        group_index = request.json.get('group_index')
        resource_index = request.json.get('resource_index')

        if group_index is None or resource_index is None:
            return jsonify({"success": False, "message": "Не указаны индексы"})

        try:
            group_index = int(group_index)
            resource_index = int(resource_index)

            if group_index < 0 or group_index >= len(data['groups']):
                return jsonify({"success": False, "message": "Неверный индекс группы"})

            if resource_index < 0 or resource_index >= len(data['groups'][group_index]['resources']):
                return jsonify({"success": False, "message": "Неверный индекс ресурса"})

            del data['groups'][group_index]['resources'][resource_index]
            # Перенумеровываем после удаления
            data = renumber_resources(data)

            if save_resources(data):
                return jsonify({"success": True, "message": "Ресурс удален"})
            else:
                return jsonify({"success": False, "message": "Ошибка сохранения данных"})

        except (ValueError, IndexError):
            return jsonify({"success": False, "message": "Неверные индексы"})

    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"})


@app.route('/api/delete_group', methods=['POST'])
def delete_group():
    """Удаление группы"""
    try:
        data = load_resources()

        group_index = request.json.get('group_index')

        if group_index is None:
            return jsonify({"success": False, "message": "Не указан индекс группы"})

        try:
            group_index = int(group_index)

            if group_index < 0 or group_index >= len(data['groups']):
                return jsonify({"success": False, "message": "Неверный индекс группы"})

            # Проверяем, что группа пуста
            if data['groups'][group_index]['resources']:
                return jsonify({"success": False, "message": "Нельзя удалить группу с ресурсами"})

            del data['groups'][group_index]

            if save_resources(data):
                return jsonify({"success": True, "message": "Группа удалена"})
            else:
                return jsonify({"success": False, "message": "Ошибка сохранения данных"})

        except (ValueError, IndexError):
            return jsonify({"success": False, "message": "Неверный индекс группы"})

    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка сервера: {str(e)}"})
# ... (все ваши API endpoints остаются без изменений)

if __name__ == '__main__':
    setup_logging()
    # Создаем бэкап при запуске
    create_backup()
    # Создаем данные при первом запуске
    load_resources()

    from waitress import serve

    app.logger.info('Запуск production сервера на порту 5000')
    print("=== Whitelist Application ===")
    print("Production сервер запущен!")
    print("Основная страница: http://localhost:5000")
    print("Администрирование: http://localhost:5000/admin")
    print("Логи: logs/whitelist.log")
    print("Бэкапы: backups/")
    print("Для остановки: Ctrl+C")

    serve(app, host='0.0.0.0', port=5000, threads=4)