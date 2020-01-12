from django.urls import path

from .views import (
    PlayGameView, results
)

app_name = 'game'

urlpatterns = [
    path('', PlayGameView.as_view(), name='play'),
]