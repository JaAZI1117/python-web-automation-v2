from selenium.webdriver.common.by import By

from pages.base_page import BasePage

class CartPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def item_count(self):
        return len(self.finds(self.ITEMS))

    def item_names(self):
        return self.texts_of(self.ITEM_NAMES)

    def item_prices(self):
        return [self.to_decimal(t) for t in self.texts_of(self.ITEM_PRICES)]

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING)
        return self
