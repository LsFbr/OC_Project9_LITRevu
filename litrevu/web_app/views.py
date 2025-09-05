from itertools import chain
from django.db.models import Value, CharField, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.db import IntegrityError
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from web_app.forms import LoginForm, RegisterForm, TicketForm, ReviewForm, FollowForm
from web_app.models import Ticket, Review, UserFollows


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
        followed_ids = UserFollows.objects.filter(user=request.user) \
            .values_list("followed_user_id", flat=True)

        tickets = (
            Ticket.objects
            .filter(Q(user=request.user) | Q(user_id__in=followed_ids))
            .select_related("user")
            .annotate(content_type=Value("ticket", output_field=CharField()))
        )

        reviews = (
            Review.objects
            .filter(Q(user=request.user) | Q(user_id__in=followed_ids) | Q(ticket__user=request.user))
            .select_related("user", "ticket", "ticket__user")
            .annotate(content_type=Value("review", output_field=CharField()))
        )
        content = sorted(
            chain(tickets, reviews),
            key=lambda object: (object.time_created, 1 if object.content_type == "review" else 0),
            reverse=True
        )

        reviewed_ticket_ids = Review.objects.values_list("ticket_id", flat=True)
        return render(request, self.template_name, {"content": content, "reviewed_ticket_ids": reviewed_ticket_ids})


class PostsView(LoginRequiredMixin, View):
    template_name = "web_app/posts.html"

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user).annotate(content_type=Value("ticket", CharField()))
        reviews = Review.objects.filter(user=request.user).annotate(content_type=Value("review", CharField()))
        content = sorted(
            chain(tickets, reviews),
            key=lambda object: (object.time_created, 1 if object.content_type == "review" else 0),
            reverse=True
        )
        return render(request, self.template_name, {"content": content})


class SubscriptionsView(LoginRequiredMixin, View):
    template_name = "web_app/subscriptions.html"

    def _context(self, request, form=None):
        """Construit le contexte pour le GET et pour ré-afficher en cas d'erreur de form."""
        follow_form = form or FollowForm(request_user=request.user)
        subscriptions = (
            UserFollows.objects
            .select_related("followed_user")
            .filter(user=request.user)
            .order_by("followed_user__username")
        )
        followers = (
            UserFollows.objects
            .select_related("user")
            .filter(followed_user=request.user)
            .order_by("user__username")
        )
        return {
            "follow_form": follow_form,
            "subscriptions": subscriptions,
            "followers": followers,
        }

    def get(self, request):
        return render(request, self.template_name, self._context(request))

    def post(self, request):
        operation = request.POST.get("operation", "follow")

        if operation == "unfollow":
            # Désabonnement
            user_follow_id = request.POST.get("user_follow_id")
            user_follow = get_object_or_404(UserFollows, id=user_follow_id, user=request.user)
            username = user_follow.followed_user.username
            user_follow.delete()
            messages.success(request, f"Vous ne suivez plus {username}.")
            return redirect("subscriptions")

        # Abonnement
        form = FollowForm(request.POST, request_user=request.user)
        if form.is_valid():
            to_follow = form.user_to_follow
            try:
                UserFollows.objects.create(user=request.user, followed_user=to_follow)
            except IntegrityError:
                messages.warning(request, f"Vous suivez déjà {to_follow.username}.")
            else:
                messages.success(request, f"Vous suivez maintenant {to_follow.username}.")
            return redirect("subscriptions")

        return render(request, self.template_name, self._context(request, form=form))


class TicketCreateView(LoginRequiredMixin, View):
    template_name = "web_app/ticket.html"

    def get(self, request):
        form = TicketForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("flux")
        else:
            message = "Erreur lors de la création du ticket"
        return render(request, self.template_name, {"form": form, "message": message})


class TicketEditView(LoginRequiredMixin, View):
    template_name = "web_app/ticket_edit.html"

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
        form = TicketForm(instance=ticket)
        return render(request, self.template_name, {"form": form, "ticket": ticket})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket.title = form.cleaned_data["title"]
            ticket.description = form.cleaned_data["description"]

            if request.POST.get("image-clear") == "on":
                if ticket.image:
                    ticket.image.delete(save=False)
                ticket.image = None

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
    template_name = "web_app/review.html"

    def get(self, request, ticket_id=None):
        if ticket_id:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            review_form = ReviewForm()
            return render(request, self.template_name, {
                "ticket": ticket,
                "review_form": review_form
            })
        else:
            ticket_form = TicketForm()
            review_form = ReviewForm()
            return render(request, self.template_name, {
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


class ReviewEditView(LoginRequiredMixin, View):
    template_name = "web_app/review_edit.html"

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, user=request.user)
        ticket = review.ticket
        review_form = ReviewForm(initial={
            "headline": review.headline,
            "rating": review.rating,
            "body": review.body
        })
        return render(request, self.template_name, {
            "review_form": review_form,
            "ticket": ticket
        })

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review.headline = review_form.cleaned_data["headline"]
            review.rating = review_form.cleaned_data["rating"]
            review.body = review_form.cleaned_data["body"]
            review.save()
            return redirect("posts")
        return render(request, self.template_name, {
            "review_form": review_form,
            "ticket": review.ticket
        })


class ReviewDeleteView(LoginRequiredMixin, View):
    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review.delete()
        return redirect("posts")
