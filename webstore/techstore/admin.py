from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_ru', 'title_ru', 'parent')
    # list_display_links = ('pk', 'title_ru', 'title_en')
    prepopulated_fields = {'slug': ('title_ru', )}