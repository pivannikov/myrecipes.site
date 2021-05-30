from django import template
from django.utils.safestring import mark_safe


register = template.Library()


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

@register.filter(name='highlight_search')
def highlight_search(text, search):
    search = str(search)
    text = str(text)
    search = search.lower()
    text = text.lower()
    highlighted = text.replace(search, '<span class="bg-warning">{}</span>'.format(search))
    return mark_safe(highlighted)
