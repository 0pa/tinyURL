from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<tiny_url>/stats/', views.get_stats, name='stats'),
    path('shorten/', views.add_new_url, name='add new url'),
    re_path('^(?P<tiny_url>[A-Za-z0-9_]{6})\/$', views.get_original_url, name='original_url')
]

