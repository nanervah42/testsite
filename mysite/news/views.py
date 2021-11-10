from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
from news.models import News, Category
from .forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin   # добавить новость могут тока зареганые (есть правки в _nav)
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserCreationForm()

    return render(request, 'news/register.html', {'form': form})


def login(request):
    return render(request, 'news/login.html')


def test(request):
    objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6', 'george7']
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})


class HomeNews(ListView):   # вместо index
    model = News        # определяем модель откуда беруться все данные
    template_name = 'news/index.html'   # переопределяем дефолтное название шаблона
    context_object_name = 'news'        # переопределяемn дефолтное название объекта
    # extra_context = {'title': 'Главная'}    # желательно использовать только для статичных данных
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):  # ...для динамичных данных
        context = super().get_context_data(**kwargs)            # получаем контекст, который уже есть
        context['title'] = 'Главная страница'                   # дополняем его
        return context

    def get_queryset(self):     # правим дефолтный запрос который ~ SELECT все поля FROM таблица, без всяких условий
        return News.objects.filter(is_published=True).select_related('category')   # select_related для уменьшения sql запросов(тема в дебаг тулз)


class ViewNews(DetailView): # вместо view_news
    model = News
    pk_url_kwarg = 'news_id'    # для news/<int:news_id>
    template_name = 'news/view_news.html'
    context_object_name = 'news_item' # по дефолту значение object


class CreateNews(LoginRequiredMixin, CreateView): # вместо add_news
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
    news = News.objects.filter(category_id=category_id).select_related('category')  # filter возвращает несколько результатов
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


