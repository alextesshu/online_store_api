import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_read_products():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        product_data = {
            "name": "Test Product",
            "category_id": 1,
            "price": 99.99,
            "stock": 10
        }
        response = await ac.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
    assert response.json()["price"] == 99.99
    assert response.json()["stock"] == 10
    
@pytest.mark.asyncio
async def test_delete_product():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Create a product for deletion test
        product_data = {
            "name": "Product to Delete",
            "category_id": 1,
            "price": 100.0,
            "stock": 10
        }
        create_response = await ac.post("/products/", json=product_data)
        assert create_response.status_code == 200
        product_id = create_response.json()["id"]

        # Delete the created product
        delete_response = await ac.delete(f"/products/{product_id}")
        assert delete_response.status_code == 200

        # Verify the product was deleted
        get_response = await ac.get(f"/products/{product_id}")
        assert get_response.status_code == 404
