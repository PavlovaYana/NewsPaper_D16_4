from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from .models import Post, Category, Author
from django import forms


class PostFilter(FilterSet):
    date = DateFilter(field_name="time_of_creation", widget=forms.DateInput(attrs={'type': "date"}),
                      label='Дата', lookup_expr='date__gte')

    class Meta:
        model = Post
        fields = {

            'title': ['icontains'],
            'author': ['in']

        }