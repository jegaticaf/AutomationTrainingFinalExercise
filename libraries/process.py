from libraries.common import log_message, capture_page_screenshot, browser
from config import OUTPUT_FOLDER, tabs_dict
from libraries.mundialitis.mundialitis import Mundialitis
from libraries.google.google import Google
from libraries.itunes.itunes import Itunes
from libraries.onpe.onpe import Onpe

class Process():
    
    def __init__(self, credentials: dict):
        log_message("Initialization")

        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_popups": 0,
            "directory_upgrade": True,
            "download.default_directory": OUTPUT_FOLDER,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False
        }

        browser.open_available_browser(preferences = prefs)
        browser.set_window_size(1920, 1080)
        browser.maximize_browser_window()

        mundialitis = Mundialitis(browser, credentials["Mundialitis"])
        mundialitis.login()
        self.mundialits = mundialitis
        
        #google = Google(browser, {"url": "https://www.google.com/ncr"})
        #tabs_dict["Google"] = len(tabs_dict)
        #google.access_google()
        #self.google = google

        #onpe = Onpe(browser, {"url": "https://www.onpe.gob.pe/"})
        #tabs_dict["ONPE"] = len(tabs_dict)
        #onpe.access_onpe()
        #self.onpe = onpe

    def start(self):
        """
        main
        """
        self.mundialits.create_lobby()
        self.mundialits.create_new_user()
        self.mundialits.join_lobby("new_user")
        self.mundialits.login()
        self.mundialits.join_lobby("creator")
        self.mundialits.start_game()
        self.mundialits.play_game()

        #Ejercicio 2
        #matched_link = self.google.search_movie()
        #log_message("Matched Link: {}".format(matched_link))
        #tabs_dict.pop("Google")
        #itunes = Itunes(browser, {"url": matched_link})
        #self.itunes = itunes
        #self.itunes.access_itunes()
        #tabs_dict["Itunes"] = len(tabs_dict)
        #self.itunes.extract_artist_information()
        #self.itunes.create_reports()

        #self.onpe.read_input_file()
        #self.onpe.download_files()
        #self.onpe.read_pdf()

        pass
    
    def finish(self):
        log_message("DW Process Finished")
        browser.close_browser()