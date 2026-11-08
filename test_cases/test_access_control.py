import allure
import pytest

from config import BASE_URL
from pages.login_page import LoginPage

@allure.feature("访问控制")
class TestAccessControl:
    """未登录直接敲 URL 访问内页，应被重定向回登录页"""

    @allure.story("未登录访问受保护页面")
    @allure.title("未登录直接访问 {path} 应回到登录页")
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "path",
        ["/inventory.html", "/cart.html", "/checkout-step-one.html", "/checkout-step-two.html"],
    )
    def test_direct_access_redirects_to_login(self, driver, path):
        driver.get(BASE_URL.rstrip("/") + path)

        assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/"), "没有重定向回登录页"
        assert LoginPage(driver).is_visible(LoginPage.LOGIN_BUTTON), "登录表单不可见"
