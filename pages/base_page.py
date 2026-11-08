from decimal import Decimal

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, WAIT_TIMEOUT

class BasePage:
    """所有页面对象的基类，统一封装等待/点击/输入，页面对象里不再直接写 driver.find_element"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIMEOUT)

    # ---------- 打开页面 ----------
    def open(self, path=""):
        self.driver.get(BASE_URL.rstrip("/") + path)
        return self

    @property
    def current_url(self):
        return self.driver.current_url

    # ---------- 元素操作 ----------
    def find(self, locator):
        """等元素可见再返回"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def finds(self, locator):
        """不等，直接返回列表（判断"不存在"时用这个）"""
        return self.driver.find_elements(*locator)

    def click(self, locator):
        """等元素可点击再点"""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        if text:
            element.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text

    def texts_of(self, locator):
        return [e.text for e in self.finds(locator)]

    def is_visible(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ---------- 金额工具 ----------
    @staticmethod
    def to_decimal(text):
        """把 '$29.99' / 'Item total: $29.99' 转成 Decimal('29.99')，不要用 float"""
        return Decimal(text.replace("$", "").replace("Item total:", "")
                       .replace("Tax:", "").replace("Total:", "").strip())
