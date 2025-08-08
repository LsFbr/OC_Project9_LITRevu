from itertools import chain
from django.db.models import Value, CharField
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from web_app.forms import LoginForm, RegisterForm, TicketForm, ReviewForm
from web_app.models import Ticket, Review


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
        tickets = Ticket.objects.all().annotate(content_type=Value("ticket", CharField()))
        reviews = Review.objects.select_related("ticket", "user", "ticket__user") \
                                .annotate(content_type=Value("review", CharField()))

        content = sorted(
            chain(tickets, reviews),
            key=lambda object: (object.time_created, 1 if object.content_type == "review" else 0),
            reverse=True
        )
        return render(request, self.template_name, {"content": content})


class PostsView(LoginRequiredMixin, View):
    template_name = "web_app/posts.html"

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
        return render(request, self.template_name, {"tickets": tickets})


class SubscriptionsView(LoginRequiredMixin, View):
    template_name = "web_app/subscriptions.html"

    def get(self, request):
        return render(request, self.template_name)


class TicketCreateView(LoginRequiredMixin, View):
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


class ReviewCreateView(View):
    def get(self, request, ticket_id=None):
        if ticket_id:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            review_form = ReviewForm()
            return render(request, "web_app/review.html", {
                "ticket": ticket,
                "review_form": review_form
            })
        else:
            ticket_form = TicketForm()
            review_form = ReviewForm()
            return render(request, "web_app/review.html", {
                "ticket_form": ticket_form,
                "review_form": review_form
            })

    def post(self, request, ticket_id=None):
        if ticket_id:
            ticket = get_object_or_404(Ticket, id=ticket_id)
        else:
            ticket_form = TicketForm(request.POST, request.FILES)
            if ticket_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()
            else:
                review_form = ReviewForm(request.POST)
                return render(request, "web_app/review.html", {
                    "ticket_form": ticket_form,
                    "review_form": review_form
                })

        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("flux")
        return render(request, "web_app/review.html", {
            "ticket": ticket,
            "review_form": review_form
        })
