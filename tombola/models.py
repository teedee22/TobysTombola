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
        return round(self.deadline - time()) % 6

    def minutes_remaining(self):
        """Checks how many mins are remaining"""
        return math.floor((self.deadline - time()) / 60)


class Ticket(models.Model):
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
