from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
import time


class TestNewUser(FunctionalTest):
    def test_user_can_access_homepage(self):
        # The person running the tournament goes to the website,
        # as no tombola is running they have the option to start one
        self.browser.get(self.live_server_url)

        # They notice that tombola is in the title of the webpage
        self.assertIn("Tombola", self.browser.title)
        self.assertIn(
            "Toby's Tombola", self.browser.find_element_by_tag_name("h1").text
        )

        # They are invited to start a new tombola and enter a time limit
        # They enter 3 into the box and hit enter
        inputbox = self.browser.find_element_by_id("id_time_limit")
        inputbox.send_keys(3)
        inputbox.send_keys(Keys.ENTER)

        # The game takes them to a new screen showing the Tombola is in progress
        self.wait_for(
            lambda: self.assertRegex(self.browser.current_url, "tombolas/.+",)
        )

        # The game takes them to a new screen showing the Tombola is in progress

        # The game displays that the tombola is in progress
        self.assertIn(
            "in progress", self.browser.find_element_by_id("in_progress").text
        )
        # The game displays how many minutes and seconds there are left
        self.assertIn(
            "second", self.browser.find_element_by_tag_name("html").text
        )
        self.assertIn(
            "minute", self.browser.find_element_by_tag_name("html").text
        )
        time.sleep(3)

        # After the time limit has elapsed, they refresh the page
        self.browser.refresh()
        # The page shows that the tombola has finished
        self.wait_for(
            lambda: self.assertIn(
                "Finished", self.browser.find_element_by_id("finished").text,
            )
        )

    def test_user_can_buy_tickets_and_receives_correct_information(self):
        # A new Tombola is set up with a 10 second time window
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id("id_time_limit")
        inputbox.send_keys(10)
        inputbox.send_keys(Keys.ENTER)

        # The user can now see that the tombola is in in progress
        self.wait_for(
            lambda: self.assertRegex(self.browser.current_url, "tombolas/.+",)
        )

        # User notices an input box in which they can input the number of
        # tickets they wish to buy.
        inputbox = self.browser.find_element_by_id("id_ticket_quantity")
        inputbox.send_keys(1)
        inputbox.send_keys(Keys.ENTER)

        # The page refreshes to show their purchase was succesful
        self.wait_for(
            lambda: self.assertIn(
                "successful",
                self.browser.find_element_by_id("purchase_success").text,
            )
        )

        # The page returns the id of the ticket bought (testing table data)
        ## removing this test as it will return an unpredictable integer
        # self.assertNotIn(
        #    "<td>", self.browser.find_element_by_tag_name("table").text
        # )

        # The page returns the odds of the ticket(s) bought winning
        self.assertIn("odds", self.browser.find_element_by_tag_name("h3").text)
        # The page returns the total cost of the tickets bought
        self.assertIn(
            "total cost", self.browser.find_element_by_tag_name("h2").text
        )
