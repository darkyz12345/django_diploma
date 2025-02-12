from django.shortcuts import render
from django.views.generic import ListView
from django.utils.translation import get_language
from .models import *


# Create your views here.
class ProductListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'techstore/main.html'

    def get_queryset(self):
        print(f'LANG: {get_language()}')
        return Category.objects.filter(parent=None)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        if get_language() == 'ru':
            context['title'] = 'TechStore. Магазин электроники и не только'
        else:
            print("NO")
            context['title'] = 'Tech Store. Electronics store and more'
        return context