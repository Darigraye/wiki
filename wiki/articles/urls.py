from django.urls import path
from .views import *


urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('articles/', DisplayArticles.as_view(), name='display_articles'),
    path('update/<slug:postname>/', ArticleUpdateView.as_view(), name='update_article'),
    path('add_post/', CreateArticle.as_view(), name='create_article'),
    path('categories/<slug:name>/', ShowCategory.as_view(), name='show_category'),
    path('tags/', ShowByTag.as_view(), name='show_by_tag'),
    path('show_post_like/<slug:postname>/', likePost, name='show_post_like'),
    path('<slug:postname>/', ShowArticle.as_view(), name='show_post'),
]
