from django import forms
from django.contrib.auth.models import User

from .models import Candidacy, Profile, Vote


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Tu usuario', 'autocomplete': 'username'}),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña', 'autocomplete': 'current-password'}),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'autocomplete': 'username'}),
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'autocomplete': 'email'}),
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite la contraseña'}),
    )
    ficha = forms.CharField(
        label='Ficha',
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'No. Ficha (ej): 3229879'}),
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Ese usuario ya existe. Elige otro nombre.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ese correo ya está registrado. Usa otro correo.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas deben coincidir.')
        return cleaned_data


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico registrado', 'autocomplete': 'email'}),
    )


class PasswordResetConfirmForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico registrado', 'autocomplete': 'email'}),
    )
    code = forms.CharField(
        label='Código de restablecimiento',
        max_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Código recibido por correo'}),
    )
    password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña'}),
    )
    password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite la contraseña'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas deben coincidir.')
        return cleaned_data


class AprendizForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
    )
    email = forms.EmailField(
        label='Correo electrónico',
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
    )
    ficha = forms.CharField(
        label='Ficha',
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 3229879'}),
    )
    password1 = forms.CharField(
        label='Contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite la contraseña'}),
    )

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['username'].initial = instance.user.username
            self.fields['email'].initial = instance.user.email
            self.fields['ficha'].initial = instance.ficha

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance:
            if User.objects.filter(username=username).exclude(pk=self.instance.user.pk).exists():
                raise forms.ValidationError('Ese usuario ya existe. Elige otro nombre.')
        else:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('Ese usuario ya existe. Elige otro nombre.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.user.pk if self.instance else None).exists():
            self.add_error('email', 'Ese correo ya está registrado. Usa otro correo.')
        if self.instance:
            if password1 or password2:
                if password1 != password2:
                    self.add_error('password2', 'Las contraseñas deben coincidir.')
        else:
            if not password1:
                self.add_error('password1', 'La contraseña es requerida.')
            if password1 and password2 and password1 != password2:
                self.add_error('password2', 'Las contraseñas deben coincidir.')
        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data.get('email')
        ficha = self.cleaned_data['ficha']
        password1 = self.cleaned_data.get('password1')

        if self.instance:
            user = self.instance.user
            user.username = username
            user.email = email
            if password1:
                user.set_password(password1)
            user.save()
            self.instance.ficha = ficha
            self.instance.save()
            return self.instance

        user = User.objects.create_user(username=username, password=password1, email=email)
        profile = user.profile
        profile.ficha = ficha
        profile.save()
        return profile


class CandidacyForm(forms.ModelForm):
    class Meta:
        model = Candidacy
        fields = ['name', 'role', 'ficha', 'description', 'proposals', 'profile_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'proposals': forms.Textarea(attrs={'rows': 3}),
            'ficha': forms.TextInput(attrs={'placeholder': 'Ficha solo para voceros y subvoceros'}),
        }


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['voter', 'candidacy']

    def clean(self):
        cleaned_data = super().clean()
        candidacy = cleaned_data.get('candidacy')
        if candidacy:
            cleaned_data['role'] = candidacy.role
        return cleaned_data

    def save(self, commit=True):
        vote = super().save(commit=False)
        vote.role = self.cleaned_data.get('role')
        if commit:
            vote.save()
        return vote
