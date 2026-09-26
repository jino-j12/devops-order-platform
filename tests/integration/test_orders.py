def _create_product(client, **overrides):
    payload = {
        "name": "Mechanical Keyboard",
        "description": "RGB mechanical keyboard",
        "price": 100.00,
        "stock": 10,
    }
    payload.update(overrides)
    return client.post("/products", json=payload).json()


def test_create_order(client):
    product = _create_product(client, stock=10)

    response = client.post(
        "/orders",
        json={"items": [{"product_id": product["id"], "quantity": 3}]},
    )
    assert response.status_code == 201
    body = response.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["quantity"] == 3
    assert body["items"][0]["unit_price"] == "100.00"

    updated_product = client.get(f"/products/{product['id']}").json()
    assert updated_product["stock"] == 7


def test_create_order_product_not_found(client):
    response = client.post(
        "/orders",
        json={"items": [{"product_id": 999999, "quantity": 1}]},
    )
    assert response.status_code == 400


def test_create_order_insufficient_stock(client):
    product = _create_product(client, stock=2)

    response = client.post(
        "/orders",
        json={"items": [{"product_id": product["id"], "quantity": 5}]},
    )
    assert response.status_code == 400

    unchanged_product = client.get(f"/products/{product['id']}").json()
    assert unchanged_product["stock"] == 2


def test_create_order_invalid_quantity(client):
    product = _create_product(client)

    response = client.post(
        "/orders",
        json={"items": [{"product_id": product["id"], "quantity": 0}]},
    )
    assert response.status_code == 422


def test_create_order_empty_items(client):
    response = client.post("/orders", json={"items": []})
    assert response.status_code == 422


def test_create_order_duplicate_product_lines_checked_cumulatively(client):
    product = _create_product(client, stock=5)

    response = client.post(
        "/orders",
        json={
            "items": [
                {"product_id": product["id"], "quantity": 3},
                {"product_id": product["id"], "quantity": 3},
            ]
        },
    )
    assert response.status_code == 400

    unchanged_product = client.get(f"/products/{product['id']}").json()
    assert unchanged_product["stock"] == 5


def test_list_orders(client):
    product = _create_product(client, stock=10)
    client.post("/orders", json={"items": [{"product_id": product["id"], "quantity": 1}]})
    client.post("/orders", json={"items": [{"product_id": product["id"], "quantity": 1}]})

    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_order(client):
    product = _create_product(client, stock=10)
    created = client.post(
        "/orders", json={"items": [{"product_id": product["id"], "quantity": 1}]}
    ).json()

    response = client.get(f"/orders/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_order_not_found(client):
    response = client.get("/orders/999999")
    assert response.status_code == 404
