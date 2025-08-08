"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from web_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("", views.CustomLoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("flux/", views.FluxView.as_view(), name="flux"),
    path("posts/", views.PostsView.as_view(), name="posts"),
    path("subscriptions/", views.SubscriptionsView.as_view(), name="subscriptions"),
    path("ticket/", views.TicketCreateView.as_view(), name="ticket"),
    path("ticket/edit/<int:ticket_id>/", views.TicketEditView.as_view(), name="edit_ticket"),
    path("ticket/delete/<int:ticket_id>/", views.TicketDeleteView.as_view(), name="delete_ticket"),
    path("review/", views.ReviewCreateView.as_view(), name="review"),
    path("review/ticket/<int:ticket_id>/", views.ReviewCreateView.as_view(), name="review_from_ticket"),
    path("review/edit/<int:review_id>/", views.ReviewEditView.as_view(), name="edit_review"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
