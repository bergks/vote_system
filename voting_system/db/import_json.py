import json
from db.database import get_connection

USERS_FILE = "data/users.json"
POLLS_FILE = "data/polls.json"
VOTES_FILE = "data/votes.json"


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_users(conn):
    users = load_json(USERS_FILE)
    user_data = [
        (user["id"], user["username"])
        for user in users.values()
    ]
    # Импортируем тех пользователей, которые есть
    conn.executemany(
        "INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)",
        user_data
    )

    polls = load_json(POLLS_FILE)
    existing_users = {user[0] for user in user_data}
    for poll in polls.values():
        author_id = poll["author_id"]
        if author_id not in existing_users:

            conn.execute(
                "INSERT INTO users (id, username) VALUES (?, ?)",
                (author_id, f"User_{author_id}")
            )
            existing_users.add(author_id)


def import_polls_and_choices(conn):
    polls = load_json(POLLS_FILE)
    polls_data = []
    choices_data = []
    for poll in polls.values():
        # Добавляем данные в список для таблицы polls
        polls_data.append((
            poll["id"],
            poll["author_id"],
            poll["question"],
            1 if poll["is_active"] else 0,
            poll["created_at"]
        ))
        # Разбираем варианты ответов
        for choice_id, choice_text in poll["choices"].items():
            choices_data.append((
                int(choice_id),
                poll["id"],
                choice_text
            ))

    conn.executemany(
        polls_data
    )
    conn.executemany(
        "INSERT INTO choices (id, poll_id, choice_text) VALUES (?, ?, ?)",
        choices_data
    )


def import_votes(conn):
    votes = load_json(VOTES_FILE)
    # В вашем JSON это список словарей
    votes_data = []
    # Нам нужно сгенерировать ID для голосов, так как в JSON их нет
    for index, vote in enumerate(votes, start=1):
        votes_data.append((
            index,
            vote["user_id"],
            vote["poll_id"],
            vote["choice_id"],
            vote["voted_at"]
        ))
    conn.executemany(
        "INSERT INTO votes (id, user_id, poll_id, choice_id, voted_at)\
            VALUES (?, ?, ?, ?, ?)",
        votes_data
    )
    print(f"Импортировано голосов: {len(votes_data)}")


def main():
    conn = get_connection()
    try:
        print("Начинаем импорт данных...")

        # ВАЖНО: Порядок важен из-за внешних ключей!
        # Сначала пользователи и голосования, потом голоса
        import_users(conn)
        import_polls_and_choices(conn)
        import_votes(conn)

        conn.commit()
        print("Импорт успешно завершен!")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при импорте: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
