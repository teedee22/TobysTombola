from django.test import TestCase
from time import time
from .models import Game, Ticket


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class NewTombolaTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/tombolas/new", data={"time_limit": 1})
        self.assertEqual(Game.objects.count(), 1)

    def test_redirects_after_POST(self):
        response = self.client.post("/tombolas/new", data={"time_limit": 5})
        new_game = Game.objects.first()
        self.assertRedirects(response, f"/tombolas/{new_game.id}/")


class ViewTombolaTest(TestCase):
    def test_uses_correct_template(self):
        game = Game.objects.create(deadline=0)
        response = self.client.get(f"/tombolas/{game.id}/")
        self.assertTemplateUsed(response, "tombola_in_progress.html")


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
