from django.shortcuts import render
from .models import Project

# Create your views here.

projects_list = [
    {
        "id": "1",
        "title": "Ecommerce Website",
        "description": "Fully functional ecommerce website",
    },
    {
        "id": "2",
        "title": "Portfolio Website",
        "description": "A personal website to write articles and display work",
    },
    {
        "id": "3",
        "title": "Social Network",
        "description": "An open source project built by the community",
    },
]

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