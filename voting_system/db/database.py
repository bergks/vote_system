import sqlite3

# Путь к файлу базы данных (относительно корня проекта)
DB_PATH = "data/voting.sqlite"


def get_connection():
    """Создает соединение с базой данных и включает проверку внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    # Включаем проверку внешних ключей (в SQLite по умолчанию она выключена)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
