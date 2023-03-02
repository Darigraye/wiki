from django.contrib.auth import forms
from django import forms as fms

from .models import User, Profile


class CustomUserCreationForm(forms.UserCreationForm):
    username = fms.CharField(label='Логин',
                             widget=fms.TextInput(attrs={'class': 'form-input'}))
    email = fms.EmailField(label='Введите адрес вашей электронной почты',
                           widget=fms.EmailInput())
    password1 = fms.CharField(label='Пароль',
                              widget=fms.PasswordInput(attrs={'class': 'form-input'}),
                              )
    password2 = fms.CharField(label='Подтвердите пароль',
                              widget=fms.PasswordInput(attrs={'class': 'form-input'}),
                              )

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = ('username', 'email')


class CustomUserChangePasswordForm(forms.PasswordChangeForm):
    class Meta:
        model = User
        fields = ('username', 'old_password', 'new_password1', 'new_password2')


class CustomUserLoginForm(forms.AuthenticationForm):
    username = fms.CharField(label='Логин',
                             widget=fms.TextInput(attrs={'class': 'form-input'}))
    password = fms.CharField(label='Пароль',
                             widget=fms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password')
