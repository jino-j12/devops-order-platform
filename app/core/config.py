import os

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://devops_user:devops_password@localhost:5433/order_platform",
)
