from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

# Файл для хранения данных
DATA_FILE = 'data/resources.json'


def load_resources():
    """Загрузка ресурсов из JSON файла"""
    # Создаем директорию если ее нет
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    if not os.path.exists(DATA_FILE):
        # Создаем начальные данные если файла нет
        return create_initial_data()

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                # Если файл пустой, создаем начальные данные
                return create_initial_data()
            data = json.loads(content)
            # Пересчитываем номера при загрузке
            return renumber_resources(data)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Ошибка загрузки JSON: {e}")
        # Если файл поврежден, создаем заново
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
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False


def renumber_resources(data):
    """Перенумеровывает все ресурсы последовательно"""
    counter = 1
    for group in data['groups']:
        for resource in group['resources']:
            resource['number'] = counter
            counter += 1
    return data


@app.route('/')
def index():
    """Основная страница с ресурсами"""
    try:
        data = load_resources()
        return render_template('index.html', groups=data['groups'])
    except Exception as e:
        return f"Ошибка загрузки данных: {e}", 500


@app.route('/admin')
def admin():
    """Страница администрирования"""
    try:
        data = load_resources()
        return render_template('admin.html', groups=data['groups'])
    except Exception as e:
        return f"Ошибка загрузки данных: {e}", 500


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


if __name__ == '__main__':
    # Создаем данные при первом запуске
    load_resources()
    print("Приложение запущено!")
    print("Основная страница: http://localhost:5001")
    print("Администрирование: http://localhost:5001/admin")
    app.run(host='0.0.0.0', port=5001, debug=True)