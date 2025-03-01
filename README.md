# E-commerce

## Описание
Проект реализует ядро для для интернет-магазина.

## Структура
В директории `src/` присутствует следущие модули:
- `models.py` - реализуюет модели `Product` и `Category`, описывающий модели для хранения продуктов и категорий продуктов соответственно.
Функция `convert_json_to_categories` конвертирует категории в формате JSON в список объектов класса `Category`.

В директории `tests/` написаны тесты для модулей из директории `src/`

## Установка и Использование
1. Скопировать репозирорий
```shell
git clone https://github.com/github-main-user/ecommerce.git
```
Или
```shell
git clonegit@github.com:github-main-user/ecommerce.git
```

2. Зайти в директорию
```shell
cd ecommerce
```

3. Установить зависимости
```python
poetry install
```

4. Запустить `main.py` файл:
```shell
python main.py
```
или
```shell
./main.py
```
на Linux.

## Тесты
Тесты написаны с использованием pytest.
Для проверки использовать:
```shell
pytest --cov src
```