from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import os

MAX_WAIT = 10


class FunctionalTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = "http://" + staging_server

    def tearDown(self):
        self.browser.quit()


class TestSetupTombola(FunctionalTest):
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
        # They enter 5 into the box and hit enter
        inputbox = self.browser.find_element_by_id("id_time_limit")
        inputbox.send_keys(5)
        inputbox.send_keys(Keys.ENTER)

        # The game takes them to a new screen showing the Tombola is in progress

        self.fail("finish the test")
