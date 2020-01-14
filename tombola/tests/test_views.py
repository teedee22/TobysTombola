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
        response = self.client.post(
            "/tombolas/new", data={"time_limit": 5}, follow=True
        )
        new_game = Game.objects.first()
        self.assertRedirects(response, f"/tombolas/{new_game.id}/inprogress/")


class ViewTombolaTest(TestCase):
    def test_redirects_to_in_progress(self):
        game = Game.objects.create(deadline=(time() + 100))
        response = self.client.get(f"/tombolas/{game.id}/")
        self.assertRedirects(response, f"/tombolas/{game.id}/inprogress/")

    def test_redirects_to_finished_when_finished(self):
        game = Game.objects.create(deadline=(time() - 1))
        response = self.client.get(f"/tombolas/{game.id}/")
        self.assertRedirects(response, f"/tombolas/{game.id}/finished/")


class TombolaInProgressTest(TestCase):
    def test_calculates_and_displays_seconds_and_minutes_correctly(self):
        game = Game.objects.create(deadline=time() + 65)
        response = self.client.get(f"/tombolas/{game.id}/inprogress/")
        self.assertContains(response, "1 minute")
        self.assertContains(response, "seconds")

    def test_uses_correct_template(self):
        game = Game.objects.create(deadline=time() + 60)
        response = self.client.get(f"/tombolas/{game.id}/inprogress/")
        self.assertTemplateUsed(response, "tombola_in_progress.html")

    def test_redirects_if_deadline_has_passed(self):
        game = Game.objects.create(deadline=time() - 1)
        response = self.client.get(
            f"/tombolas/{game.id}/inprogress/", follow=True
        )
        self.assertRedirects(response, f"/tombolas/{game.id}/finished/")


class BuyTicketTest(TestCase):
    def test_uses_correct_template_after_POST(self):
        game = Game.objects.create(deadline=time() + 10)
        response = self.client.post(
            f"/tombolas/{game.id}/buy/",
            data={"ticket_quantity": 1},
            follow=True,
        )
        self.assertTemplateUsed(response, "bought.html")

    def test_returns_ticket_single_id(self):
        game = Game.objects.create(deadline=time() + 10)
        response = self.client.post(
            f"/tombolas/{game.id}/buy/",
            data={"ticket_quantity": 1},
            follow=True,
        )
        self.assertContains(response, 1)

    def test_returns_multiple_ticket_ids(self):
        game = Game.objects.create(deadline=time() + 10)
        response = self.client.post(
            f"/tombolas/{game.id}/buy/",
            data={"ticket_quantity": 5},
            follow=True,
        )
        for ticket in range(5):
            self.assertContains(response, ticket + 1)


class TombolaFinishedTest(TestCase):
    def test_redirects_if_deadline_has_not_passed(self):
        game = Game.objects.create(deadline=time() + 60)
        response = self.client.get(
            f"/tombolas/{game.id}/finished/", follow=True
        )
        self.assertRedirects(response, f"/tombolas/{game.id}/inprogress/")

    def test_uses_correct_template(self):
        game = Game.objects.create(deadline=time() - 1)
        response = self.client.get(f"/tombolas/{game.id}/finished/")
        self.assertTemplateUsed(response, "tombola_finished.html")
