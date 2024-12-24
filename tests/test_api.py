import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.api import app, get_db

# SQLALCHEMY_DATABASE_URL = "postgresql://ironman@localhost:5433/test_ecommerce"
SQLALCHEMY_DATABASE_URL = "postgresql://ironman:ironman@test_db:5432/test_ecommerce"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

class TestProducts:
    def test_create_product(self, client):
        response = client.post(
            "/products/", 
            json={
                "name": "Test Product",
                "description": "Test Description",
                "price": 9.99,
                "stock": 10
            }
        )
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Product"
        assert "id" in data
        return data["id"]

    def test_get_products(self, client):
        self.test_create_product(client)
        
        response = client.get("/products/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0

class TestOrders:
    @pytest.fixture
    def test_product(self, client):
        response = client.post(
            "/products/",
            json={
                "name": "Test Product",
                "description": "Test Description",
                "price": 9.99,
                "stock": 10
            }
        )
        assert response.status_code == 200
        return response.json()

    def test_create_order(self, client, test_product):
        response = client.post(
            "/orders/",
            json={"items": [{"product_id": test_product["id"], "quantity": 2}]}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "pending"
        assert "id" in data
        return data["id"]

    def test_get_orders(self, client, test_product):
        # Create an order first to ensure there's data
        self.test_create_order(client, test_product)
        
        response = client.get("/orders/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0

    def test_update_order_status(self, client, test_product):
        order_id = self.test_create_order(client, test_product)
        
        response = client.put(
            f"/orders/{order_id}/", 
            json={"status": "completed"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"

    def test_invalid_order_status(self, client, test_product):
        order_id = self.test_create_order(client, test_product)
        
        response = client.put(
            f"/orders/{order_id}/",  
            json={"status": "gibberish"}
        )
        assert response.status_code == 400

    def test_insufficient_stock(self, client):
        # Create a product with low stock
        product_response = client.post(
            "/products/",
            json={
                "name": "Low Stock Product",
                "description": "Test Description",
                "price": 9.99,
                "stock": 1
            }
        )
        assert product_response.status_code == 200
        product_id = product_response.json()["id"]
        
        # Trying to order more than available stock
        response = client.post(
            "/orders/",
            json={"items": [{"product_id": product_id, "quantity": 2}]}
        )
        assert response.status_code == 400