from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('register', register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    # когда джанго встречает такую строку(первый параметр), то срабатывает функция из views, указанная во втором параметре
    # path('', index, name='home'),

    path('', HomeNews.as_view(), name='home'),
    # path('', cache_page(60)(HomeNews.as_view()), name='home'), # кэшируем главную страницу на 60 секунд

    path('category/<int:category_id>/', get_category, name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:news_id>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('contact/', contact, name='contact')
]
