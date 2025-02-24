import pytest

from src.models import Category, Product


@pytest.fixture
def product_object() -> Product:
    return Product(name="Keyboard", description="A computer keyboard", price=2000.25, quantity=50)


@pytest.fixture
def list_of_products() -> list[Product]:
    return [
        Product(name="Keyboard", description="A computer keyboard", price=2000.25, quantity=50),
        Product(name="Mouse", description="A computer mouse", price=1520.5, quantity=45),
        Product(name="Cable", description="A computer cable", price=150.9, quantity=5),
        Product(name="Monitor", description="A computer monitor", price=5120, quantity=30),
    ]


@pytest.fixture
def category_object(product_object: Product) -> Category:
    return Category(name="Computer products", description="Products for a computer", products=[product_object])


def test_product_init(product_object: Product) -> None:
    assert product_object.name == "Keyboard"
    assert product_object.description == "A computer keyboard"
    assert product_object.price == 2000.25
    assert product_object.quantity == 50


def test_category_init(category_object: Category) -> None:
    assert category_object.name == "Computer products"
    assert category_object.description == "Products for a computer"

    product = category_object.products[0]
    assert product.name == "Keyboard"
    assert product.description == "A computer keyboard"
    assert product.price == 2000.25
    assert product.quantity == 50


def test_number_of_products(list_of_products: list[Product]) -> None:
    # в одном list_of_products 4 продукта
    Category.number_of_categories = 0
    Category.number_of_products = 0

    _ = Category(name="Something", description="something", products=list_of_products)
    assert Category.number_of_categories == 1
    assert Category.number_of_products == 4

    _ = Category(name="Something", description="something", products=list_of_products)
    _ = Category(name="Something", description="something", products=list_of_products)
    _ = Category(name="Something", description="something", products=list_of_products)
    assert Category.number_of_categories == 4
    assert Category.number_of_products == 16
