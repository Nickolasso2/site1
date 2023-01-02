from django import template
from myapp1.models import Category
from django.db.models import Count, F, Q

register = template.Library()

@register.simple_tag
def get_categories():
    # returns only categories with news published
    
    return Category.objects.annotate(news_number=Count('news', filter=F('news__is_published'))).filter( news_number__gt=0)

    

@register.inclusion_tag('myapp1/sidebar2.html')
def show_categories(arg1='Hello,', arg2 = 'world'):
    categories = Category.objects.all()
    return {'categories':categories, 'arg1':arg1, 'arg2':arg2}