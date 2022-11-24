from django.urls import path
from news import views
from .views import *

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:slug>/', views.article_detail, name='article'),
    path('category/<slug:slug>/', views.category_content, name='category'),
    path('register', views.register_request, name='register'),
    path('accounts/login', views.login_request, name='login'),
    path('accounts/logout', views.logout_request, name='logout'),
    path('users/profile/', views.profile, name='profile'),

]
