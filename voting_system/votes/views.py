import sqlite3
from django.shortcuts import render

# Путь к нашей новой базе данных
DB_PATH = "data/voting.sqlite"


def get_db_connection():
    """Вспомогательная функция для подключения к БД."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def poll_list(request):
    """Страница со списком всех голосований, поиском и фильтрацией."""
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'all')
    
    conn = get_db_connection()
    
    # Вариант 1: Есть и поиск, и фильтр по статусу
    if search_query and status_filter == 'active':
        polls = conn.execute(
            """
            SELECT id, question, is_active, created_at
            FROM polls
            WHERE question
            LIKE ? AND is_active = 1
            ORDER BY id DESC
            """,
            (f"%{search_query}%",)
        ).fetchall()

    elif search_query and status_filter == 'finished':
        polls = conn.execute(
            """
            SELECT id, question, is_active, created_at
            FROM polls
            WHERE question
            LIKE ? AND is_active = 0
            ORDER BY id DESC
            """,
            (f"%{search_query}%",)
        ).fetchall()
        
    elif search_query:
        polls = conn.execute(
            """
            SELECT id, question, is_active, created_at
            FROM polls
            WHERE question
            LIKE ?
            ORDER BY id DESC
            """,
            (f"%{search_query}%",)
        ).fetchall()
        
    elif status_filter == 'active':
        polls = conn.execute(
            """
            SELECT id, question, is_active, created_at
            FROM polls
            WHERE is_active = 1
            ORDER BY id DESC
            """
        ).fetchall()

    elif status_filter == 'finished':
        polls = conn.execute(
            """
            SELECT id, question, is_active, created_at
            FROM polls
            WHERE is_active = 0
            ORDER BY id DESC
            """
        ).fetchall()

    else:
        polls = conn.execute(
            """
            SELECT id, question, is_active, created_at
            FROM polls
            ORDER BY id DESC
            """
        ).fetchall()
        
    conn.close()
    
    return render(request, "votes/poll_list.html", {
        "polls": polls,
        "search_query": search_query,
        "current_status": status_filter,
    })


def poll_detail(request, poll_id):
    """Страница с конкретным голосованием и результатами."""
    conn = get_db_connection()
    poll = conn.execute("SELECT id, question, is_active, created_at \
                        FROM polls WHERE id = ?",
                        (poll_id,)).fetchone()
    if poll is None:
        conn.close()
        return render(request, "votes/poll_detail.html",
                      {"poll": None}, status=404)

    # получаем варианты и количество голосов
    choices_data = conn.execute("""
        SELECT choices.choice_text, COUNT(votes.id) AS votes_count
        FROM choices
        LEFT JOIN votes ON choices.id = votes.choice_id
        WHERE choices.poll_id = ?
        GROUP BY choices.id
    """, (poll_id,)).fetchall()
    
    conn.close()
    
    return render(
        request,
        "votes/poll_detail.html",
        {
            "poll": poll,
            "choices_data": choices_data,
        },
        status=200
    )


def statistics(request):
    conn = get_db_connection()
    
    total_polls = conn.execute("SELECT COUNT(*) AS count FROM polls").fetchone()['count']
    total_votes = conn.execute("SELECT COUNT(*) AS count FROM votes").fetchone()['count']
    
    stats = conn.execute("""
        SELECT polls.question, COUNT(votes.id) AS votes_count
        FROM polls
        LEFT JOIN votes ON polls.id = votes.poll_id
        GROUP BY polls.id
        ORDER BY votes_count DESC
    """).fetchall()
    
    recent_votes = conn.execute("""
        SELECT users.username, polls.question,
               choices.choice_text, votes.voted_at
        FROM votes
        JOIN users ON votes.user_id = users.id
        JOIN polls ON votes.poll_id = polls.id
        JOIN choices ON votes.choice_id = choices.id
        ORDER BY votes.voted_at DESC
        LIMIT 5
    """).fetchall()

    conn.close()
    
    return render(request, "votes/statistics.html", {
        "total_polls": total_polls,
        "total_votes": total_votes,
        "stats": stats,
        "recent_votes": recent_votes
    })


def page_not_found(request, exception):
    return render(request, "pages/404.html", status=404)