from django.db import models
from time import time
import math


class Game(models.Model):
    deadline = models.IntegerField()

    def is_finished(self):
        """Checks to see if the tombola has passed the deadline"""
        if time() > self.deadline:
            return True

    def seconds_remaining(self):
        """checks how many seconds are remaining"""
        return round(self.deadline - time()) % 60

    def minutes_remaining(self):
        """Checks how many mins are remaining"""
        return math.floor((self.deadline - time()) / 60)

    def tickets_bought(self):
        """Totals up number of tickets bought for given game"""
        return Ticket.objects.filter(game=self).count()

    def current_ticket_price(self):
        """calculates ticket price"""
        if self.tickets_bought() < 101:
            return 1
        compound = self.tickets_bought() // 100
        return round(1.01 ** compound, 2)

    def ticket_odds(self, ticket_quantity):
        """calculates players odds so far of winning"""
        return round((ticket_quantity / self.tickets_bought()) * 100, 2)


class Ticket(models.Model):
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
