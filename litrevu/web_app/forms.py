from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from web_app.models import Ticket, Review


class LoginForm(AuthenticationForm):
    """Formulaire personnalisé pour la connexion des utilisateurs."""

    error_messages = {
        "invalid_login": "Nom d'utilisateur ou mot de passe incorrect.",
    }

    def __init__(self, *args, **kwargs):
        """Initialise le formulaire avec les attributs CSS personnalisés."""
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Nom d\'utilisateur',
            'required': True,
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Mot de passe',
            'required': True,
        })


class RegisterForm(UserCreationForm):
    """Formulaire personnalisé pour l'inscription des nouveaux utilisateurs."""

    class Meta:
        """Métadonnées du formulaire d'inscription."""
        model = get_user_model()
        fields = ['username']

    def __init__(self, *args, **kwargs):
        """Initialise le formulaire avec les attributs CSS et messages d'erreur personnalisés."""
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'unique': 'Ce nom d\'utilisateur est déjà utilisé.',
            'required': 'Ce champ est obligatoire.'
        }
        self.fields['username'].widget.attrs.update({
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Nom d\'utilisateur',
            'label': 'Nom d\'utilisateur',
            'required': True,
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Mot de passe',
            'label': 'Mot de passe',
            'required': True,
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Confirmer mot de passe',
            'label': 'Confirmer mot de passe',
            'required': True,
        })


class TicketForm(forms.ModelForm):
    """Formulaire pour créer et modifier des tickets."""

    class Meta:
        """Métadonnées du formulaire de ticket."""
        model = Ticket
        fields = ["title", "description", "image"]

    def __init__(self, *args, **kwargs):
        """Initialise le formulaire avec les attributs CSS personnalisés."""
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Titre',
            'required': True,
        })
        self.fields['description'].widget.attrs.update({
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Description',
            'required': True,
        })
        self.fields['image'].widget.attrs.update({
            'class': 'py-2',
            'placeholder': 'Image',
            'required': False,
        })


class ReviewForm(forms.ModelForm):
    """Formulaire pour créer et modifier des critiques."""

    RATING_CHOICES = [(i, str(i)) for i in range(6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        """Métadonnées du formulaire de critique."""
        model = Review
        fields = ["headline", "rating", "body"]

    def __init__(self, *args, **kwargs):
        """Initialise le formulaire avec les attributs CSS personnalisés."""
        super().__init__(*args, **kwargs)
        self.fields['headline'].widget.attrs.update({
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Titre',
            'required': True,
        })

        self.fields['body'].widget.attrs.update({
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Commentaire',
            'required': True,
        })


class FollowForm(forms.Form):
    """Formulaire pour s'abonner à un utilisateur."""

    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=40,
        widget=forms.TextInput(attrs={
            "class": "w-full border border-gray-400 rounded px-4 py-2",
            "placeholder": "Nom d'utilisateur",
        })
    )

    def __init__(self, *args, **kwargs):
        """Initialise le formulaire avec l'utilisateur de la requête."""
        self.request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        """Valide le nom d'utilisateur et vérifie qu'il existe et n'est pas l'utilisateur actuel."""
        User = get_user_model()
        username = self.cleaned_data["username"].strip()
        # utilisateur existe ?
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Utilisateur introuvable.")
        # pas soi-même
        if self.request_user and user == self.request_user:
            raise forms.ValidationError("Vous ne pouvez pas vous abonner à vous-même.")
        # on stocke l’objet pour la vue
        self.user_to_follow = user
        return username
