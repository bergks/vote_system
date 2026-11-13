from django.shortcuts import render
from .models import Category, Candidate
from django.core.paginator import Paginator


# Create your views here.
def candidates_list(request):
    search_query = request.GET.get("q", "").strip()
    category_filter = request.GET.get("category", "all")
    categories = Category.objects.all()

    candidates = Candidate.objects.all().order_by("title").prefetch_related("category")

    if search_query:
        candidates = candidates.filter(title__icontains=search_query)

    if category_filter != "all":
        candidates = candidates.filter(category__slug=category_filter)

    # Пагинация
    paginator = Paginator(candidates, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "candidates/candidates_list.html",
        {
            "page_obj": page_obj,  # объект страницы
            "paginator": paginator,
            "is_paginated": page_obj.has_other_pages(),
            "categories": categories,
            "search_query": search_query,
            "current_category": category_filter,
        },
    )


def candidate_detail(request, candidate_id):
    try:
        candidate = Candidate.objects.prefetch_related("category").get(pk=candidate_id)
    except:
        return render(
            request, "candidates/canidate_detail.html", {"candidate": None}, status=404
        )

    return render(
        request,
        "candidates/candidate_detail.html",
        {
            "candidate": candidate,
        },
        status=200,
    )
