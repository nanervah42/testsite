from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


from .models import News, Category


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):  # класс редактор
    form = NewsAdminForm

    list_display = ('id', 'title', 'category', 'created_at', 'updated_at',
                    'is_published', 'get_photo')  # какие поля будут выводится в админке редактирования новостей
    list_display_links = ('id', 'title')    # какие поля должны быть ссылками на соответствующие записи
    search_fields = ('title', 'content')    # по каким полям можно производить поиск
    list_editable = ('is_published',)   # можно редактировать прям из админки не проваливаясь в новость (только bool?)
    list_filter = ('is_published', 'category')  # добавить поля для фильтрации в админке
    fields = (('title', 'category'), 'content', 'photo', 'get_photo', 'is_published', 'views', 'created_at', 'updated_at') # список полей, которые нужны для внутри вывода отдельной новости
    readonly_fields = ('get_photo', 'views', 'created_at', 'updated_at') # поля, из передыдущей строки, которые нельзя редактировать

    def get_photo(self, obj):   # вывод картинки новости в админке джанго
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')  # mark_safe помечает строку как хтмл_код и не экранирует
        else:   # не обязательно
            return 'Фото не установлено'

    get_photo.short_description = 'Миниатюра'   # чтобы GET PHOTO в админке поменялось на МИНИАТЮРА
    save_on_top = True  # добавляет кнопки сохранить удалить и т.д. дополнительно СВЕРХУ


class CategoryAdmin(admin.ModelAdmin):  # класс редактор
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

admin.site.register(News, NewsAdmin)  # не забыть добавить NewsAdmin (важен порядок)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
