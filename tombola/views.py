from django.shortcuts import redirect, render
from .models import Game
from time import time


def HomePage(request):
    return render(request, "home.html")


def NewTombola(request):
    game = Game.objects.create(
        deadline=(time() + int(request.POST["time_limit"]))
    )
    return redirect(f"/tombolas/{game.id}/")


def ViewTombola(request, game_id):
    game = Game.objects.get(id=game_id)
    if time() < game.deadline:
        return render(request, "tombola_in_progress.html", {"game": game})
    else:
        return render(request, "tombola_finished.html")
