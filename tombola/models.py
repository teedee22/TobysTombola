from django.db import models
from time import time
import math
import random


class Game(models.Model):
    deadline = models.IntegerField()
    winner = models.IntegerField(null=True)

    def is_finished(self) -> bool:
        """Checks to see if the tombola has passed the deadline"""
        if time() > self.deadline:
            return True

    def seconds_remaining(self) -> int:
        """checks how many seconds are remaining"""
        return round(self.deadline - time()) % 60

    def minutes_remaining(self) -> int:
        """Checks how many mins are remaining"""
        return math.floor((self.deadline - time()) / 60)

    def tickets_bought(self) -> int:
        """Totals up number of tickets bought for given game"""
        return Ticket.objects.filter(game=self).count()

    def current_ticket_price(self) -> int:
        """calculates ticket price"""
        if self.tickets_bought() < 101:
            return 1
        compound = self.tickets_bought() // 100
        return round(1.01 ** compound, 2)

    def ticket_odds(self, ticket_quantity: int) -> int:
        """calculates players odds so far of winning"""
        return round((ticket_quantity / self.tickets_bought()) * 100, 2)

    def multiple_ticket_prices(self, quantity: int) -> int:
        """Calculates total cost of tickets bought"""
        tickets_bought = self.tickets_bought()
        total_cost = 0
        for i in range(quantity):
            if tickets_bought < 101:
                total_cost += 1
            else:
                compound = tickets_bought // 100
                total_cost += 1.01 ** compound
            tickets_bought += 1
        return round(total_cost, 2)

    def calculate_winner(self) -> int:
        """returns a winning ticket or calculates and returns ticket if not
        already calculated"""
        if not self.winner:
            all_tickets = Ticket.objects.filter(game=self)
            # Check tickets were bought
            if len(all_tickets) > 1:
                self.winner = random.choice(
                    [ticket.id for ticket in all_tickets]
                )
                self.save()
        return self.winner

    def buy_tickets(self, ticket_quantity: int) -> list:
        """Buy multiple tickets and return a list of their ids"""
        ticket_ids = []
        for ticket in range(ticket_quantity):
            new_ticket = Ticket.objects.create(game=self)
            ticket_ids.append(new_ticket.id)
        return ticket_ids


class Ticket(models.Model):
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
