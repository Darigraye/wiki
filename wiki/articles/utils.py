from django.urls import reverse_lazy
from .models import Articles

menu = ({'title': 'Вход', 'url_name': 'users:login'},
        {'title': 'Изменить пароль', 'url_name': 'users:password-change'})


class MenuMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['user'] = self.request.user
        context['profile_url'] = reverse_lazy('users:show_profile',
                                              kwargs={'username': self.request.user.username})
        return context


class DataListMixin:
    model = Articles
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False
