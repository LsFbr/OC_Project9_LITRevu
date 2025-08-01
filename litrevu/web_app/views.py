from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from web_app.forms import LoginForm, RegisterForm, TicketForm
from web_app.models import Ticket


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class CustomLoginView(LoginView):
    template_name = "web_app/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


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


class TicketDeleteView(LoginRequiredMixin, View):
    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
        ticket.delete()
        return redirect("posts")
