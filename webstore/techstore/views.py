from django.shortcuts import render
from django.views.generic import ListView
from .models import *


# Create your views here.
class ProductListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'techstore/main.html'
    extra_context = {
        'title': 'TechStore. Магазин электроники и не только'
    }

    def get_queryset(self):
        return Category.objects.filter(parent=None)