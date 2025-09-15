

## Django TechStore - Многоязычный интернет-магазин электроники

**TechStore** - это веб-приложение интернет-магазина, построенное на Django 5.1.6 с поддержкой русского и английского языков. [1](#0-0)  Система предоставляет полнофункциональный каталог товаров с иерархической структурой категорий, галереями изображений и административным интерфейсом для управления контентом. [2](#0-1) 

### Основные возможности

- **Иерархический каталог товаров**: Система категорий с неограниченной вложенностью через самоссылающуюся связь `parent` [3](#0-2) 
- **Многоязычность**: Автоматический перевод контента на русский и английский языки с использованием `django-modeltranslation` [4](#0-3) 
- **Управление товарами**: Полная информация о товарах включая цены, скидки, количество на складе и цветовые варианты [5](#0-4) 
- **Галереи изображений**: Множественные фотографии товаров с удобными методами доступа [6](#0-5) 
- **Расчет цен со скидками**: Автоматический расчет финальной цены с учетом скидок [7](#0-6) 

### Технологический стек

- **Backend**: Django 5.1.6
- **База данных**: SQLite
- **Интернационализация**: django-modeltranslation
- **Административный интерфейс**: django-jazzmin
- **Языки**: Python, HTML, CSS, JavaScript

### Структура проекта

Проект состоит из основного пакета `webstore` для конфигурации и приложения `techstore` для бизнес-логики магазина. [8](#0-7)  Модели данных включают категории товаров, сами товары, галереи изображений и модели продуктов. [9](#0-8) 

### Установка и запуск

```bash
# Клонирование репозитория
git clone https://github.com/darkyz12345/django_diploma.git
cd django_diploma

# Установка зависимостей
pip install -r requirements.txt

# Миграции базы данных
python manage.py migrate

# Запуск сервера разработки
python manage.py runserver
```

Проект готов к развертыванию и дальнейшей разработке функционала интернет-магазина. <cite/>

## Notes

Описание основано на анализе основных компонентов системы: моделей данных в `webstore/techstore/models.py`, конфигурации Django в `webstore/webstore/settings.py` и настроек интернационализации в `webstore/techstore/translation.py`. Проект представляет собой типичное Django-приложение для электронной коммерции с акцентом на многоязычность и удобство администрирования.

Wiki pages you might want to explore:
- [Overview (darkyz12345/django_diploma)](/wiki/darkyz12345/django_diploma#1)

### Citations

**File:** webstore/webstore/settings.py (L32-35)
```python
LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]
```

**File:** webstore/webstore/settings.py (L39-50)
```python
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'modeltranslation',
    'techstore',
    'users',
]
```

**File:** webstore/techstore/models.py (L10-107)
```python
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
```

**File:** webstore/techstore/translation.py (L1-10)
```python
from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)
```
