from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from web_app.models import Ticket, Review


class LoginForm(AuthenticationForm):

    error_messages = {
        "invalid_login": "Nom d'utilisateur ou mot de passe incorrect.",
    }

    def __init__(self, *args, **kwargs):
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
    class Meta:
        model = get_user_model()
        fields = ['username']

    def __init__(self, *args, **kwargs):
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
    remove_image = forms.BooleanField(
        required=False, label="Supprimer l’image actuelle"
    )

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

    def __init__(self, *args, **kwargs):
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
        if not getattr(self.instance, "image", None):
            self.fields["remove_image"].widget = forms.HiddenInput()


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

    def __init__(self, *args, **kwargs):
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
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=40,
        widget=forms.TextInput(attrs={
            "class": "w-full border border-gray-400 rounded px-4 py-2",
            "placeholder": "Nom d'utilisateur",
        })
    )

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
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
