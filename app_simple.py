from flask import Flask, render_template, request, jsonify
import json
import os
import logging

# Базовая настройка Flask
app = Flask(__name__)

# Файл для хранения данных
DATA_FILE = 'data/resources.json'


def log_message(message):
    """Простое логирование"""
    try:
        log_path = os.path.join(os.path.dirname(__file__), "app_log.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
    except:
        pass


def load_resources():
    """Упрощенная загрузка ресурсов"""
    try:
        log_message("Загрузка ресурсов...")
        if not os.path.exists(DATA_FILE):
            return {"groups": []}

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log_message(f"Ошибка загрузки: {e}")
        return {"groups": []}


@app.route('/')
def index():
    """Основная страница"""
    try:
        data = load_resources()
        return render_template('index.html', groups=data.get('groups', []))
    except Exception as e:
        return f"Ошибка: {e}", 500


@app.route('/admin')
def admin():
    """Страница администрирования"""
    try:
        data = load_resources()
        return render_template('admin.html', groups=data.get('groups', []))
    except Exception as e:
        return f"Ошибка: {e}", 500


# Простые API endpoints
@app.route('/api/add_group', methods=['POST'])
def add_group():
    try:
        data = load_resources()
        group_name = request.json.get('name', '').strip()

        if not group_name:
            return jsonify({"success": False, "message": "Пустое название"})

        new_group = {"name": group_name, "resources": []}
        data['groups'].append(new_group)

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return jsonify({"success": True, "message": "Группа добавлена"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


if __name__ == '__main__':
    log_message("Запуск простого сервера")
    from waitress import serve

    serve(app, host='127.0.0.1', port=5001, threads=2)