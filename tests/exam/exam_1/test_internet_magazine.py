import string

import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.exam.exam_1.internet_magazine import *


class TestShop:
    @staticmethod
    def create_test_shop():
        shirts = Product("shirt", 100, 100, 3)
        sneakers = Product("sneaker", 1000, 1000, 2)
        caps = Product("cap", 200, 10, 5)

        shop = Shop()
        shop.add_products_to_shop(shirts, sneakers, caps)

        return shop

    @given(
        name=st.text(alphabet=string.ascii_lowercase),
        cost=st.floats(),
        count=st.integers(min_value=0),
        rating=st.floats(min_value=0.0, max_value=5.0),
    )
    def test_add_to_shop(self, name, cost, count, rating):
        shop = self.create_test_shop()

        new_product = Product(name, cost, count, rating)
        shop.add_products_to_shop(new_product)

        assert new_product == shop.products[name]

    @given(
        basket_name=st.text(alphabet=string.ascii_lowercase).filter(lambda x: x != ""),
        product_name=st.text(alphabet=string.ascii_lowercase).filter(lambda x: x != ""),
        count=st.integers(min_value=0),
        cost=st.floats(),
        rating=st.floats(min_value=0.0, max_value=5.0),
    )
    def test_add_to_basket(self, basket_name, product_name, count, cost, rating):
        shop = self.create_test_shop()
        shop.create_basket(basket_name)

        new_product = Product(product_name, cost, count, rating)
        shop.add_products_to_shop(new_product)

        shop.add_product_to_basket(basket_name, product_name, count)
        basket = shop.baskets[basket_name]

        assert basket.products[product_name].count == count
        assert len(basket.products) == 1

    @given(
        basket_name=st.text(alphabet=string.ascii_lowercase).filter(lambda x: x != ""),
        product_name=st.text(alphabet=string.ascii_lowercase).filter(lambda x: x != ""),
        count=st.integers(min_value=100),
        cost=st.floats(),
        rating=st.floats(min_value=0.0, max_value=5.0),
    )
    def test_sell_basket(self, basket_name, product_name, count, cost, rating):
        shop = self.create_test_shop()
        shop.create_basket(basket_name)

        new_product = Product(product_name, cost, count, rating)
        shop.add_products_to_shop(new_product)

        shop.add_product_to_basket(basket_name, product_name, count)
        shop.sell_products_in_basket(basket_name)

        assert shop.baskets == {}
        assert shop.products[product_name].count == 0
