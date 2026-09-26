from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(db: Session) -> list[Product]:
    return db.query(Product).order_by(Product.id).all()


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def update_product(
    db: Session, product_id: int, product_in: ProductUpdate
) -> Product | None:
    product = db.get(Product, product_id)
    if product is None:
        return None

    for field, value in product_in.model_dump().items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    product = db.get(Product, product_id)
    if product is None:
        return False

    db.delete(product)
    db.commit()
    return True
