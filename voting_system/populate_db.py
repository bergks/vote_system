import os
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voting_system.settings")
django.setup()

import random
from django.db import transaction
from django.utils import timezone
from user.models import User
from candidates.models import Category, Candidate
from votes.models import Poll, Vote


# ---------- 1. Пользователи ----------
USERS = [
    ("ivan_petrov",     "Иван",     "Петров"),
    ("anna_smirnova",   "Анна",     "Смирнова"),
    ("sergey_kozlov",   "Сергей",   "Козлов"),
    ("maria_ivanova",   "Мария",    "Иванова"),
    ("dmitry_volkov",   "Дмитрий",  "Волков"),
    ("elena_sokolova",  "Елена",    "Соколова"),
    ("pavel_morozov",   "Павел",    "Морозов"),
    ("olga_novikova",   "Ольга",    "Новикова"),
    ("artem_lebede",    "Артём",    "Лебедев"),
    ("kate_orlova",     "Екатерина","Орлова"),
    ("nikita_zaytsev",  "Никита",   "Зайцев"),
    ("yulia_pavlova",   "Юлия",     "Павлова"),
    ("maxim_kuznetsov", "Максим",   "Кузнецов"),
    ("sveta_popova",    "Светлана", "Попова"),
    ("oleg_vasi",       "Олег",     "Васильев"),
]


# ---------- 2. Категории ----------
CATEGORIES = [
    ("Драма",          "drama"),
    ("Комедия",        "comedy"),
    ("Фантастика",     "sci-fi"),
    ("Триллер",        "thriller"),
    ("Ужасы",          "horror"),
    ("Анимация",       "animation"),
    ("Документальное", "documentary"),
    ("Мелодрама",      "romance"),
]


# ---------- 3. Кандидаты (фильмы) ----------
CANDIDATES = [
    # (title, director, year, categories_slugs, description)
    ("Побег из Шоушенка",       "Фрэнк Дарабонт",   1994, ["drama"],                 "История о надежде и дружбе в стенах тюрьмы."),
    ("Крёстный отец",           "Фрэнсис Форд Коппола", 1972, ["drama", "thriller"], "Классическая сага о мафиозной семье."),
    ("Тёмный рыцарь",           "Кристофер Нолан",  2008, ["thriller", "drama"],     "Бэтмен против Джокера."),
    ("Криминальное чтиво",      "Квентин Тарантино", 1994, ["thriller", "drama"],    "Несколько переплетающихся историй."),
    ("Форрест Гамп",            "Роберт Земекис",   1994, ["drama", "romance"],      "Жизнь простого человека на фоне истории США."),
    ("Начало",                  "Кристофер Нолан",  2010, ["sci-fi", "thriller"],    "Кража идей через сны."),
    ("Матрица",                 "Лана Вачовски",    1999, ["sci-fi"],                "Реальность — иллюзия."),
    ("Интерстеллар",            "Кристофер Нолан",  2014, ["sci-fi", "drama"],       "Путешествие сквозь червоточину."),
    ("Король Лев",              "Роджер Аллерс",    1994, ["animation", "drama"],    "Взросление львёнка Симбы."),
    ("История игрушек",         "Джон Лассетер",    1995, ["animation", "comedy"],   "Игрушки оживают, когда люди не видят."),
    ("Молчание ягнят",          "Джонатан Демми",   1991, ["thriller", "horror"],    "Кларис Старлинг и Ганнибал Лектер."),
    ("Сияние",                  "Стэнли Кубрик",    1980, ["horror"],                "Отель, который сводит с ума."),
    ("Один дома",               "Крис Коламбус",    1990, ["comedy"],                "Кевин защищает дом от грабителей."),
    ("Назад в будущее",         "Роберт Земекис",   1985, ["sci-fi", "comedy"],      "Марти Макфлай в 1955 году."),
    ("Джанго освобождённый",    "Квентин Тарантино", 2012, ["drama", "thriller"],    "Освобождение раба на Диком Западе."),
    ("Планета Земля",           "Аластер Фотергилл", 2006, ["documentary"],          "Документальный сериал о природе."),
    ("Ла-Ла Ленд",              "Дэмьен Шазелл",    2016, ["romance", "drama"],      "История любви в Лос-Анджелесе."),
    ("Дюна",                    "Дени Вильнёв",     2021, ["sci-fi", "drama"],       "Борьба за планету Арракис."),
    ("Властелин колец: Братство Кольца", "Питер Джексон", 2001, ["sci-fi", "drama"], "Путешествие к Роковой горе."),
    ("Ирония судьбы",           "Эльдар Рязанов",   1975, ["comedy", "romance"],     "Случайная встреча в Ленинграде."),
]


