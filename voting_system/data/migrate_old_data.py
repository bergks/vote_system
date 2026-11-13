import os
import sys
import sqlite3
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voting_system.settings')
django.setup()

from user.models import User, BaseModel
from votes.models import Poll, Choice, Vote

# Путь к старой базе данных
OLD_DB_PATH = 'data/voting.sqlite'

def migrate_data():
    conn = sqlite3.connect(OLD_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Перенос пользователей
    print("Migrating users...")
    cursor.execute("SELECT username FROM users")
    for row in cursor.fetchall():
        user = User.objects.create(
            username=row['username'],
            name=row['username'],
        )

    # 2. Перенос голосований
    print("Migrating polls...")
    cursor.execute("SELECT id, author_id, question, is_active, created_at FROM polls")
    for row in cursor.fetchall():
        try:
            author = User.objects.get(id=row['author_id'])
        except User.DoesNotExist:
            print(f"  Author with id {row['author_id']} not found. Skipping poll '{row['question']}'.")
            continue

        # Конвертируем is_active в status
        status = Poll.PollStatus.ACTIVE if row['is_active'] else Poll.PollStatus.FINISHED

        poll = Poll.objects.create(
                author = author,
                question = row['question'],
                description = f'Описание для голосования с вопросом {row["question"]}',
                status = status,
        )

    # 3. Перенос вариантов ответов
    print("Migrating choices...")
    cursor.execute("SELECT id, poll_id, choice_text FROM choices")
    for row in cursor.fetchall():
        try:
            poll = Poll.objects.get(id=row['poll_id'])
        except Poll.DoesNotExist:
            print(f"  Poll with id {row['poll_id']} not found. Skipping choice '{row['choice_text']}'.")
            continue

        choice = Choice.objects.create(
            poll = poll,
            choice_text = row['choice_text']
        )

    # 4. Перенос голосов
    print("Migrating votes...")
    cursor.execute("SELECT id, user_id, choice_id FROM votes")
    for row in cursor.fetchall():
        try:
            user = User.objects.get(id=row['user_id'])
            choice = Choice.objects.get(id=row['choice_id'])
        except (User.DoesNotExist, Choice.DoesNotExist):
            print(f"  User or Choice for vote {row['id']} not found. Skipping.")
            continue

        vote = Vote.objects.get_or_create(
            user = user,
            choice = choice,
        )

    conn.close()
    print("Migration finished.")

if __name__ == '__main__':
    migrate_data()