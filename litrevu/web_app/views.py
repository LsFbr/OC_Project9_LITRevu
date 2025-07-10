from django.shortcuts import render


def login(request):
    return render(request, "web_app/login.html")


def register(request):
    return render(request, "web_app/register.html")
