from django.db import models


class Game(models.Model):
    deadline = models.IntegerField()


class Ticket(models.Model):
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
