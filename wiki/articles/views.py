from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView

from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from .models import Articles, Categories, Tags
from .forms import AddArticleForm, GetPostsByTagForm, SortArticlesForm, GetByTopicForm

from .utils import *


def likePost(request, postname):
    post = get_object_or_404(Articles, slug=postname)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('show_post', args=(postname, )))


class HomePage(MenuMixin, TemplateView):
    template_name = 'articles/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        additional_context = super().get_user_context()

        return dict(list(context.items()) + list(additional_context.items()))


class DisplayArticles(LoginRequiredMixin, DataListMixin, MenuMixin, ListView, FormView):
    template_name = 'articles/articles.html'
    form_class = SortArticlesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = super().get_user_context()

        context['form_search'] = GetByTopicForm()

        return dict(list(context.items()) + list(additional_context.items()))

    def get_queryset(self):
        topic_name = self.request.GET.get('topic')
        sort_param = self.request.GET.get('sorting')

        articles = Articles.objects.all()

        if topic_name:
            print(topic_name)
            articles = articles.filter(topic__regex=rf'{topic_name}')

        if sort_param:
            articles = articles.order_by(f'-{sort_param}')

        return articles


class CreateArticle(LoginRequiredMixin, MenuMixin, CreateView):
    form_class = AddArticleForm
    template_name = 'articles/add_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = super().get_user_context()

        return dict(list(context.items()) + list(additional_context.items()))


class ShowArticle(LoginRequiredMixin, MenuMixin, DetailView):
    model = Articles
    template_name = 'articles/show_post.html'
    slug_url_kwarg = 'postname'
    context_object_name = 'post'
    http_method_names = ('get', 'post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = super().get_user_context()

        likes_connected = get_object_or_404(Articles, slug=self.kwargs.get('postname'))
        liked = False

        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['number_likes'] = likes_connected.likes.count()
        context['post_is_liked'] = liked

        return dict(list(context.items()) + list(additional_context.items()))

    def get_object(self, queryset=None):
        displayed_object = super().get_object(queryset)
        if displayed_object is not None:
            displayed_object.update_number_views()

        return displayed_object


class ShowCategory(LoginRequiredMixin, DataListMixin, MenuMixin, ListView):
    template_name = 'articles/show_categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        additional_context = super().get_user_context()

        return dict(list(context.items()) + list(additional_context.items()))

    def get_queryset(self):
        category = self.kwargs.get('name')
        return Articles.objects.filter(category__name=category)


class ShowByTag(LoginRequiredMixin, DataListMixin, MenuMixin, ListView, FormView):
    template_name = 'articles/show_by_tag.html'
    form_class = GetPostsByTagForm
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['get_parameter_exists'] = self.request.GET
        additional_context = super().get_user_context()

        return dict(list(context.items()) + list(additional_context.items()))

    def get_queryset(self):
        if 'name_tag' in self.request.GET:
            tag = self.request.GET.get('name_tag')
            return Articles.objects.filter(tags__name_tag=tag)


class ArticleUpdateView(UpdateView):
        model = Articles
        template_name_suffix = '_update_form'
        slug_url_kwarg = 'postname'
        fields = ('content', 'photo')
