from django.urls import path

from . import views

urlpatterns = [
    path('', views.top, name='top'),
    path('leaderboard/', views.top, name='top'),
    path('chart/', views.top_chart, name='top_chart'),
    path('player/<str:account_id>/', views.player_by_id, name='player_by_id'),
    path('player/<str:account_id>/chart/', views.chart, name='player_chart')
]
