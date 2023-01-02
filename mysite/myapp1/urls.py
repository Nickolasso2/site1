from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(index), name='all_category'),
    path('2/', index2),
    #path('category/<int:a_tag>/', get_category, name='choosen_category'),
    path('category/<int:a_tag>/', NewsCategory.as_view(context_object_name='news_class'),name='choosen_category'),
    #path('news/<int:news_id>/', get_full_news, name='full_news'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='full_news'),
    path('add_news/', add_news, name='add_news'),
    # path('add_categ/', add_category, name='add_category'),
    path('add_categ/', CreateCategory.as_view(), name='add_category'),
    path('register/', register, name='register'),
    path('log_in/', log_in, name='log_in'),
    path('log_out/', log_out, name='log_out'),
    path('sending_mail/', mail_sending, name='sending_mail')
    
]
