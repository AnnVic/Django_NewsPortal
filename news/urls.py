from django.urls import path
from news import views
from .views import *

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:slug>/', views.article_detail, name='article'),
    path('category/<slug:slug>/', views.category_content, name='category'),
]
