from django.http import JsonResponse
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
        "seconds": game.seconds_remaining(),
        "minutes": game.minutes_remaining(),
    }

    return render(
        request,
        "tombola_in_progress.html",
        {"game": game, "time_remaining": time_remaining},
    )


def BuyTicket(request, game_id):
    """purchases tickets and displays their ids"""
    game = Game.objects.get(id=game_id)
    if request.method == "GET" or game.is_finished():
        return redirect(f"/tombolas/{game.id}")
    ticket_quantity = int(request.POST["ticket_quantity"])
    total_cost = game.multiple_ticket_prices(ticket_quantity)
    ticket_ids = game.buy_tickets(ticket_quantity)

    return render(
        request,
        "bought.html",
        {
            "ticket_ids": ticket_ids,
            "total_cost": total_cost,
            "ticket_odds": game.ticket_odds(len(ticket_ids)),
        },
    )


def ApiBuyTicket(request, game_id):
    game = Game.objects.get(id=game_id)
    if request.method == "GET" or game.is_finished():
        data = {"error": "error"}
        return JsonResponse(data)


def TombolaFinished(request, game_id):
    """View displays that the tombola has finished. It will handle logic for
    winning ticket"""
    game = Game.objects.get(id=game_id)
    if not game.is_finished():
        return redirect(f"/tombolas/{game.id}/")
    return render(
        request, "tombola_finished.html", {"winner": game.calculate_winner()}
    )
