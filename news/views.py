from django.shortcuts import render, get_list_or_404, get_object_or_404
from news.models import Category, Article
from django.views.generic import ListView, DetailView
# Create your views here.


def home(request):
    categories = Category.objects.all()
    articles = Article.objects.filter(
        is_published=True).order_by('-created_at')
    context = {
        'categories': categories,
        'articles': articles,
    }
    return render(request, 'news/index.html', context)


def category_content(request, slug):
    category = Category.objects.get(slug=slug)
    articles = Article.objects.all()
    context = {
        'articles': articles,
        'category': category,

    }
    return render(request, 'news/category.html', context)


def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    if article:
        article.update_views()

    context = {'article': article,
               'image': article.image,
               }
    return render(request, 'news/article.html', context)
