from django.contrib import admin

from .models import News, Category


class NewsAdmin(admin.ModelAdmin):  # класс редактор
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at',
                    'is_published')  # какие поля будут выводится в админке редактирования новостей
    list_display_links = ('id', 'title')    # какие поля должны быть ссылками на соответствующие записи
    search_fields = ('title', 'content')    # по каким полям можно производить поиск
    list_editable = ('is_published',)   # можно редактировать прям из админки не проваливаясь в новость (только bool?)
    list_filter = ('is_published', 'category')  # добавить поля для фильтрации в админке

class CategoryAdmin(admin.ModelAdmin):  # класс редактор
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

admin.site.register(News, NewsAdmin)  # не забыть добавить NewsAdmin (важен порядок)
admin.site.register(Category, CategoryAdmin)