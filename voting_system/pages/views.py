import sqlite3
from django.shortcuts import render
from votes.models import Poll
from django.db.models import Count

DB_PATH = "data/voting.sqlite"


def index(request):

    top_poll = Poll.objects.annotate(votes_count=Count('votes')).order_by('-votes_count')[0]

    return render(request, "pages/index.html", {"top_poll": top_poll})


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)
