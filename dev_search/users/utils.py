from django.db.models import Q
from django.core.paginator import PageNotAnInteger, EmptyPage

from .models import Skill, Profile


def search_profiles(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")
        print("SEARCH", search_query)

    skills = Skill.objects.filter(name__iexact=search_query)

    user_profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query)
        | Q(short_intro__icontains=search_query)
        | Q(skill__in=skills)
    )
    return user_profiles, search_query


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
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    return profiles


def get_range_paginator(request, paginator):
    page = get_page(request)
    return get_range(page, paginator), get_paginator(page, paginator)
