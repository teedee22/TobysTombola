from django.test import TestCase
from time import time
from tombola.models import Game, Ticket


class GameModelAndTicketTest(TestCase):
    def test_saving_and_retrieving_tickets(self):
        game = Game(deadline=5)
        game.save()

        first_ticket = Ticket()
        first_ticket.game = game
        first_ticket.save()

        second_ticket = Ticket()
        second_ticket.game = game
        second_ticket.save()

        saved_game = Game.objects.first()
        self.assertEqual(saved_game, game)

        saved_items = Ticket.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_ticket = saved_items[0]
        second_saved_ticket = saved_items[1]
        self.assertEqual(first_saved_ticket.id, 1)
        self.assertEqual(first_saved_ticket.game, game)
        self.assertEqual(second_saved_ticket.id, 2)
        self.assertEqual(second_saved_ticket.game, game)


class GameModelTest(TestCase):
    def test_game_saves_times_and_can_retrieve_them(self):
        game = Game()
        current_time = time()
        current_time_plus_five_seconds = time() + 5
        game.deadline = round(current_time_plus_five_seconds)
        game.save()

        # Check current time is before 5 second deadline
        saved_game = Game.objects.first()
        self.assertTrue(
            saved_game.deadline == round(current_time_plus_five_seconds)
        )
        self.assertTrue(current_time < saved_game.deadline)

        # Check 6 seconds from now is past the deadline
        new_time = time() + 6
        self.assertFalse(new_time < saved_game.deadline)

    def test_is_finished_method(self):
        game = Game.objects.create(deadline=time() - 1)
        self.assertTrue(game.is_finished())
        game2 = Game.objects.create(deadline=time() + 10)
        self.assertFalse(game2.is_finished())

    def test_seconds_remaining_method(self):
        game = Game.objects.create(deadline=time() + 65)
        self.assertEqual(5, game.seconds_remaining())
        game = Game.objects.create(deadline=time() + 55)
        self.assertEqual(55, game.seconds_remaining())

    def test_minutes_remaining_method(self):
        game = Game.objects.create(deadline=time() + 365)
        game2 = Game.objects.create(deadline=time() + 55)
        self.assertEqual(6, game.minutes_remaining())
        self.assertEqual(0, game2.minutes_remaining())

    def test_tickets_bought_method(self):
        game = Game.objects.create(deadline=time() + 300)
        Ticket.objects.create(game=game)
        Ticket.objects.create(game=game)
        self.assertEqual(game.tickets_bought(), 2)

    def test_ticket_price_method(self):
        game = Game.objects.create(deadline=time() + 300)
        game2 = Game.objects.create(deadline=time() + 300)

        for i in range(1100):
            Ticket.objects.create(game=game2)

        self.assertEqual(game.current_ticket_price(), 1)
        self.assertEqual(game2.current_ticket_price(), 1.12)

    def test_ticket_odds_method(self):
        game = Game.objects.create(deadline=time() + 300)
        for i in range(100):
            Ticket.objects.create(game=game)

        self.assertEqual(game.ticket_odds(1), 1)
        self.assertEqual(game.ticket_odds(33), 33)
