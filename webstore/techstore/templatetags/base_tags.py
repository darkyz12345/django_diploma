from django import template

from techstore.models import Category


register = template.Library()

@register.simple_tag()
def get_parent_categories():
    return Category.objects.filter(parent=None)

@register.simple_tag()
def get_children_categories(cat_slug):
    return Category.objects.get(slug=cat_slug).subcategories.all()