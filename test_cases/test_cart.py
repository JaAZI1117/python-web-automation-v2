import allure
from selenium.webdriver.common.by import By

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"

@allure.feature("购物车模块")
class TestCart:

    @allure.story("加入购物车")
    @allure.title("加购一件商品，角标显示 1")
    def test_add_single_item(self, logged_in):
        page = InventoryPage(logged_in)

        with allure.step("加购前角标不存在"):
            assert page.cart_count() == 0

        with allure.step("点击背包的 Add to cart"):
            page.add_to_cart(BACKPACK)

        with allure.step("断言角标变成 1，按钮变成 Remove"):
            assert page.cart_count() == 1
            assert page.is_visible((By.ID, f"remove-{BACKPACK}"))

    @allure.story("加入购物车")
    @allure.title("加购两件商品，购物车里应有两件")
    def test_add_two_items(self, logged_in):
        page = InventoryPage(logged_in)
        page.add_to_cart(BACKPACK).add_to_cart(BIKE_LIGHT)
        assert page.cart_count() == 2

        page.open_cart()
        assert "cart.html" in logged_in.current_url

        cart = CartPage(logged_in)
        assert cart.item_count() == 2
        assert set(cart.item_names()) == {"Sauce Labs Backpack", "Sauce Labs Bike Light"}

    @allure.story("购物车内容")
    @allure.title("购物车里的商品名和价格应与列表页一致")
    def test_cart_content(self, logged_in):
        inventory = InventoryPage(logged_in)
        expected_name = inventory.item_names()[0]
        expected_price = inventory.item_prices()[0]
        inventory.add_to_cart(BACKPACK).open_cart()

        cart = CartPage(logged_in)
        assert cart.item_names() == [expected_name]
        assert cart.item_prices() == [expected_price]

    @allure.story("移除商品")
    @allure.title("移除唯一的一件商品，角标应消失")
    def test_remove_last_item(self, logged_in):
        page = InventoryPage(logged_in)
        page.add_to_cart(BACKPACK)
        assert page.cart_count() == 1

        page.remove_from_cart(BACKPACK)
        assert page.cart_count() == 0, "移除后角标应该消失"
        assert not page.is_visible((By.ID, f"remove-{BACKPACK}"))

    @allure.story("继续购物")
    @allure.title("购物车里点 Continue Shopping 应回到商品列表")
    def test_continue_shopping(self, logged_in):
        InventoryPage(logged_in).open_cart()
        CartPage(logged_in).continue_shopping()
        assert "inventory.html" in logged_in.current_url
