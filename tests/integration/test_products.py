def _create_product(client, **overrides):
    payload = {
        "name": "Mechanical Keyboard",
        "description": "RGB mechanical keyboard",
        "price": 2500.00,
        "stock": 20,
    }
    payload.update(overrides)
    return client.post("/products", json=payload)


def test_create_product(client):
    response = _create_product(client)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Mechanical Keyboard"
    assert body["stock"] == 20
    assert "id" in body


def test_create_product_invalid(client):
    response = _create_product(client, price=-1)
    assert response.status_code == 422


def test_list_products(client):
    _create_product(client, name="Product A")
    _create_product(client, name="Product B")

    response = client.get("/products")
    assert response.status_code == 200
    names = [p["name"] for p in response.json()]
    assert "Product A" in names
    assert "Product B" in names


def test_get_product(client):
    created = _create_product(client).json()

    response = client.get(f"/products/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_product_not_found(client):
    response = client.get("/products/999999")
    assert response.status_code == 404


def test_update_product(client):
    created = _create_product(client).json()

    response = client.put(
        f"/products/{created['id']}",
        json={
            "name": "Updated Keyboard",
            "description": "Updated description",
            "price": 3000.00,
            "stock": 5,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Updated Keyboard"
    assert body["stock"] == 5


def test_update_product_not_found(client):
    response = client.put(
        "/products/999999",
        json={"name": "X", "price": 10, "stock": 1},
    )
    assert response.status_code == 404


def test_delete_product(client):
    created = _create_product(client).json()

    response = client.delete(f"/products/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/products/{created['id']}")
    assert response.status_code == 404


def test_delete_product_not_found(client):
    response = client.delete("/products/999999")
    assert response.status_code == 404
