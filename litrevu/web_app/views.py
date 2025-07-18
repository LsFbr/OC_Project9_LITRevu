from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import View
from web_app.forms import LoginForm


def logout_user(request):
    logout(request)
    return redirect("login")


class LoginView(View):
    template_name = "web_app/login.html"
    form_class = LoginForm
    success_url = "flux"

    def get(self, request):
        form = self.form_class()
        message = ""
        return render(request, self.template_name, {"form": form, "message": message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect('flux')
            else:
                message = 'Identifiants invalides.'
        return render(request, self.template_name, {"form": form, "message": message})


def register(request):
    return render(request, "web_app/register.html")


@login_required
def flux(request):
    return render(request, "web_app/flux.html")
