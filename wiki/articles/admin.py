from django.utils.html import mark_safe

from django.contrib import admin
from .models import *


class ArticlesAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('topic', 
                    'get_html_photo',
                    'time_create', 
                    'time_update', 
                    'author',
                    'number_views')
    list_display_links = ('topic', 'author')
    search_fields = ('topic', 'author')
    readonly_fields = ('time_create', 'time_update', 'author')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>'")
        else:
            return 'Нет фото'

    get_html_photo.short_description = 'Фото'


class CategoriesAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)


class TagsAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name_tag', )
    list_display_links = ('name_tag',)
    search_fields = ('name_tag',)


admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Tags, TagsAdmin)

admin.site.site_title = 'Админ-панель wiki'
admin.site.site_header = 'Админ-панель wiki'
