from django.contrib import admin

from web_app.models import User, Ticket, Review, UserFollows

admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
