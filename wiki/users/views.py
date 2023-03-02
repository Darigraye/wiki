from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.views.generic.edit import CreateView

from django.urls import reverse_lazy
from .forms import *

from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.detail import DetailView
from .models import *

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


class RegisterUserView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class LoginUserView(LoginView):
    form_class = CustomUserLoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('users:show_profile', kwargs={'username': self.request.user.username})


class LogoutUserView(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy('users:login')
    template_name = 'users/logout.html'


class ChangeUserPasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change-password.html'
    form_class = CustomUserChangePasswordForm
    login_url = reverse_lazy('users:login')
    success_url = reverse_lazy('users:password-change-done')


class ChangeUserPasswordDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'users/password-change-done.html'


class ShowProfileView(DetailView):
    model = Profile
    template_name = 'users/user_profile.html'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'

    def get_context_data(self, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        username = user.username
        email = user.email
        rating = user.rating_author

        context = super().get_context_data(**kwargs)
        context['username'] = username
        context['email'] = email
        context['rating'] = rating

        return context

    def get_object(self, queryset=None):
        try:
            profile_obj = Profile.objects.get(user__username=self.kwargs.get('username'))
        except ObjectDoesNotExist:
            profile_obj = None

        return profile_obj


class CreateProfileView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = 'users/create_profile.html'
    login_url = reverse_lazy('users:login')
    fields = ('avatar', 'profile_description')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/reset-password-form.html'
    success_url = reverse_lazy('users:reset-password-done')


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/reset-password-complete.html'
    success_url = reverse_lazy('users:reset-password-complete')
