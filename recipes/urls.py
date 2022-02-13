from django.urls import path

from .views import *


urlpatterns = [
    # path('', Start.as_view(), name='start'),
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('recipe/add-recipe/', add_post, name='add_post'),
    path('recipe/<str:slug>/', ShowPost.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
    path('favorites/', PostsByFavorites.as_view(), name='favorites'),
    path('cooked/', PostsByCooked.as_view(), name='cooked'),

]