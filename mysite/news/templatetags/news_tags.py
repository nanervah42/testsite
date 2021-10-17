from django import template

from news.models import Category

register = template.Library()   # это обязательно ...

@register.simple_tag(name='get_list_categories')          # ...для этого        (name - не обязательный параметр)
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('news/list_categories.html')
def show_categories():
    categories = Category.objects.all()
    return {"categories": categories}