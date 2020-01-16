from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Game
from time import time
import json


def HomePage(request):
    tombolas = Game.objects.all().order_by("-id")
    return render(request, "home.html", {"tombolas": tombolas})


def NewTombola(request):
    """View creates a new tombola with a configurable amount of time"""
    error = None
    try:
        game = Game.objects.create(
            deadline=(time() + int(request.POST["time_limit"]))
        )
    except ValueError or ValidationError:
        error = "You can't start a game without a time limit"
        return render(request, "home.html", {"error": error})
    if int(request.POST["time_limit"]) < 1:
        error = "Your game must have a positive time limit"
        return render(request, "home.html", {"error": error})
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
    time_remaining = {
        "seconds": game.seconds_remaining(),
        "minutes": game.minutes_remaining(),
    }
    if request.method == "GET" or game.is_finished():
        return redirect(f"/tombolas/{game.id}")
    try:
        ticket_quantity = int(request.POST["ticket_quantity"])
    except ValueError:
        return render(
            request,
            "tombola_in_progress.html",
            {
                "error": "No ticket number entered",
                "game": game,
                "time_remaining": time_remaining,
            },
        )

    if ticket_quantity < 1:
        return render(
            request,
            "tombola_in_progress.html",
            {
                "error": "Enter a positive number of tickets",
                "game": game,
                "time_remaining": time_remaining,
            },
        )
    total_cost = game.multiple_ticket_prices(ticket_quantity)
    ticket_ids = game.buy_tickets(ticket_quantity)

    return render(
        request,
        "bought.html",
        {
            "ticket_ids": ticket_ids,
            "total_cost": total_cost,
            "ticket_odds": game.ticket_odds(len(ticket_ids)),
            "game": game,
        },
    )


def TombolaFinished(request, game_id):
    """View displays that the tombola has finished. It will handle logic for
    winning ticket"""
    game = Game.objects.get(id=game_id)
    if not game.is_finished():
        return redirect(f"/tombolas/{game.id}/")
    return render(
        request,
        "tombola_finished.html",
        {"winner": game.calculate_winner(), "game": game},
    )


@csrf_exempt
def ApiBuyTicket(request, game_id):
    game = Game.objects.get(id=game_id)
    if request.method == "GET":
        data = {"error": "use POST request"}
        return JsonResponse(data)
    if game.is_finished():
        data = {"error": "Tombola is finished"}
        return JsonResponse(data)
    incoming_data = json.loads(request.body.decode("utf-8"))
    try:
        incoming_data["ticket_quantity"]
    except ValueError:
        data = {"error": "Invalid ticket quantity"}
        return JsonResponse(data)
    if incoming_data["ticket_quantity"] < 1:
        data = {"error": "Enter postive ticket quantity"}
        return JsonResponse(data)
    ticket_quantity = incoming_data["ticket_quantity"]
    total_cost = game.multiple_ticket_prices(ticket_quantity)
    ticket_ids = game.buy_tickets(ticket_quantity)
    ticket_odds = game.ticket_odds(ticket_quantity)
    data = {
        "total_cost": total_cost,
        "ticket_ids": ticket_ids,
        "ticket_odds": ticket_odds,
    }
    return JsonResponse(data)
