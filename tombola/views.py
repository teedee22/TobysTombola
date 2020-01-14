from django.shortcuts import redirect, render
from .models import Game
from time import time


def HomePage(request):
    return render(request, "home.html")


def NewTombola(request):
    """View creates a new tombola with a configurable amount of time"""
    game = Game.objects.create(
        deadline=(time() + int(request.POST["time_limit"]))
    )
    return redirect(f"/tombolas/{game.id}/")


def ViewTombola(request, game_id):
    """View decides if game is in progress or finished"""
    game = Game.objects.get(id=game_id)
    if game.is_finished():
        return redirect(f"/tombolas/{game.id}/finished/")
    else:
        return redirect(f"/tombolas/{game.id}/inprogress/")


def TombolaInProgress(request, game_id):
    """View calculates how much time is left and pass it to template"""
    game = Game.objects.get(id=game_id)
    if game.is_finished():
        return redirect(f"/tombolas/{game.id}/")
    time_remaining = {
        "seconds": game.seconds_remaining,
        "minutes": game.minutes_remaining,
    }

    return render(
        request,
        "tombola_in_progress.html",
        {"game": game, "time_remaining": time_remaining},
    )


def TombolaFinished(request, game_id):
    """View displays that the tombola has finished. It will handle logic for
    winning ticket"""
    game = Game.objects.get(id=game_id)
    if not game.is_finished():
        return redirect(f"/tombolas/{game.id}/")
    return render(request, "tombola_finished.html")
