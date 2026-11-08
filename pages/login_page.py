from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def load(self):
        return self.open("")

    def login(self, username, password, submit_by_enter=False):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        if submit_by_enter:
            self.find(self.PASSWORD).send_keys(Keys.ENTER)
        else:
            self.click(self.LOGIN_BUTTON)
        return self

    def error_visible(self):
        return self.is_visible(self.ERROR_MESSAGE)

    def error_text(self):
        return self.text_of(self.ERROR_MESSAGE)
