from django.urls import path
from .views import *

urlpatterns = [
    path('register', register, name='register'),
    path('login', login, name='login'),
    # когда джанго встречает такую строку(первый параметр), то срабатывает функция из views, указанная во втором параметре
    # path('', index, name='home'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', get_category, name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:news_id>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('test/', test, name='test')
]
