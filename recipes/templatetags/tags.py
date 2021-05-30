from django import template
from recipes.models import Tag

register = template.Library()

@register.inclusion_tag('recipes/tags_tpl.html')
def show_tags():
    tags = Tag.objects.all()
    return {"tags": tags}