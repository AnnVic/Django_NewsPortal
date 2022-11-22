from django.contrib import admin
from news.models import Category, Article, Profile
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published',
                    'created_at', 'updated_at', 'views')
    list_filter = ('author', 'is_published', 'views', 'created_at')
    ordering = ('is_published', )
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Profile)
