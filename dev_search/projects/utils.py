from django.core.paginator import PageNotAnInteger, EmptyPage
from django.db.models import Q

from .models import Tag, Project


def search_projects(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query)
        | Q(description__icontains=search_query)
        | Q(owner__name__icontains=search_query)
        | Q(tags__in=tags)
    )

    return projects, search_query


def get_page(request) -> int:
    return request.GET.get("page") or 1


def get_range(page, paginator):
    left_index = int(page) - 4
    left_index = max(left_index, 1)

    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    return range(left_index, right_index)


def get_paginator(page, paginator):
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    return projects


def get_range_paginator(request, paginator):
    page = get_page(request)
    return get_range(page, paginator), get_paginator(page, paginator)
