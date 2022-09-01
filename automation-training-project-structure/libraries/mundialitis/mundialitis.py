from cmath import log
from distutils.spawn import find_executable
from logging import raiseExceptions
from libraries.common import log_message, capture_page_screenshot, act_on_element
from config import OUTPUT_FOLDER
import random, os

class Mundialitis():

    def __init__(self, rpa_selenium_instance, credentials: dict):
        self.browser = rpa_selenium_instance
        self.mundialitis_url = credentials["url"]
        self.mundialitis_login = credentials["login"]
        self.mundialitis_password = credentials["password"]
        self.lobby = ""
    
    def login(self):
        """
        Login with Bitwarden credentials to Mundialitis
        """
        try:
            self.browser.go_to(self.mundialitis_url)
            #self.browser.click_element()
            act_on_element('//a[text()="LOGIN"]', "click_element")
            self.browser.input_text_when_element_is_visible('//input[@id="logusername"]', self.mundialitis_login)
            self.browser.input_text_when_element_is_visible('//input[@id="logpassword"]', self.mundialitis_password)
            act_on_element('//button[@name="login"]', "click_element")
            act_on_element('//div[@id="main"]', "find_element")

        except Exception as ex:
            log_message(str(ex))
            capture_page_screenshot(OUTPUT_FOLDER, "Exception_Mundialitis_Login")
            raise Exception("Login to Mundialitis Failed")
    
    def create_lobby(self):
        """
        Create a new lobby for the trivia page
        """
        #new_lobby = "AutomationTrainingEnriqueUpload"
        new_lobby = os.environ.get("LOBBY_NAME", "ATEnrique")
        act_on_element('//a[@href="/trivialobbies"]', "click_element")
        act_on_element('//button[text()="CREAR LOBBY"]', "click_element")
        self.browser.input_text_when_element_is_visible('//input[@id="lobbyname"]', new_lobby)
        self.browser.input_text_when_element_is_visible('//input[@id="lobbypassword"]', new_lobby)
        self.browser.input_text_when_element_is_visible('//input[@id="lobbymoney"]', "500")
        act_on_element('//button[@name="createlobby" and @type="submit"]', "click_element")
        self.lobby = new_lobby
        log_message("End - Create Lobby")

    def create_new_user(self):
        """
        Function that registers a new user
        """
        log_message("Start - Register New User")
        #new_user = "AutomationTrainingUserEnriqueUpload"
        new_user = os.environ.get("NEW_USER_NAME", "ATEnrique")
        self.browser.go_to(self.mundialitis_url)

        self.browser.input_text_when_element_is_visible('//input[@id = "rusername"]', new_user)
        self.browser.input_text_when_element_is_visible('//input[@id = "rpassword"]', new_user)
        self.browser.input_text_when_element_is_visible('//input[@id = "rpassword2"]', new_user)
        act_on_element('//button[@name="register" and @type="submit"]', "click_element")

        self.browser.input_text_when_element_is_visible('//input[@id = "rfirstname"]', "Automation")
        self.browser.input_text_when_element_is_visible('//input[@id = "rlastname"]', "Training")
        self.browser.input_text_when_element_is_visible('//input[@id = "remail"]', "Automation@training.com")
        self.browser.input_text_when_element_is_visible('//input[@id = "raddress"]', "Automation Training Adress")

        act_on_element('//select[@id="rcountry"]', "click_element")
        act_on_element('//select[@id="rcountry"]/option[@value = "México"]', "click_element")

        self.browser.input_text_when_element_is_visible('//input[@id = "rmoney"]', "500")

        act_on_element('//button[@name="cmpregister" and @type="submit"]', "click_element")

        act_on_element('//div[@id="main"]', "find_element")

        log_message("End - Register New User")

    def join_lobby(self, mode: str):
        """
        Function that joins an especific lobby
        """
        log_message("Start - Join Lobby")
        act_on_element('//a[@href="/trivialobbies"]', "click_element")

        if mode == "creator":
            act_on_element('//li[@class="list-group-item"]/a[text()="{}"]'.format("{} - Unido".format(self.lobby)), "click_element")
        else:
            act_on_element('//li[@class="list-group-item"]/a[text()="{}"]'.format(self.lobby), "click_element")
            self.browser.input_text_when_element_is_visible('//input[@id="lobbypassword"]', self.lobby)
            act_on_element('//button[@id="accesslobby"]', "click_element")
            act_on_element('//button[@id="joinlobby"]', "click_element")

        log_message("End - Join Lobby")
    
    def start_game(self):
        """
        Function that starts the game with the user that created the lobby
        """
        log_message("Start - Start Game")
        act_on_element('//button[@id="setup" and text()="INICIAR JUEGO"]', "click_element")

        act_on_element('//button[@id="begin3" and @value="Difícil"]', "click_element")

        log_message("End - Start Game")
    
    def play_game(self):
        """
        Function that plays the trivia game
        """
        log_message("Start - Play Game")
        
        questions_remaining = True
        while questions_remaining:
            try:
                act_on_element('//div[@class="list-group"]', "find_element")
            except:
                questions_remaining = False
            else:
                answer_elements = act_on_element('//button[contains(@id, "optn") and position()>1]', "find_elements")
                selected_answer_index = random.randint(0, len(answer_elements)-1)
                act_on_element(answer_elements[selected_answer_index], "click_element")
                act_on_element('//a[@id="btnopt" and text()="Siguiente"]', "click_element")
        
        results = act_on_element('//li[@class="list-group-item"]', "find_element").text.split(": ")
        log_message("Username: {}".format(results[0]))
        log_message("Score: {}".format(results[1]))
        capture_page_screenshot(OUTPUT_FOLDER, "Mundialitis_Trivia_Results")

        log_message("End - Play Game")