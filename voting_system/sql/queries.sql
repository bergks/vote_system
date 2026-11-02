-- ============================================
-- SQL-запросы для проекта Voting System
-- ============================================

-- 1. Получение списка всех голосований (для страницы /votes/)
SELECT id, question, is_active, created_at 
FROM polls 
ORDER BY id DESC;

-- 2. Получение конкретного голосования по ID (для страницы /votes/<id>/)
SELECT id, question, is_active, created_at 
FROM polls 
WHERE id = ?;

-- 3. Получение всех вариантов ответа для конкретного голосования (для страницы /votes/<id>/)
SELECT id, choice_text 
FROM choices 
WHERE poll_id = ?;

-- 4. JOIN: Получение вопроса и всех его вариантов ответа одной выборкой
SELECT polls.question, choices.choice_text 
FROM polls 
JOIN choices ON polls.id = choices.poll_id 
WHERE polls.id = ?;

-- 5. Агрегатная функция: Подсчет общего количества отданных голосов во всей системе
SELECT COUNT(*) AS total_votes FROM votes;

-- 6. Агрегатная функция + JOIN: Подсчет голосов для конкретного голосования
SELECT COUNT(votes.id) AS votes_count 
FROM votes 
WHERE votes.poll_id = ?;

-- 7. GROUP BY + JOIN: Статистика голосов по каждому варианту для конкретного опроса
-- (LEFT JOIN нужен, чтобы показать варианты с 0 голосов)
SELECT choices.choice_text, COUNT(votes.id) AS votes_count 
FROM choices 
LEFT JOIN votes ON choices.id = votes.choice_id 
WHERE choices.poll_id = ? 
GROUP BY choices.id;

-- 8. JOIN (3 таблицы): Кто и за что голосовал (полная информация)
SELECT polls.id, polls.question, COUNT(votes.id) AS total_votes
FROM polls 
LEFT JOIN votes ON polls.id = votes.poll_id 
GROUP BY polls.id, polls.question
ORDER BY total_votes DESC 
LIMIT 1;
-- 9. Фильтрация WHERE: Поиск активных голосований
SELECT id, question 
FROM polls 
WHERE is_active = 1;

-- 10. GROUP BY + HAVING: Пользователи, которые проголосовали больше 1 раза (самые активные)
SELECT users.username, COUNT(votes.id) AS votes_count 
FROM users 
JOIN votes ON users.id = votes.user_id 
GROUP BY users.id 
HAVING COUNT(votes.id) > 1;