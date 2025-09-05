from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """Gestionnaire personnalisé pour les utilisateurs."""

    def create_user(self, username, password=None):
        """Crée et sauvegarde un nouvel utilisateur."""
        if not username:
            raise ValueError("Un nom d'utilisateur est requis")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """Crée et sauvegarde un superutilisateur."""
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé pour l'application LITRevu."""

    username = models.CharField(max_length=40, unique=True, help_text="Nom d'utilisateur unique")
    is_active = models.BooleanField(default=True, help_text="Indique si l'utilisateur est actif")
    is_staff = models.BooleanField(default=False, help_text="Indique si l'utilisateur peut accéder à l'admin")
    date_joined = models.DateTimeField(auto_now_add=True, help_text="Date d'inscription de l'utilisateur")

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        """Retourne le nom d'utilisateur comme représentation string."""
        return self.username


class Ticket(models.Model):
    """Modèle représentant un ticket de demande de critique."""

    title = models.CharField(max_length=128, help_text="Titre du ticket")
    description = models.TextField(max_length=2048, blank=True, help_text="Description détaillée du ticket")
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Utilisateur ayant créé le ticket")
    image = models.ImageField(upload_to="tickets_images/", null=True, blank=True, help_text="Image associée au ticket")
    time_created = models.DateTimeField(auto_now_add=True, help_text="Date de création du ticket")

    def delete(self, *args, **kwargs):
        """Supprime le ticket et son image associée."""
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)


class Review(models.Model):
    """Modèle représentant une critique d'un ticket."""

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, help_text="Ticket critiqué")
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Note de 0 à 5")
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Utilisateur ayant écrit la critique")
    headline = models.CharField(max_length=128, help_text="Titre de la critique")
    body = models.TextField(max_length=8192, blank=True, help_text="Corps de la critique")
    time_created = models.DateTimeField(auto_now_add=True, help_text="Date de création de la critique")


class UserFollows(models.Model):
    """Modèle représentant une relation d'abonnement entre utilisateurs."""

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following',
        help_text="Utilisateur qui suit")
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by',
        help_text="Utilisateur suivi")

    class Meta:
        """Métadonnées pour le modèle UserFollows."""
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )
