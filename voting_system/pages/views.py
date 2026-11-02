import sqlite3
from django.shortcuts import render

DB_PATH = "data/voting.sqlite"


def index(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Самое популярное голосование
    top_poll = conn.execute("""
        SELECT polls.id, polls.question, COUNT(votes.id) AS total_votes
        FROM polls
        LEFT JOIN votes ON polls.id = votes.poll_id
        GROUP BY polls.id, polls.question
        ORDER BY total_votes DESC
        LIMIT 1;
    """).fetchone()

    conn.close()

    return render(request, "pages/index.html", {"top_poll": top_poll})


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)
