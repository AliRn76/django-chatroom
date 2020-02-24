from django.urls import path, include
from game.views import game_dino_view
urlpatterns = [
    path('dino', game_dino_view, name="game_dino")
    ]