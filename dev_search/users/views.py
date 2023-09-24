from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from .forms import CustomUserCreationForm


def login_user(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        if user := authenticate(request, username=username, password=password):
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Username or password is incorrect! ")

    return render(request, "users/login_register.html")


def logout_user(request):
    logout(request)
    messages.info(request, "User logged out successfully")
    return redirect("login")


def register_user(request):
    page = "register"
    form = CustomUserCreationForm
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            return create_user(form, request)
        else:
            messages.error(request, "An error has occurred during registration.")

    context = {
        "page": page,
        "form": form,
    }
    return render(request, "users/login_register.html", context)


# TODO Rename this here and in `register_user`
def create_user(form, request):
    user = form.save(commit=False)
    user.username = user.username.lower()
    user.save()

    messages.success(request, "User account as created successfully.")

    login(request, user)
    return redirect("profiles")


# Create your views here.
def profiles(request):
    user_profiles = Profile.objects.all()
    context = {"user_profiles": user_profiles}
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")

    context = {
        "profile": profile,
        "top_skills": top_skills,
        "other_skills": other_skills,
    }
    return render(request, "users/user_profile.html", context)
