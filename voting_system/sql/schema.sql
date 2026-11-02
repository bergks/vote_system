-- 1. Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE
);

-- 2. Таблица голосований (вопросов)
CREATE TABLE IF NOT EXISTS polls (
    id INTEGER PRIMARY KEY,
    author_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT,
    FOREIGN KEY (author_id) REFERENCES users(id)
);

-- 3. Таблица вариантов ответа
CREATE TABLE IF NOT EXISTS choices (
    id INTEGER PRIMARY KEY,
    poll_id INTEGER NOT NULL,
    choice_text TEXT NOT NULL,
    FOREIGN KEY (poll_id) REFERENCES polls(id)
);

-- 4. Таблица отданных голосов
CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    poll_id INTEGER NOT NULL,
    choice_id INTEGER NOT NULL,
    voted_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (poll_id) REFERENCES polls(id),
    FOREIGN KEY (choice_id) REFERENCES choices(id)
);