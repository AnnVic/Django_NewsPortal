from django.contrib import admin
from news.models import Category, Article
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published',
                    'created_at', 'updated_at', 'views')
    list_filter = ('author', 'is_published', 'views', 'created_at')
    ordering = ('is_published', )


admin.site.register(Article, ArticleAdmin)
