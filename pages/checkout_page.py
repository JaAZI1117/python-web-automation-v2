from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """结算三步：step-one（填信息）→ step-two（确认）→ complete（完成）"""

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    FINISH_BUTTON = (By.ID, "finish")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    # ---------- step one ----------
    def fill_information(self, first_name, last_name, postal_code):
        """传空字符串表示该项不填，用来测必填校验"""
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        return self

    def continue_next(self):
        self.click(self.CONTINUE_BUTTON)
        return self

    def error_visible(self):
        return self.is_visible(self.ERROR_MESSAGE)

    def error_text(self):
        return self.text_of(self.ERROR_MESSAGE)

    # ---------- step two ----------
    def subtotal(self):
        return self.to_decimal(self.text_of(self.SUBTOTAL_LABEL))

    def tax(self):
        return self.to_decimal(self.text_of(self.TAX_LABEL))

    def total(self):
        return self.to_decimal(self.text_of(self.TOTAL_LABEL))

    def finish(self):
        self.click(self.FINISH_BUTTON)
        return self

    # ---------- complete ----------
    def complete_text(self):
        return self.text_of(self.COMPLETE_HEADER)
