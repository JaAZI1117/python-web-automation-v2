import allure
import pytest

from pages.inventory_page import InventoryPage

@allure.feature("商品列表模块")
class TestInventory:

    @allure.story("商品展示")
    @allure.title("商品列表应展示 6 件商品")
    @pytest.mark.smoke
    def test_item_count(self, logged_in):
        page = InventoryPage(logged_in)
        assert page.item_count() == 6, "商品数量不对"

    @allure.story("商品展示")
    @allure.title("价格区间应为 $7.99 ~ $49.99")
    def test_price_range(self, logged_in):
        prices = InventoryPage(logged_in).item_prices()
        assert str(min(prices)) == "7.99", f"最低价不对: {min(prices)}"
        assert str(max(prices)) == "49.99", f"最高价不对: {max(prices)}"

    @allure.story("商品排序")
    @allure.title("排序功能：{sort_value}")
    @pytest.mark.parametrize(
        "sort_value, by_price, reverse",
        [
            ("lohi", True, False),
            ("hilo", True, True),
            ("az", False, False),
            ("za", False, True),
        ],
        ids=["价格低到高", "价格高到低", "名称A到Z", "名称Z到A"],
    )
    def test_sort(self, logged_in, sort_value, by_price, reverse):
        page = InventoryPage(logged_in)

        with allure.step(f"选择排序方式 {sort_value}"):
            page.sort_by(sort_value)

        with allure.step("断言排序结果有序"):
            if by_price:
                prices = page.item_prices()
                assert prices == sorted(prices, reverse=reverse), f"价格排序错误: {prices}"
            else:
                names = page.item_names()
                assert names == sorted(names, reverse=reverse), f"名称排序错误: {names}"
