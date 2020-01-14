from django.test import TestCase
from tombola.models import Game, Ticket
from time import time


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
    def test_uses_correct_template_in_progress(self):
        game = Game.objects.create(deadline=(time() + 100))
        response = self.client.get(f"/tombolas/{game.id}/")
        self.assertTemplateUsed(response, "tombola_in_progress.html")

    def test_uses_correct_template_when_finished(self):
        game = Game.objects.create(deadline=(time() - 1))
        response = self.client.get(f"/tombolas/{game.id}/")
        self.assertTemplateUsed(response, "tombola_finished.html")
