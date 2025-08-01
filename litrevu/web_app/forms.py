from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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


class TicketForm(forms.Form):
    title = forms.CharField(
        max_length=128,
        label="Titre",
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Titre',
            'required': True
        })
    )
    description = forms.CharField(
        max_length=2048,
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Description',
            'required': True
        })
    )
    image = forms.ImageField(
        label="Image",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'py-2',
            'placeholder': 'Image'
        })
    )
