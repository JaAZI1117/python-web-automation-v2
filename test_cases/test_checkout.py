import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from utils.file_reader import load_json

CHECKOUT_DATA = load_json("checkout_data.json")
VALID = CHECKOUT_DATA["valid_customer"]
INVALID_CASES = CHECKOUT_DATA["invalid_customers"]
BACKPACK = CHECKOUT_DATA["backpack"]

@allure.feature("结算流程")
class TestCheckout:

    @pytest.fixture
    def checkout_page(self, logged_in):
        """加购一件背包 → 进购物车 → 点 Checkout，停在信息填写页"""
        InventoryPage(logged_in).add_to_cart(BACKPACK["key"]).open_cart()
        CartPage(logged_in).checkout()
        return CheckoutPage(logged_in)

    @allure.story("必填校验")
    @allure.title("结算信息校验：{case[desc]}")
    @pytest.mark.parametrize("case", INVALID_CASES, ids=[c["desc"] for c in INVALID_CASES])
    def test_required_field_validation(self, checkout_page, case):
        checkout_page.fill_information(
            case["first_name"], case["last_name"], case["postal_code"]
        ).continue_next()

        assert checkout_page.error_visible(), "预期出现错误提示"
        assert checkout_page.error_text() == case["error"], "错误文案不一致"

    @allure.story("完整下单")
    @allure.title("填写正确信息，完成从结算到下单成功的全流程")
    @pytest.mark.smoke
    def test_full_checkout_flow(self, logged_in, checkout_page):
        with allure.step("填写收货信息并继续"):
            checkout_page.fill_information(
                VALID["first_name"], VALID["last_name"], VALID["postal_code"]
            ).continue_next()
            assert "checkout-step-two.html" in logged_in.current_url

        with allure.step("校验金额：商品总价 + 税 = 合计"):
            subtotal = checkout_page.subtotal()
            tax = checkout_page.tax()
            total = checkout_page.total()
            assert str(subtotal) == BACKPACK["price"], f"商品总价不对: {subtotal}"
            assert tax > 0, "税费应该大于 0"
            assert total == subtotal + tax, f"{subtotal} + {tax} != {total}"

        with allure.step("点击 Finish 完成下单"):
            checkout_page.finish()
            assert "checkout-complete.html" in logged_in.current_url
            assert checkout_page.complete_text() == "Thank you for your order!"

    @allure.story("取消结算")
    @allure.title("结算页点 Cancel 应回到购物车，商品还在")
    def test_cancel_checkout(self, logged_in, checkout_page):
        checkout_page.click(checkout_page.CANCEL_BUTTON)
        assert "cart.html" in logged_in.current_url
        assert CartPage(logged_in).item_count() == 1