# ---------- 4. Опросы ----------
POLLS = [
    {
        "question": "Лучший фильм 1994 года?",
        "description": "Выберите лучший фильм, вышедший в 1994 году.",
        "status": Poll.PollStatus.FINISHED,
        "candidates": ["Побег из Шоушенка", "Криминальное чтиво", "Форрест Гамп", "Король Лев"],
    },
    {
        "question": "Лучший фильм Кристофера Нолана?",
        "description": "Голосуем за самого любимого Нолана.",
        "status": Poll.PollStatus.ACTIVE,
        "candidates": ["Тёмный рыцарь", "Начало", "Интерстеллар"],
    },
    {
        "question": "Лучший фантастический фильм?",
        "description": "Что из научной фантастики вы любите больше всего?",
        "status": Poll.PollStatus.ACTIVE,
        "candidates": ["Матрица", "Начало", "Интерстеллар", "Назад в будущее", "Дюна"],
    },
    {
        "question": "Лучший анимационный фильм?",
        "description": "Выбираем лучший мультфильм.",
        "status": Poll.PollStatus.ACTIVE,
        "candidates": ["Король Лев", "История игрушек"],
    },
    {
        "question": "Самый страшный фильм?",
        "description": "Что действительно пугает?",
        "status": Poll.PollStatus.FINISHED,
        "candidates": ["Сияние", "Молчание ягнят"],
    },
    {
        "question": "Лучшая комедия?",
        "description": "Что рассмешит вас сильнее всего?",
        "status": Poll.PollStatus.ACTIVE,
        "candidates": ["Один дома", "Назад в будущее", "Ирония судьбы", "История игрушек"],
    },
    {
        "question": "Лучший фильм Тарантино?",
        "description": "Классика от Квентина.",
        "status": Poll.PollStatus.ACTIVE,
        "candidates": ["Криминальное чтиво", "Джанго освобождённый"],
    },
]


@transaction.atomic
def populate():
    # Очистка (осторожно на проде!)
    Vote.objects.all().delete()
    Poll.objects.all().delete()
    Candidate.objects.all().delete()
    Category.objects.all().delete()
    User.objects.all().delete()

    # Пользователи
    users = []
    for username, name, surname in USERS:
        users.append(User.objects.create(username=username, name=name, surname=surname))
    print(f"Создано пользователей: {len(users)}")

    # Категории
    categories = {}
    for title, slug in CATEGORIES:
        categories[slug] = Category.objects.create(title=title, slug=slug)
    print(f"Создано категорий: {len(categories)}")

    # Кандидаты
    candidates = {}
    for title, director, year, cat_slugs, desc in CANDIDATES:
        c = Candidate.objects.create(
            title=title, director=director, year=year, description=desc
        )
        c.category.set([categories[s] for s in cat_slugs])
        candidates[title] = c
    print(f"Создано кандидатов: {len(candidates)}")

    # Опросы
    polls = []
    for p in POLLS:
        poll = Poll.objects.create(
            question=p["question"],
            description=p["description"],
            status=p["status"],
        )
        poll.choices.set([candidates[t] for t in p["candidates"]])
        polls.append(poll)
    print(f"Создано опросов: {len(polls)}")

    # Голоса — каждый пользователь голосует в случайном подмножестве опросов
    total_votes = 0
    for user in users:
        # 1–4 опроса на пользователя
        for poll in random.sample(polls, k=random.randint(1, min(4, len(polls)))):
            choices = list(poll.choices.all())
            choice = random.choice(choices)
            Vote.objects.create(poll=poll, choice=choice, user=user)
            total_votes += 1
    print(f"Создано голосов: {total_votes}")


if __name__ == "__main__":
    populate()