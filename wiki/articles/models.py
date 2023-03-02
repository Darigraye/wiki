from django.db import models
from django.urls import reverse

import autoslug


class Articles(models.Model):
    topic = models.CharField(max_length=50, unique=True, verbose_name='Тема')
    slug = autoslug.AutoSlugField(populate_from='topic', unique=True, db_index=True)
    content = models.TextField(verbose_name='Текст статьи')
    photo = models.ImageField(upload_to='photos_art/%Y/%m/%d', blank=True, verbose_name='Фото')
    time_create = models.TimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.TimeField(auto_now=True, verbose_name='Время последнего изменения')
    category = models.ForeignKey('Categories',
                                 on_delete=models.PROTECT,
                                 related_name='articles',
                                 verbose_name='Категория')
    author = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='articles', verbose_name='Автор')
    number_views = models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров')
    likes = models.ManyToManyField('users.User',
                                   related_name='likes',
                                   verbose_name='Лайки')

    def __str__(self):
        return self.topic

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'postname': self.slug})

    def update_number_views(self, *args, **kwargs):
        self.number_views = self.number_views + 1
        super().save(*args, **kwargs)

    def get_count_likes(self):
        return self.likes.count()

    class Meta:
        db_table = 'articles'
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ['topic']


class Categories(models.Model):
    name = models.CharField(max_length=15, db_index=True, verbose_name='Название категории')

    def get_absolute_url(self):
        return reverse('show_category', kwargs={'name': self.name})

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Tags(models.Model):
    name_tag = models.CharField(max_length=20, verbose_name='Название тега')
    articles = models.ManyToManyField(Articles, related_name='tags', verbose_name='Статьи')

    def __str__(self):
        return self.name_tag

    class Meta:
        db_table = 'tags'
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        