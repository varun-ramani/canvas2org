import selenium
from selenium import webdriver
from typing import List

from utils import clean_padding_whitespace, create_datetime

class BrowserWrapper:
    def __init__(self, browser_type="Safari"):
        if browser_type == "Safari":
            self.driver: selenium.WebDriver = webdriver.Safari()

        if browser_type == "Chrome":
            self.driver: selenium.WebDriver = webdriver.Chrome()

        if browser_type == "Firefox":
            self.driver: selenium.WebDriver = webdriver.Firefox()

    def load_page(self, url: str):
        self.driver.get(url)

        self.intended_page = url

    def update_intended_page(self):
        self.intended_page = self.driver.current_url


    def was_redirected(self, update_url=False) -> bool:
        if self.driver.current_url != self.intended_page:
            ret_value = True

        else:
            ret_value = False

        if update_url:
            self.intended_page = self.driver.current_url

        return ret_value

    def wait_for_next_page(self):
        while not self.was_redirected():
            pass

    def execute_js(self, script):
        self.driver.execute_script(script)


    def get_login_fields(self):
        forms = self.driver.find_elements_by_tag_name("form")

        def find_field(form, ids, default_label):
            labels = form.find_elements_by_tag_name("label")

            return_dict = {}

            for identifier in ids:
                elements = form.find_elements_by_id(identifier)
                if len(elements) != 0:
                    return_dict['element'] = elements[0]

                    for label in labels:
                        if label.get_attribute("for") == identifier:
                            return_dict['label'] = label.text
                            break

                    if not return_dict['label']:
                        return_dict['label'] = default_label

            if len(return_dict.keys()) > 0:
                return return_dict

            return None

        for form in forms:
            username = find_field(form, ['email', 'username', 'user'], "Username")
            password = find_field(form, ['password', 'passwd', 'pass'], "Password")

            if username != None and password != None:
                submit_buttom = form.find_elements_by_xpath("//button[@type='submit']")
                return {
                    "form_element": form,
                    "username": username,
                    "password": password,
                    "submit_button": submit_buttom
                }

        return None

    def get_type_lists(self):
        return self.driver.find_elements_by_xpath("//div[@id='ag-list']/ul/li")

    def process_type_list(self, type_list):
        title = clean_padding_whitespace(type_list.find_element_by_xpath("div//button").text.replace("\n", ""))
        print(title)

        assignments = []

        for assignment in type_list.find_elements_by_xpath("div//div[@class='ig-info']"):
            assignment_title = clean_padding_whitespace(assignment.find_element_by_xpath("a[@class='ig-title']").text)

            try:
                due_month, due_day, _, due_time = clean_padding_whitespace(assignment.find_element_by_xpath("div[@class='ig-details']/div[@data-view='date-due']/span").text).split(" ")
            except:
                continue

            assignments.append({"title": assignment_title, "deadline": create_datetime(due_month, due_day, due_time)})

        return {
            "title": title,
            "assignments": assignments
        }
