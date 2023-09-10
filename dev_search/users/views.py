from django.shortcuts import render
from .models import Profile


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
