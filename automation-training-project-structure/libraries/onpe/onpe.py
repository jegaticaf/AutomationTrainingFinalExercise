from email import header
from libraries.common import log_message, capture_page_screenshot, act_on_element, files, check_file_download_complete, file_system, pdf
from config import OUTPUT_FOLDER, tabs_dict
import random

class Onpe():

    def __init__(self, rpa_selenium_instance, credentials:dict):
        self.browser = rpa_selenium_instance
        self.onpe_url = credentials["url"]
        self.excel_data_dict_list = []
    
    def access_onpe(self):
        """
        Access Onpe from the browser
        """
        log_message("Start - Access Onpe")

        self.browser.go_to(self.onpe_url)

        log_message("End - Access Onpe")

    def read_input_file(self):
        """
        Read the data from the input file received
        """
        log_message("Start - Read Input File")

        files.open_workbook("Files_To_Download.xlsx")
        excel_data_dict_list = files.read_worksheet(name = "Sheet1", header=True)
        files.close_workbook()
        self.excel_data_dict_list = excel_data_dict_list

        log_message("End - Read Input File")
    
    def download_files(self):
        """
        Downloads files from ONPE
        """
        log_message("Start - Download Files")

        act_on_element('//a[@alt = "Resoluciones"]', "click_element")
        document_elements = act_on_element('//div[@class = "pdf"]//a', "find_elements")
        documents_to_download = []

        for excel_data_dict in self.excel_data_dict_list:
            if excel_data_dict["Download Required"].strip().upper() == "YES":
                documents_to_download.append(excel_data_dict["Name"].strip().upper())
        
        for document_element in document_elements:
            onpe_file_name = document_element.text.strip().upper()
            if onpe_file_name in documents_to_download:
                act_on_element(document_element, "click_element")
                check_file_download_complete("pdf")

        log_message("End - Download Files")     

    def read_pdf(self):
        """
        Read Pdf File
        """   
        log_message("Start - Read PDF")

        files_downloaded = file_system.find_files("{}/RJ-2790*.{}".format(OUTPUT_FOLDER, "pdf"))
        for file_downloaded in files_downloaded:
            text_dict = pdf.get_text_from_pdf(file_downloaded)
            pages_amount = len(text_dict)
            last_page_text = text_dict[pages_amount]
            print("---------------")
            print(last_page_text)
            print("---------------")

        content_data = "Amount of Pages:" + "\n" + str(pages_amount)
        file_system.create_file("{}/Pages_Amount.txt".format(OUTPUT_FOLDER), content=content_data, encoding = "utf-8", overwrite = True)
        file_content = file_system.read_file("{}/Pages_Amount.txt".format(OUTPUT_FOLDER), encoding = "utf-8")
        print(""+file_content)
        log_message("End - Read PDF")        