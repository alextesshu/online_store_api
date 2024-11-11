import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# Utility function to create a category for tests
async def create_test_category(ac, name="Test Category"):
    category_data = {
        "name": name
    }
    response = await ac.post("/categories/", json=category_data)
    assert response.status_code == 200
    return response.json()

# Utility function to create a product for tests
async def create_test_product(ac, name="Test Product", category_id=1, price=99.99, stock=10):
    product_data = {
        "name": name,
        "category_id": category_id,
        "price": price,
        "stock": stock
    }
    response = await ac.post("/products/", json=product_data)
    assert response.status_code == 200
    return response.json()

@pytest.mark.asyncio
async def test_read_products():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        category = await create_test_category(ac)
        product = await create_test_product(ac, name="Test Product", category_id=category["id"])
        assert product["name"] == "Test Product"
        assert round(product["price"], 2) == 99.99
        assert product["stock"] == 10
    
@pytest.mark.asyncio
async def test_delete_product():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        category = await create_test_category(ac)
        product = await create_test_product(ac, name="Product to Delete", category_id=category["id"])
        product_id = product["id"]
        
        # Delete the created product
        delete_response = await ac.delete(f"/products/{product_id}")
        assert delete_response.status_code == 200

        # Verify the product was deleted
        get_response = await ac.get(f"/products/{product_id}")
        assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_update_price():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        category = await create_test_category(ac)
        product = await create_test_product(ac, name="Product to Update Price", category_id=category["id"])
        product_id = product["id"]

        new_price = 150.0
        update_response = await ac.patch(f"/products/{product_id}/price", json={"new_price": new_price})
        assert update_response.status_code == 200
        assert update_response.json()["price"] == new_price
        
@pytest.mark.asyncio
async def test_reserve_product():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        category = await create_test_category(ac)
        product = await create_test_product(ac, name="Product to Reserve", category_id=category["id"])
        product_id = product["id"]

        reserve_response = await ac.post(f"/products/{product_id}/reserve")
        assert reserve_response.status_code == 200
        assert reserve_response.json()["reserved_quantity"] == 1
        assert reserve_response.json()["stock"] == product["stock"]
        
@pytest.mark.asyncio
async def test_cancel_reservation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        category = await create_test_category(ac)
        product = await create_test_product(ac, name="Product to Cancel Reservation", category_id=category["id"])
        product_id = product["id"]

        await ac.post(f"/products/{product_id}/reserve")  # Reserve product first
        cancel_response = await ac.delete(f"/products/{product_id}/cancel-reservation")
        assert cancel_response.status_code == 200
        assert cancel_response.json()["reserved_quantity"] == 0
        assert cancel_response.json()["stock"] == product["stock"]
        
@pytest.mark.asyncio
async def test_sell_product():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        category = await create_test_category(ac)
        product = await create_test_product(ac, name="Product to Sell", category_id=category["id"], stock=1)
        product_id = product["id"]

        # Reserve a product first
        reserve_response = await ac.post(f"/products/{product_id}/reserve")
        print("Reserve response data:", reserve_response.json())
        assert reserve_response.status_code == 200
        assert reserve_response.json()["reserved_quantity"] == 1

        # Sell the product
        sell_response = await ac.post(f"/products/{product_id}/sell")
        print("Sell response data:", sell_response.json())
        assert sell_response.status_code == 200

        product_after_sell = sell_response.json()
        assert product_after_sell["stock"] == 0
        assert product_after_sell["reserved_quantity"] == 0
        assert product_after_sell["is_available"] is False
        print("Product after sell:", product_after_sell)
        
