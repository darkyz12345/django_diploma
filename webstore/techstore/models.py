from django.utils.text import slugify
from googletrans import Translator

from django.db import models
from django.urls import reverse_lazy


# Create your models here.

class Category(models.Model):
    title_ru = models.CharField(max_length=150, verbose_name='Категория на русском')
    title_en = models.CharField(max_length=150, verbose_name='Категория на английском', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, verbose_name='Слаг')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='subcategories', verbose_name='Родитель категории')

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        if not self.title_en:
            translator = Translator()
            self.title_en = translator.translate(self.title_ru, dest='en').text
        self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    def get_title(self, code):
        if code == 'ru':
            return self.title_ru
        return self.title_en

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
