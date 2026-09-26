import pytest
from pydantic import ValidationError

from app.schemas.product import ProductCreate, ProductUpdate


def test_product_create_valid():
    product = ProductCreate(name="Keyboard", description="RGB", price=25.00, stock=10)
    assert product.name == "Keyboard"
    assert product.price == 25.00
    assert product.stock == 10


def test_product_create_empty_name():
    with pytest.raises(ValidationError):
        ProductCreate(name="", price=10, stock=1)


def test_product_create_invalid_price():
    with pytest.raises(ValidationError):
        ProductCreate(name="Keyboard", price=0, stock=1)


def test_product_create_negative_price():
    with pytest.raises(ValidationError):
        ProductCreate(name="Keyboard", price=-5, stock=1)


def test_product_create_negative_stock():
    with pytest.raises(ValidationError):
        ProductCreate(name="Keyboard", price=10, stock=-1)


def test_product_create_optional_description():
    product = ProductCreate(name="Keyboard", price=10, stock=1)
    assert product.description is None


def test_product_update_valid():
    product = ProductUpdate(name="Keyboard", description="RGB", price=25.00, stock=10)
    assert product.stock == 10


def test_product_update_empty_name():
    with pytest.raises(ValidationError):
        ProductUpdate(name="", price=10, stock=1)


def test_product_update_negative_stock():
    with pytest.raises(ValidationError):
        ProductUpdate(name="Keyboard", price=10, stock=-1)
