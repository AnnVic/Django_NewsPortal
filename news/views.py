from django.shortcuts import render, redirect
from news.models import Category, Article
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
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


def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('news:home')
        messages.error(
            request, 'Unsuccessful registration. Invalid information.')
    form = NewUserForm()
    return render(request=request, template_name='news/register.html', context={'register_form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('news:home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request=request, template_name='news/login.html', context={'login_form': form})


def logout_request(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('news:home')


@login_required
def profile(request):
    return render(request, 'news/profile.html')
