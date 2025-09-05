from django.contrib import admin

from web_app.models import User, Ticket, Review, UserFollows


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle User."""

    list_display = ('username', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username',)
    ordering = ('username',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Ticket."""

    list_display = ('title', 'user', 'time_created')
    list_filter = ('time_created', 'user')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-time_created',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle Review."""

    list_display = ('headline', 'ticket', 'user', 'rating', 'time_created')
    list_filter = ('rating', 'time_created', 'user')
    search_fields = ('headline', 'body', 'user__username', 'ticket__title')
    ordering = ('-time_created',)


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour le modèle UserFollows."""

    list_display = ('user', 'followed_user')
    list_filter = ('user', 'followed_user')
    search_fields = ('user__username', 'followed_user__username')
    ordering = ('user',)
