from django.urls import path

from .views import (PlayGameView)

app_name = 'game'

urlpatterns = [
    path('', PlayGameView.as_view(), name='play'),
]