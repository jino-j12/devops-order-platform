import pytest
from pydantic import ValidationError

from app.schemas.order import OrderCreate, OrderItemCreate


def test_order_item_create_valid():
    item = OrderItemCreate(product_id=1, quantity=2)
    assert item.quantity == 2


def test_order_item_create_zero_quantity():
    with pytest.raises(ValidationError):
        OrderItemCreate(product_id=1, quantity=0)


def test_order_item_create_negative_quantity():
    with pytest.raises(ValidationError):
        OrderItemCreate(product_id=1, quantity=-1)


def test_order_create_valid():
    order = OrderCreate(items=[OrderItemCreate(product_id=1, quantity=2)])
    assert len(order.items) == 1


def test_order_create_empty_items():
    with pytest.raises(ValidationError):
        OrderCreate(items=[])
