from django.db import models
from django.contrib.auth.models import AbstractUser

from django.urls import reverse
from django.core.validators import validate_slug


class User(AbstractUser):
    class Kinds(models.TextChoices):
        USUAL = 'u', 'обычный пользователь'
        PREMIUM = 'p', 'премиум пользователь'

    username = models.CharField(max_length=20,
                                unique=True,
                                validators=[validate_slug],
                                verbose_name='Имя пользователя')
    email = models.EmailField(unique=True, verbose_name='Почта email')
    user_type = models.CharField(max_length=1,
                                 choices=Kinds.choices,
                                 default=Kinds.USUAL,
                                 verbose_name='Тип пользователя')
    rating_author = models.IntegerField(default=0, verbose_name='Рейтинг автора')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'User'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile',
                                verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='photos_user/%Y/%m/%d', blank=True, verbose_name='Фото')
    profile_description = models.TextField(blank=True, verbose_name='Описание профиля')

    def get_absolute_url(self):
        return reverse('users:show_profile', kwargs={'username': self.user.username})

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = 'Profile'
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
