from distutils.spawn import find_executable
from logging import raiseExceptions
from re import search
from libraries.common import log_message, capture_page_screenshot, act_on_element
from config import OUTPUT_FOLDER
import random
from selenium.webdriver.common.keys import Keys

class Google():

    def __init__(self, rpa_selenium_instance, credentials:dict):
        self.browser = rpa_selenium_instance
        self.google_url = credentials["url"]

    def access_google(self):
        """
        Access Google from the browser
        """
        log_message("Start - Access Google")

        self.browser.go_to(self.google_url)        

        try:
            act_on_element('//button[child::div[text()= "I agree"]]', "click_element", 2)
        except:
            pass
        log_message("End - Access Google")
    
    def search_movie(self):
        """
        Searches for the movie "The Lord of the Rings: The Return of the King"
        """
        log_message("Start - Search Movie")

        search_bar = act_on_element('//input[@class="gLFyf gsfi"]', "find_element")
        self.browser.input_text_when_element_is_visible('//input[@class="gLFyf gsfi"]', "The Lord of the Rings: The Return of the King itunes movie us")
        search_bar.send_keys(Keys.ENTER)
        matched_link = act_on_element('//a[contains(@href, "itunes.apple.com") and not(contains(@href, "translate")) and not(contains(@href, "google"))]', "find_elements")[0].get_attribute("href")

        log_message("End - Search Movie")
        return matched_link