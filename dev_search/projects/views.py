from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
# Create your views here.

def search(pk, project_list):
    return [element for element in project_list if element["id"]==pk]

def projects(request):
    projects_list = Project.objects.all()
    context = {"projects": projects_list}
    return render(request, "projects/projects.html", context)

def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    tags = project_obj.tags.all()
    context = {"project":project_obj, "tags": tags}
    return render(request, "projects/single-project.html", context)

def create_project(request):
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {"form":form}
    return render(request, 'projects/project-form.html', context)