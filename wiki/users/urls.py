from django.urls import path
from .views import *


app_name = 'users'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('password-change/', ChangeUserPasswordView.as_view(),
         name='password-change'),
    path('password-change-done/', ChangeUserPasswordDoneView.as_view(), name='password-change-done'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('reset-password-form/', UserPasswordResetView.as_view(), name='reset-password-form'),
    path('reset-password-done/', PasswordResetDoneView.as_view(template_name='users/password-reset-done.html'),
         name='reset-password-done'),
    path('password_reset_confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset-password-complete', PasswordResetCompleteView.as_view(), name='reset-password-complete'),
    path('<slug:username>/', ShowProfileView.as_view(), name='show_profile')
]
