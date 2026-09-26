# API Design

## 1. Overview

The application will provide a REST API for managing products and orders.

The API will be implemented using FastAPI.

The initial API will provide:

- Product management
- Order management
- Application health checking
- Prometheus metrics

The API will use HTTP methods and status codes to communicate the result
of each operation.

---

## 2. API Endpoints

### 2.1 Health Check

**Method:** `GET`

**Endpoint:**

```text
/health