from django import forms
from .models import Articles, Tags


class AddArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Articles
        fields = ['topic', 'content', 'photo', 'category']
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }


class GetPostsByTagForm(forms.Form):
    name_tag = forms.CharField(max_length=20)


class SortArticlesForm(forms.Form):
    SORTING_CHOICES = (('rating_article', 'rating'),
                       ('number_views', 'number_views'),
                       ('time_update', 'time_update'))
    sorting = forms.ChoiceField(choices=SORTING_CHOICES,
                                widget=forms.Select(attrs={'onchange': "insertParam('sorting', "
                                                                       "document.getElementById('sorting').value);",
                                                           'id': 'sorting'}))


class GetByTopicForm(forms.Form):
    topic = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control me-2',
                                                                         'type': 'search',
                                                                         'placeholder': 'Search',
                                                                         'aria-label': 'Search',
                                                                         'id': 'topic'}))
