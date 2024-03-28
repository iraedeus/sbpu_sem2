from typing import Optional


class Shop:
    def __init__(self) -> None:
        self.products: dict[str, Product] = {}
        self.baskets: dict[str, Basket] = {}

        self.cheapest: list[Product] = []
        self.richest: list[Product] = []
        self.highest_rating: list[Product] = []
        self.lowest_rating: list[Product] = []

    def get_cheapest(self) -> list[str]:
        if len(self.cheapest) == 0:
            raise ValueError

        return [cheapest_product.name for cheapest_product in self.cheapest]

    def get_richest(self) -> list[str]:
        if len(self.richest) == 0:
            raise ValueError

        return [rich_product.name for rich_product in self.richest]

    def get_higher_rating(self) -> list[str]:
        if len(self.highest_rating) == 0:
            raise ValueError

        return [highest_rating_product.name for highest_rating_product in self.highest_rating]

    def get_lower_rating(self) -> list[str]:
        if len(self.lowest_rating) == 0:
            raise ValueError

        return [lowest_rating_product.name for lowest_rating_product in self.lowest_rating]

    def check_cheapest_richest(self, product: "Product") -> None:
        if len(self.cheapest) == 0 and len(self.richest) == 0:
            self.cheapest.append(product)
            self.richest.append(product)
            return None
        if self.cheapest[0].cost == product.cost:
            self.cheapest.append(product)
            return None
        if self.richest[0].cost == product.cost:
            self.richest.append(product)
            return None
        if self.richest[0].cost < product.cost:
            self.richest = [product]
            return None
        if self.cheapest[0].cost > product.cost:
            self.cheapest = [product]
            return None

    def check_lowest_highest_rating(self, product: "Product") -> None:
        if len(self.lowest_rating) == 0 and len(self.highest_rating) == 0:
            self.lowest_rating.append(product)
            self.highest_rating.append(product)
            return None
        if self.lowest_rating[0].rating == product.rating:
            self.lowest_rating.append(product)
            return None
        if self.highest_rating[0].cost == product.rating:
            self.highest_rating.append(product)
            return None
        if self.lowest_rating[0].cost > product.rating:
            self.lowest_rating = [product]
            return None
        if self.highest_rating[0].cost < product.rating:
            self.highest_rating = [product]
            return None

    def add_products_to_shop(self, *products: "Product") -> None:
        for product in products:
            self.products[product.name] = product

            self.check_lowest_highest_rating(product)
            self.check_cheapest_richest(product)

    def create_basket(self, name: str) -> None:
        self.baskets[name] = Basket(name)

    def add_product_to_basket(self, basket_name: str, product_name: str, count: int) -> None:
        if product_name == "" or basket_name == "":
            raise ValueError("The name of your shopping cart and product should not be an empty string")

        cost = self.products[product_name].cost
        rating = self.products[product_name].rating
        basket = self.baskets[basket_name]

        if product_name in basket.products:
            basket.products[product_name].count += count
            basket.summary_cost += cost * count
        else:
            basket.products[product_name] = Product(product_name, cost, count, rating)
            basket.summary_cost += cost * count

    def sell_products_in_basket(self, basket_name: str) -> None:
        basket = self.baskets[basket_name]
        del self.baskets[basket_name]

        for product_name in basket.products:
            count = basket.products[product_name].count
            self.products[product_name].count -= count


class Basket:
    def __init__(self, name: str):
        self.name: str = name
        self.products: dict[str, Product] = {}
        self.summary_cost: float = 0


class Product:
    def __init__(self, name: str, cost: float, count: int, rating: float) -> None:
        self.name: str = name
        self.cost = cost
        self.rating = rating
        self.count = count

    def change_cost(self, new_cost: float) -> None:
        self.cost = new_cost

    def new_rating(self, new_rating: float) -> None:
        self.rating = new_rating

    def __repr__(self) -> str:
        return f"Product name {self.name}, cost {self.cost}, rating {self.rating}, count {self.count}"


def main() -> None:
    shop = Shop()
    shirts = Product("shirt", 100, 100, 4.5)
    caps = Product("cap", 200, 1000, 3)
    sneakers = Product("sneaker", 99.9, 100, 2)

    shop.add_products_to_shop(shirts, caps, sneakers)

    shop.create_basket("first_user")
    shop.add_product_to_basket("first_user", "sneaker", 2)
    shop.add_product_to_basket("first_user", "cap", 5)
    shop.add_product_to_basket("first_user", "shirt", 10)

    shop.create_basket("second_user")
    shop.add_product_to_basket("second_user", "sneaker", 10)
    shop.add_product_to_basket("second_user", "cap", 100)
    shop.add_product_to_basket("second_user", "shirt", 90)

    shop.sell_products_in_basket("first_user")
    shop.sell_products_in_basket("second_user")

    for product_name in shop.products:
        print(shop.products[product_name])


if __name__ == "__main__":
    main()
