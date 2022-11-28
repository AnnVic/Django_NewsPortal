from django.shortcuts import render, redirect
from news.models import Category, Article, Comment, Like
from .forms import NewUserForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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
    comments = article.comments.filter(active=True, parent__isnull=True)
    new_comment = None
    comment_form = CommentForm(data=request.POST)
    if request.method == 'POST':
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    reply = comment_form.save(commit=False)
                    reply.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.article = article

            new_comment.save()
            user = request.user

            return redirect('news:article', article.slug)
        else:
            comment_form = CommentForm()
    user = request.user
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        if user in comment.liked.all():
            comment.liked.remove(user)
        else:
            comment.liked.add(user)
        like, created = Like.objects.get_or_create(
            user=user, comment_id=comment_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
        return redirect('news:article', article.slug)
    context = {'article': article,
               'image': article.image,
               'comments': comments,
               'comment_form': comment_form,
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
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('news:profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'news/profile.html', context)


# def like_comment(request):
    qs = Comment.objects.all()
    user = request.user
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        if user in comment.liked.all():
            comment.liked.remove(user)
        else:
            comment.liked.add(user)
        like, created = Like.objects.get_or_create(
            user=user, comment_id=comment_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    return redirect('news:article', article.slug)
