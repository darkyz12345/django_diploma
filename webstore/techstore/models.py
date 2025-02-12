from django.utils.text import slugify
from django.db import models
from django.urls import reverse_lazy

from .functions import translate


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Категория', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name='Слаг')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='subcategories', verbose_name='Родитель категории')

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        if not self.title_en:
            self.title_en = translate(self.title_ru, src='ru', dest='en')
        if not self.title_ru:
            self.title_ru = translate(self.title_en, src='en', dest='ru')
        self.title = self.title_ru
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

class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название товара')
    description = models.CharField(max_length=150, verbose_name='Описание товара')
    price = models.FloatField(verbose_name='Цена товара')
    quantity = models.IntegerField(verbose_name='Количество товара', default=0)
    color_name = models.CharField(max_length=20, default='белый', verbose_name='Цвет товара')
    color_code = models.CharField(max_length=10, default='FFFFFF', verbose_name='Код цвета')
    slug = models.SlugField(unique=True, null=True, verbose_name='Слаг товара')
    discount = models.FloatField(verbose_name='Скидка', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория товара')
    model = models.ForeignKey('ProductModel', on_delete=models.CASCADE, verbose_name='Модель товара')

    def get_absolute_url(self):
        ...

    def get_first_photo(self):
        if self.images:
            return self.images.first().image.url
        return ''

    def get_second_photo(self):
        images_tuple = tuple(self.images)
        if len(images_tuple) >= 2:
            return images_tuple[1].image.url
        return images_tuple[0].image.url

    def save(self, *args, **kwargs):
        self.title_ru = self.title
        self.title_en = translate(self.title, src='ru', dest='en')
        self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    @property
    def get_price(self):
        if self.discount:
            return self.price * (100 - self.discount) / 100
        return self.price

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class GalleryProducts(models.Model):
    image = models.ImageField(upload_to='products', verbose_name='Фото товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товара'

class ProductModel(models.Model):
    title = models.CharField(max_length=150, verbose_name='Модель')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
