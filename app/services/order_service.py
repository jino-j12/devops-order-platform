from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate


class OrderValidationError(Exception):
    pass


def create_order(db: Session, order_in: OrderCreate) -> Order:
    quantities: dict[int, int] = {}
    for item in order_in.items:
        quantities[item.product_id] = quantities.get(item.product_id, 0) + item.quantity

    products = {
        product.id: product
        for product in db.query(Product).filter(Product.id.in_(quantities.keys())).all()
    }

    for product_id, total_quantity in quantities.items():
        product = products.get(product_id)
        if product is None:
            raise OrderValidationError(f"Product {product_id} does not exist")
        if total_quantity > product.stock:
            raise OrderValidationError(
                f"Insufficient stock for product {product_id}: "
                f"requested {total_quantity}, available {product.stock}"
            )

    order = Order()
    for item in order_in.items:
        product = products[item.product_id]
        order.items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
            )
        )

    for product_id, total_quantity in quantities.items():
        products[product_id].stock -= total_quantity

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_orders(db: Session) -> list[Order]:
    return db.query(Order).order_by(Order.id).all()


def get_order(db: Session, order_id: int) -> Order | None:
    return db.get(Order, order_id)
