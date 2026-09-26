from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.order import Order
from app.models.product import Product

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    products_total = db.query(func.count(Product.id)).scalar()
    orders_total = db.query(func.count(Order.id)).scalar()

    body = (
        "# HELP products_total Total number of products\n"
        "# TYPE products_total gauge\n"
        f"products_total {products_total}\n"
        "# HELP orders_total Total number of orders\n"
        "# TYPE orders_total gauge\n"
        f"orders_total {orders_total}\n"
    )
    return PlainTextResponse(content=body)
