from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.forms import LoginForm, RegisterForm, TicketForm
from web_app.models import Ticket
from django.urls import reverse_lazy


class LogoutView(View):
    def get(self, request):
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
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                message = 'Identifiants invalides.'
        return render(request, self.template_name, {"form": form, "message": message})


class RegisterView(View):
    template_name = "web_app/register.html"
    form_class = RegisterForm
    success_url = "login"

    def get(self, request):
        form = self.form_class()
        message = ""
        return render(request, self.template_name, {"form": form, "message": message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request, self.template_name, {"form": form})


class FluxView(LoginRequiredMixin, View):
    template_name = "web_app/flux.html"

    def get(self, request):
        tickets = Ticket.objects.all().order_by("-time_created")
        return render(request, self.template_name, {"tickets": tickets})


class PostsView(LoginRequiredMixin, View):
    template_name = "web_app/posts.html"

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
        return render(request, self.template_name, {"tickets": tickets})


class ReviewView(LoginRequiredMixin, View):
    template_name = "web_app/review.html"

    def get(self, request):
        return render(request, self.template_name)


class SubscriptionsView(LoginRequiredMixin, View):
    template_name = "web_app/subscriptions.html"

    def get(self, request):
        return render(request, self.template_name)


class TicketView(LoginRequiredMixin, View):
    template_name = "web_app/ticket.html"
    form_class = TicketForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = Ticket(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                image=form.cleaned_data["image"],
                user=request.user
            )
            ticket.save()
            return redirect("flux")
        else:
            message = "Erreur lors de la création du ticket"
            print(form.errors)
        return render(request, self.template_name, {"form": form, "message": message})


class TicketEditView(LoginRequiredMixin, View):
    template_name = "web_app/ticket_edit.html"
    form_class = TicketForm

    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id, user=request.user)
        form = self.form_class(initial={
            'title': ticket.title,
            'description': ticket.description,
            'image': ticket.image,
        })
        return render(request, self.template_name, {"form": form, "ticket": ticket})

    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id, user=request.user)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket.title = form.cleaned_data["title"]
            ticket.description = form.cleaned_data["description"]
            new_image = form.cleaned_data.get("image")
            if new_image:
                if ticket.image and ticket.image != new_image:
                    ticket.image.delete(save=False)
                ticket.image = new_image

            ticket.save()
            return redirect("posts")
        return render(request, self.template_name, {"form": form, "ticket": ticket})


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "web_app/ticket_confirm_delete.html"
    success_url = reverse_lazy("posts")

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
