from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .utils import search_projects, get_range_paginator


def projects(request):
    projects, search_query = search_projects(request)
    paginator = Paginator(projects, 3)  # set the project results into 3

    custom_range, projects = get_range_paginator(request, paginator)

    context = {
        "projects": projects,
        "search_query": search_query,
        "paginator": paginator,
        "custom_range": custom_range,
    }
    return render(request, "projects/projects.html", context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    tags = project_obj.tags.all()
    context = {"project": project_obj, "tags": tags}

    return render(request, "projects/single_project.html", context)


@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            return save_project(form, profile)

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


def save_project(form, profile):
    project = form.save(commit=False)
    project.owner = profile
    project.save()
    return redirect("account")


@login_required(login_url="login")
def update_project(request, pk):
    profile = request.use.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    context = {"object": project}
    return render(request, "delete_template.html", context)
