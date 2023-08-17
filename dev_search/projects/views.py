from django.shortcuts import render

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
    page = "projects"
    number = 1
    context = {"page":page, "number": number, "projects": projects_list}
    return render(request, "projects/projects.html", context)

def project(request, pk):
    project_obj = None
    context = None
    if search(pk, projects_list):
        context = {"project": search(pk, projects_list)[0]}
    return render(request, "projects/single-project.html", context)