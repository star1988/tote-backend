from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tote and Trend API is running"}

def get_auth_token():
    response = client.post("/login", data={"username": "admin", "password": "changeme123"})
    return response.json()["access_token"]

def test_create_product_requires_auth():
    response = client.post("/products/", json={
        "name": "Test Tote", "price": 10.0, "stock": 5, "category": "Bags"
    })
    assert response.status_code == 401

def test_create_product_with_auth():
    token = get_auth_token()
    response = client.post(
        "/products/",
        json={"name": "Test Tote", "price": 10.0, "stock": 5, "category": "Bags"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tote"

def test_order_fails_with_insufficient_stock():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    product_response = client.post(
        "/products/",
        json={"name": "Low Stock Tote", "price": 8.0, "stock": 2, "category": "Bags"},
        headers=headers
    )
    product_id = product_response.json()["id"]
    
    order_response = client.post(
        "/orders/",
        json={"product_id": product_id, "quantity": 10, "customer_name": "Test Customer"},
        headers=headers
    )
    assert order_response.status_code == 400