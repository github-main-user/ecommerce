import json
from typing import Any, Self


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name.strip()
        self.description = description.strip()
        self._price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product: dict[str, Any], product_list: list[Self]) -> Self:
        """Принимает на вход параметры товара в ввиде словаря, возвращает объект этого класса."""
        new_product = cls(**product)

        for prod in product_list:
            if prod.name.lower() == new_product.name.lower():
                new_product.quantity += prod.quantity
                new_product.price = max(prod.price, new_product.price)
                break

        return new_product

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price < self._price:
            print(f"Новая цена ({new_price}) ниже предыдущей ({self._price}) на {new_price - self._price}")
            print("Вы уверены что хотите снизить цену? (y/n): ", end="")
            if not (input() == "y"):
                return

        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        self._price = new_price


class Category:
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        self.name = name.strip()
        self.description = description.strip()
        self._products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет объект класса Product к списку продуктов."""
        self._products.append(product)

    @property
    def products(self) -> list[str]:
        """Выводит список товаров ввиде строк формата "<Название продукта>, <80 руб>. <Остаток: 15 шт>" ."""
        return [f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self._products]


def convert_json_to_categories(json_path: str) -> list[Category]:
    """Конвертирует список категорий в JSON формате в список объектов класса Category."""
    with open(json_path, "r", encoding="utf-8") as file_obj:
        categories = json.load(file_obj)

    return [
        Category(
            name=category["name"],
            description=category["description"],
            products=[
                Product.new_product(product, [Product(**prod) for prod in category.get("products", [])])
                for product in category.get("products", [])
            ],
        )
        for category in categories
    ]
