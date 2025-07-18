from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=40,
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Nom d\'utilisateur',
            'required': True
        })
    )
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-400 rounded px-4 py-2',
            'placeholder': 'Mot de passe',
            'required': True
        }),
        label='Password'
    )
