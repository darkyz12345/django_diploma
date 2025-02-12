from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
# Register your models here.

admin.site.register(GalleryProducts)
admin.site.register(ProductModel)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_ru', 'title_en', 'parent')
    list_display_links = ('pk', 'title_ru', 'title_en')
    prepopulated_fields = {'slug': ('title_ru', )}

class GalleryInline(admin.TabularInline):
    model = GalleryProducts
    fk_name = 'product'
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price', 'quantity', 'discount', 'category', 'model', 'product_image')
    list_display_links = ('pk', 'title')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (GalleryInline, )
    list_editable = ('price', 'quantity', 'discount')
    list_filter = ('category', 'model', 'discount')

    def product_image(self, obj):
        if obj.images:
            return mark_safe(f'<img src="{obj.images.first().image.url}" width="50">')
        return "No photo"

    product_image.short_description = "Фото товара"