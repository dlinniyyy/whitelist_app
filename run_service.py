from waitress import serve
from app_production import app
import logging

if __name__ == '__main__':
    print("=== Whitelist Application ===")
    print("Production сервер запущен!")
    print("Основная страница: http://localhost:5001")
    print("Администрирование: http://localhost:5001/admin")
    print("Логи: logs/whitelist.log")
    print("Для остановки: Ctrl+C")

    serve(app, host='0.0.0.0', port=5001, threads=4)