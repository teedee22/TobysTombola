from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class GameAndTicketValidation(FunctionalTest):
    def test_cannot_add_empty_tombola_time_or_ticket_number(self):
        # User goes to the home page and accidentally tries to start a new
        # tombola with a blank time limit She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("id_time_limit").send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that the time limit cannot be blank
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_id("error").text,
                "You must enter a valid time limit",
            )
        )

        # She tries again with a negative time limit, the same error appears.
        inputbox = self.browser.find_element_by_id("id_time_limit")
        inputbox.send_keys(-1)
        inputbox.send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_id("error").text,
                "You must enter a valid time limit",
            )
        )

        # She tries again with 20 seconds, which now works
        inputbox = self.browser.find_element_by_id("id_time_limit")
        inputbox.send_keys(20)
        inputbox.send_keys(Keys.ENTER)
