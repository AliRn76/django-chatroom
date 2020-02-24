from django.shortcuts import render


def game_dino_view(request):
    return render(request, "dino.html", {})