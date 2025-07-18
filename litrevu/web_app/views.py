from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from web_app.forms import LoginForm


def logout_user(request):
    logout(request)
    return redirect("login")


def login_view(request):
    form = LoginForm()
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("flux")
            else:
                message = 'Identifiants invalides.'
    return render(request, "web_app/login.html", context={"form": form, "message": message})


def register(request):
    return render(request, "web_app/register.html")


@login_required
def flux(request):
    return render(request, "web_app/flux.html")
