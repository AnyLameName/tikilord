from django.urls import path

from . import views

urlpatterns = [
    path('', views.top, name='top'),
    path('region/<str:region>/', views.top, name='top_by_region'),
    path('region/<str:region>/top/<int:player_count>/', views.top, name='top_n'),
    path('region/<str:region>/top/<int:player_count>/chart/', views.top_chart, name='top_chart'),
    path('player/<str:account_id>/', views.player_by_id, name='player_by_id'),
    path('player/<str:account_id>/chart/', views.chart, name='player_chart')
]
