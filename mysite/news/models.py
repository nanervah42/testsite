from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    # может быть ссылкой на модель или строка с именем модели.
    # если первичная модель(class Category) определена раньше - Category, если позже - 'Category'
    # null - позволяет использовать поле пустым, default - указывает значение категории, при создании записи
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"news_id": self.pk})  # view_news  - из url, которая область имен name=
                                                                  # news_id - тоже из url

    def __str__(self):
        return self.title   # чтобы было видно название новости в админке, там где оно есть

    class Meta:
        verbose_name = 'Новость'  # меняет в админке News на Новость (изменение для единственного числа)
        verbose_name_plural = 'Новости'  # тоже самое для множественного числа
        ordering = ['-created_at']  # порядок вывода в админке, можно сортировать по нескольким полям через запятую


class Category(models.Model):
    title = models.CharField(max_length=150,
                             db_index=True,
                             verbose_name='Категории',
                             )  # db_index индексирует это поле, делает более быстрым для поиска

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})  # categories - из url, которая область имен name=

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
