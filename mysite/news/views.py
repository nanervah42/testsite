from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
from news.models import News, Category
from .forms import NewsForm

class HomeNews(ListView):   # вместо index
    model = News        # определяем модель откуда беруться все данные
    template_name = 'news/index.html'   # переопределяем дефолтное название шаблона
    context_object_name = 'news'        # переопределяем дефолтное название объекта
    # extra_context = {'title': 'Главная'}    # желательно использовать только для статичных данных

    def get_context_data(self, *, object_list=None, **kwargs):  # ...для динамичных данных
        context = super().get_context_data(**kwargs)            # получаем контекст, который уже есть
        context['title'] = 'Главная страница'                   # дополняем его
        return context

    def get_queryset(self):     # правим дефолтный запрос который ~ SELECT все поля FROM таблица, без всяких условий
        return News.objects.filter(is_published=True)


class ViewNews(DetailView): # вместо view_news
    model = News
    pk_url_kwarg = 'news_id'    # для news/<int:news_id>
    template_name = 'news/view_news.html'
    context_object_name = 'news_item' # по дефолту значение object


class CreateNews(CreateView): # вместо add_news
    form_class = NewsForm   # форма из forms.py
    template_name = 'news/add_news.html'
    #т.к. в models есть get_absolute_url - джанго автоматом возвращает на этот урл, после создания новости

# def index(request):
#     news = News.objects.all()
#     # categories = Category.objects.all()  категории были переданы через пользовательский тег в news_tag.py и в html-ях
#     content = {
#         'news': news,
#         'title': 'Список новостей',
#         # 'categories': categories,
#     }
#     return render(request, template_name='news/index.html', context=content)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)  # filter возвращает несколько результатов
    # categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)  # get работает через filter но возвращает только один результат
    return render(request, 'news/category.html',
                  {'news': news, 'category': category})


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#
#     return render(request, 'news/view_news.html', {'news_item': news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)   # создаем форму из POST'a и заполняем теми данными, которые пришли
#         if form.is_valid():
#             # print(form.cleaned_data) - {'title': '123', 'content': 'sdfgsdfgdfg', 'is_published': True, 'category': <Category: Культура>}
#             # news = News.objects.create(**form.cleaned_data) # для несвязанных моделей
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
