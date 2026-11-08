import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.file_reader import load_json

LOGIN_CASES = load_json("login_data.json")

@allure.feature("登录模块")
class TestLogin:

    @allure.story("数据驱动登录")
    @allure.title("登录场景：{case[desc]}")
    @pytest.mark.smoke
    @pytest.mark.parametrize("case", LOGIN_CASES, ids=[c["desc"] for c in LOGIN_CASES])
    def test_login(self, driver, login_page, case):
        with allure.step(f"输入账号 [{case['username'] or '空'}] / 密码 [{case['password'] or '空'}] 并提交"):
            login_page.login(case["username"], case["password"])

        with allure.step("断言登录结果"):
            if case["should_pass"]:
                assert "inventory.html" in driver.current_url, "预期跳转到商品页，实际没有"
                assert driver.title == "Swag Labs", f"页面标题不对: {driver.title}"
                assert InventoryPage(driver).item_count() == 6, "商品数量不是 6"
            else:
                assert login_page.error_visible(), "预期出现红色错误提示，实际没有"
                assert login_page.error_text() == case["error"], "错误文案与预期不一致"

    @allure.story("回车键提交")
    @allure.title("用回车键提交登录表单")
    def test_login_by_enter_key(self, driver, login_page):
        login_page.login("standard_user", "secret_sauce", submit_by_enter=True)
        assert "inventory.html" in driver.current_url, "回车提交后没有跳转到商品页"

    @allure.story("退出登录")
    @allure.title("登录后从侧边栏退出，应回到登录页")
    def test_logout(self, driver, logged_in):
        with allure.step("点击右上角菜单 → Logout"):
            InventoryPage(driver).logout()

        with allure.step("断言已回到登录页"):
            assert driver.current_url.rstrip("/") == "https://www.saucedemo.com"
            assert LoginPage(driver).is_visible(LoginPage.LOGIN_BUTTON)
