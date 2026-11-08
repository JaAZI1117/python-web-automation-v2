import os

import allure
import pytest
from selenium import webdriver

from config import BASE_URL, STANDARD_USER
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="edge",
        choices=["chrome", "edge", "firefox"],
        help="选择浏览器: chrome / edge / firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="无头模式运行（CI 用）",
    )

def _create_driver(browser, headless):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
    elif browser == "edge":
        options = webdriver.EdgeOptions()
    else:
        options = webdriver.FirefoxOptions()

    if headless:
        options.add_argument("-headless" if browser == "firefox" else "--headless=new")
        options.add_argument("--window-size=1920,1080")

    factory = {
        "chrome": webdriver.Chrome,
        "edge": webdriver.Edge,
        "firefox": webdriver.Firefox,
    }[browser]
    return factory(options=options)

@pytest.fixture(scope="session")
def driver(request):
    """整个测试会话只启动一次浏览器"""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    driver = _create_driver(browser, headless)
    if not headless:
        driver.maximize_window()

    yield driver

    try:
        driver.quit()
    except Exception:
        pass

@pytest.fixture(autouse=True)
def fresh_browser(driver):
    """每条用例开始前清 Cookie 和本地存储，避免用例互相污染"""
    driver.delete_all_cookies()
    driver.get(BASE_URL)
    driver.execute_script(
        "window.localStorage.clear(); window.sessionStorage.clear();"
    )
    yield

@pytest.fixture
def login_page(driver):
    return LoginPage(driver).load()

@pytest.fixture
def logged_in(driver):
    """已登录并停在商品列表页的 driver"""
    LoginPage(driver).load().login(
        STANDARD_USER["username"], STANDARD_USER["password"]
    )
    assert InventoryPage(driver).is_loaded(), "登录后没有进入商品列表页"
    return driver

@pytest.fixture
def base_page(driver):
    return BasePage(driver)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    """失败自动截图并挂到 allure，截图异常不会影响 driver.quit()"""
    yield

    rep = getattr(request.node, "rep_call", None)
    if rep is None or not rep.failed:
        return

    try:
        os.makedirs("screenshots", exist_ok=True)
        path = os.path.join("screenshots", f"{request.node.name}.png")
        driver.save_screenshot(path)
        with open(path, "rb") as f:
            allure.attach(
                f.read(),
                name=f"失败截图-{request.node.name}",
                attachment_type=allure.attachment_type.PNG,
            )
        print(f"\n失败截图已保存: {path}")
    except Exception as err:  # 截图失败不能掩盖原始报错
        print(f"\n截图失败: {err}")
