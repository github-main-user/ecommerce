import json


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


def convert_json_to_categories(json_path: str) -> list[Category]:
    """Конвертирует список категорий в JSON формате в список объектов класса Category."""
    with open(json_path, "r", encoding="utf-8") as file_obj:
        categories = json.load(file_obj)

    return [
        Category(
            name=category["name"],
            description=category["description"],
            products=[
                Product(
                    name=product["name"],
                    description=product["description"],
                    price=product["price"],
                    quantity=product["quantity"],
                )
                for product in category.get("products", [])
            ],
        )
        for category in categories
    ]
