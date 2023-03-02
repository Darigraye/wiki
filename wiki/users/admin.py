from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.utils.html import mark_safe

from .models import User, Profile
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    save_on_top = True
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', 'username', 'user_type', 'rating_author')
    list_display_links = ('username',)
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')


class ProfileAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('user', 'get_html_photo', 'profile_description')
    list_display_links = ('user',)
    fields = ('get_html_photo', 'profile_description')
    readonly_fields = ('user', 'get_html_photo')

    def get_html_photo(self, subject):
        if subject.avatar:
            return mark_safe(f"<img src='{subject.avatar.url}' width=50>'")
        else:
            return 'Нет фото'

    get_html_photo.short_description = 'Фото'


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
