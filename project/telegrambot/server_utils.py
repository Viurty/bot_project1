import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading


def start_local_server(directory, port=8000):
    """
    Запускает локальный веб-сервер для раздачи файлов из указанной директории.

    :param directory: Папка, из которой раздаются файлы.
    :param port: Порт для сервера (по умолчанию 8000).
    """
    current_dir = os.getcwd()

    try:
        # Переходим в нужную директорию
        os.chdir(directory)

        # Настраиваем обработчик и сервер
        handler = SimpleHTTPRequestHandler
        httpd = TCPServer(("", port), handler)

        # Запускаем сервер в отдельном потоке
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        print(f"Сервер запущен на http://localhost:{port}")
        return httpd
    finally:
        # Возвращаемся в исходную директорию
        os.chdir(current_dir)
