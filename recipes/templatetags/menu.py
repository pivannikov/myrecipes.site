from django import template
from recipes.models import Category

register = template.Library()

@register.inclusion_tag('recipes/menu_tpl.html')
def show_menu():
    categories = Category.objects.filter(parent_id=None)
    return {"categories": categories}