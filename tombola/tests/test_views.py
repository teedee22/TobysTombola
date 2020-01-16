from django.test import TestCase
from django.utils.html import escape
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

    def test_validation_errors_end_up_on_home_page(self):
        response = self.client.post(f"/tombolas/new", data={"time_limit": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        expected_error = escape("You can't start a game without a time limit")
        self.assertContains(response, expected_error)


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

    def test_validation_errors_end_up_on_inprogress_page(self):
        game = Game.objects.create(deadline=time() + 30)
        response = self.client.post(
            f"/tombolas/{game.id}/buy",
            data={"ticket_quantity": ""},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tombola_in_progress.html")


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

    def test_returns_ticket_odds(self):
        game = Game.objects.create(deadline=time() + 10)
        Ticket.objects.create(game=game)
        response = self.client.post(
            f"/tombolas/{game.id}/buy/",
            data={"ticket_quantity": 3},
            follow=True,
        )
        self.assertContains(response, "75.0%")

    def test_returns_ticket_prices(self):
        game = Game.objects.create(deadline=time() + 10)
        response = self.client.post(
            f"/tombolas/{game.id}/buy/",
            data={"ticket_quantity": 102},
            follow=True,
        )
        self.assertContains(response, "£102.01")

    def test_cannot_buy_if_game_is_finished(self):
        game = Game.objects.create(deadline=time() - 1)
        response = self.client.post(
            f"/tombolas/{game.id}/buy/",
            data={"ticket_quantity": 102},
            follow=True,
        )

        self.assertRedirects(response, f"/tombolas/{game.id}/finished/")

    def test_GET_redirects(self):
        game = Game.objects.create(deadline=time() + 30)
        response = self.client.get(f"/tombolas/{game.id}/buy/", follow=True,)

        self.assertRedirects(response, f"/tombolas/{game.id}/inprogress/")


class TombolaFinishedTest(TestCase):
    def test_redirects_if_deadline_has_not_passed(self):
        game = Game.objects.create(deadline=time() + 60)
        response = self.client.get(
            f"/tombolas/{game.id}/finished/", follow=True
        )
        self.assertRedirects(response, f"/tombolas/{game.id}/inprogress/")

    def test_uses_correct_template(self):
        game = Game.objects.create(deadline=time() - 1)
        response = self.client.get(f"/tombolas/{game.id}/finished/", data={})
        self.assertTemplateUsed(response, "tombola_finished.html")

    def test_displays_winning_ticket(self):
        game = Game.objects.create(deadline=time())
        Ticket.objects.create(game=game)
        response = self.client.get(f"/tombolas/{game.id}/finished/")
        self.assertContains(response, "1")


class ApiBuyTicketTest(TestCase):
    def test_GET_produces_error(self):
        game = Game.objects.create(deadline=time() + 30)
        response = self.client.get(f"/api/tombolas/{game.id}/buy", follow=True)
        self.assertContains(response, "error")

    def test_finished_game_produces_error(self):
        game = Game.objects.create(deadline=time() - 1)
        response = self.client.post(
            f"/api/tombolas/{game.id}/buy", follow=True
        )
        self.assertContains(response, "error")

    def test_accepts_post(self):
        game = Game.objects.create(deadline=time() + 10)
        response = self.client.post(
            f"/api/tombolas/{game.id}/buy/",
            data={"ticket_quantity": 3},
            content_type="application/json",
            follow=True,
        )
        self.assertContains(response, 3)

    def test_negative_tickets_raises_error(self):
        game = Game.objects.create(deadline=time() + 10)
        response = self.client.post(
            f"/api/tombolas/{game.id}/buy/",
            data={"ticket_quantity": -3},
            content_type="application/json",
            follow=True,
        )
        self.assertContains(response, "error")
