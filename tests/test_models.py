import json
from typing import Any
from unittest.mock import Mock, mock_open, patch

import pytest

from src.models import Category, Product, convert_json_to_categories

# --- FIXTURES ---


@pytest.fixture
def product_object() -> Product:
    return Product(name="Keyboard", description="A computer keyboard", price=2000.25, quantity=50)


@pytest.fixture
def product_dict() -> dict[str, Any]:
    return {"name": "Keyboard", "description": "A computer keyboard", "price": 2000.25, "quantity": 50}


@pytest.fixture
def wrong_product_dict() -> dict[str, Any]:
    return {"na": "Keyboard", "UwU": "123"}


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


@pytest.fixture
def correct_json() -> list[dict]:
    return [
        {
            "name": "Смартфоны",
            "description": "Смартфоны, как средство не только коммуникации",
            "products": [
                {
                    "name": "Samsung Galaxy C23 Ultra",
                    "description": "256GB, Серый цвет, 200MP камера",
                    "price": 180000.0,
                    "quantity": 5,
                },
                {"name": "Iphone 15", "description": "512GB, Gray space", "price": 210000.0, "quantity": 8},
                {"name": "Xiaomi Redmi Note 11", "description": "1024GB, Синий", "price": 31000.0, "quantity": 14},
            ],
        },
        {
            "name": "Телевизоры",
            "description": "Современный телевизор, который позволяет наслаждаться просмотром",
            "products": [
                {"name": '55" QLED 4K', "description": "Фоновая подсветка", "price": 123000.0, "quantity": 7}
            ],
        },
    ]


# --- TESTS ---


# =========
#  Product
# =========


def test_product_init(product_object: Product) -> None:
    assert product_object.name == "Keyboard"
    assert product_object.description == "A computer keyboard"
    assert product_object.price == 2000.25
    assert product_object.quantity == 50


def test_product_new_product_correct(product_dict: dict[str, Any]) -> None:
    prod_dict = Product.new_product(product_dict, [])
    prod_obj = Product(**product_dict)

    assert prod_dict.name == prod_obj.name
    assert prod_dict.description == prod_obj.description
    assert prod_dict.price == prod_obj.price
    assert prod_dict.quantity == prod_obj.quantity


def test_product_new_product_incomplete_dict(wrong_product_dict: dict[str, Any]) -> None:
    with pytest.raises(TypeError):
        Product.new_product(wrong_product_dict, [])


def test_product_price_setter_negative_price(product_object: Product, capsys: Any) -> None:
    product_object.price = -10
    product_object.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_object.price == 2000.25


def test_product_price_setter_greater_price(product_object: Product) -> None:
    product_object.price = 3000
    assert product_object.price == 3000


def test_product_price_setter_decreace_denied(product_object: Product, capsys: Any) -> None:
    with patch("builtins.input", return_value="n"):
        product_object.price = 30

    captured = capsys.readouterr()
    assert "Вы уверены что хотите снизить цену? (y/n): " in captured.out
    assert product_object.price == 2000.25


def test_product_price_setter_decreace_accepted(product_object: Product, capsys: Any) -> None:
    with patch("builtins.input", return_value="y"):
        product_object.price = 30

    captured = capsys.readouterr()
    assert "Вы уверены что хотите снизить цену? (y/n): " in captured.out
    assert product_object.price == 30


# ==========
#  Category
# ==========


def test_category_init(category_object: Category) -> None:
    assert category_object.name == "Computer products"
    assert category_object.description == "Products for a computer"

    product = category_object.products[0]
    assert product == "Keyboard, 2000.25 руб. Остаток: 50 шт."


def test_category_product_count(list_of_products: list[Product]) -> None:
    # в одном list_of_products 4 продукта
    Category.category_count = 0
    Category.product_count = 0

    Category(name="Something", description="something", products=list_of_products)
    assert Category.category_count == 1
    assert Category.product_count == 4

    Category(name="Something", description="something", products=list_of_products)
    Category(name="Something", description="something", products=list_of_products)
    Category(name="Something", description="something", products=list_of_products)
    assert Category.category_count == 4
    assert Category.product_count == 16


def test_category_add_product(category_object: Category, list_of_products: list[Product]) -> None:
    Category.product_count = 0
    assert Category.product_count == 0

    category_object.add_product(list_of_products[0])
    assert Category.product_count == 1

    for product in list_of_products:
        category_object.add_product(product)
    assert Category.product_count == 5


# ============================
#  convert_json_to_categories
# ============================


def test_convert_json_success(correct_json: list[dict]) -> None:
    with patch("builtins.open", mock_open(read_data=json.dumps(correct_json))) as mock_file:
        categories = convert_json_to_categories("fake.json")
        mock_file.assert_called_once_with("fake.json", "r", encoding="utf-8")

        assert len(categories) == 2
        assert len(categories[0].products) == 3
        assert len(categories[1].products) == 1

        assert categories[0].name == "Смартфоны"
        assert categories[0].description == "Смартфоны, как средство не только коммуникации"
        assert categories[1].products[0] == '55" QLED 4K, 123000.0 руб. Остаток: 14 шт.'


def test_convert_json_empty_json() -> None:
    with patch("builtins.open", mock_open(read_data=json.dumps([]))):
        assert convert_json_to_categories("fake.json") == []


@patch("builtins.open", side_effect=FileNotFoundError)
def test_convert_json_wrong_path(mock_open: Mock) -> None:
    with pytest.raises(FileNotFoundError):
        convert_json_to_categories("fake.json")


def test_convert_json_missing_products_field() -> None:
    incomplete_json = [
        {
            "name": "Books",
            "description": "All kinds of books",
        }
    ]
    with patch("builtins.open", mock_open(read_data=json.dumps(incomplete_json))):
        categories = convert_json_to_categories("fake_path.json")
        assert len(categories) == 1
        assert categories[0].name == "Books"
        assert categories[0].description == "All kinds of books"
        assert categories[0].products == []


def test_convert_json_wrong_format(wrong_product_dict: dict[str, Any]) -> None:
    with patch("builtins.open", mock_open(read_data=json.dumps([wrong_product_dict]))):
        with pytest.raises(KeyError):
            convert_json_to_categories("fake.json")
