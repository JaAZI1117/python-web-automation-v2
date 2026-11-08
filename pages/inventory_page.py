from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage

class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def is_loaded(self):
        return self.is_visible(self.ITEMS, timeout=10)

    def item_count(self):
        return len(self.finds(self.ITEMS))

    def item_names(self):
        return self.texts_of(self.ITEM_NAMES)

    def item_prices(self):
        return [self.to_decimal(t) for t in self.texts_of(self.ITEM_PRICES)]

    def sort_by(self, value):
        """value: az / za / lohi / hilo"""
        Select(self.find(self.SORT_SELECT)).select_by_value(value)
        return self

    def add_to_cart(self, product_key):
        """product_key 例如 sauce-labs-backpack"""
        self.click((By.ID, f"add-to-cart-{product_key}"))
        return self

    def remove_from_cart(self, product_key):
        self.click((By.ID, f"remove-{product_key}"))
        return self

    def cart_count(self):
        """角标不存在时返回 0"""
        badges = self.finds(self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def open_cart(self):
        self.click(self.CART_LINK)
        return self

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        return self
