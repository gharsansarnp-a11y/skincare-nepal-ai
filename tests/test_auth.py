"""
Unit tests for authentication endpoints.

Run with: pytest tests/test_auth.py -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import from backend
import sys
sys.path.insert(0, '.')

from backend.main import app, get_db
from backend.database import Base
from backend import models
from backend.auth import hash_password, verify_password

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

class TestUserRegistration:
    """Test user registration endpoint"""

    def test_register_new_user(self):
        """Test successful user registration"""
        response = client.post(
            "/api/users/register",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "phone": "+977-9841234567",
                "age": 25,
                "gender": "male",
                "password": "TestPass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test User"
        assert data["email"] == "test@example.com"
        assert "id" in data

    def test_register_duplicate_email(self):
        """Test registration with duplicate email fails"""
        # Register first user
        client.post(
            "/api/users/register",
            json={
                "name": "User 1",
                "email": "duplicate@example.com",
                "phone": "+977-9841111111",
                "age": 25,
                "gender": "male",
                "password": "Pass123"
            }
        )

        # Try to register with same email
        response = client.post(
            "/api/users/register",
            json={
                "name": "User 2",
                "email": "duplicate@example.com",
                "phone": "+977-9841111112",
                "age": 26,
                "gender": "female",
                "password": "Pass123"
            }
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_register_short_password(self):
        """Test registration with password < 6 chars fails"""
        response = client.post(
            "/api/users/register",
            json={
                "name": "Test",
                "email": "test@example.com",
                "phone": "+977-9841234567",
                "age": 25,
                "gender": "male",
                "password": "abc"  # Too short
            }
        )
        assert response.status_code == 400
        assert "at least 6 characters" in response.json()["detail"]

class TestUserLogin:
    """Test login and JWT authentication"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test user before each test"""
        client.post(
            "/api/users/register",
            json={
                "name": "Test User",
                "email": "login@example.com",
                "phone": "+977-9840000001",
                "age": 25,
                "gender": "male",
                "password": "TestPass123"
            }
        )
        yield

    def test_login_success(self):
        """Test successful login returns JWT token"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "login@example.com",
                "password": "TestPass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user_id" in data

    def test_login_wrong_password(self):
        """Test login with wrong password fails"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "login@example.com",
                "password": "WrongPassword"
            }
        )
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    def test_login_nonexistent_user(self):
        """Test login with non-existent email fails"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "Password123"
            }
        )
        assert response.status_code == 401

class TestProtectedEndpoints:
    """Test protected endpoints requiring JWT"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test user and get JWT token"""
        client.post(
            "/api/users/register",
            json={
                "name": "Protected Test",
                "email": "protected@example.com",
                "phone": "+977-9840000002",
                "age": 25,
                "gender": "male",
                "password": "ProtectPass123"
            }
        )

        login_response = client.post(
            "/api/auth/login",
            json={
                "email": "protected@example.com",
                "password": "ProtectPass123"
            }
        )
        self.token = login_response.json()["access_token"]
        yield

    def test_get_profile_with_valid_token(self):
        """Test getting profile with valid JWT token"""
        response = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "protected@example.com"

    def test_get_profile_without_token(self):
        """Test getting profile without token fails"""
        response = client.get("/api/users/me")
        assert response.status_code == 401
        assert "Authorization header missing" in response.json()["detail"]

    def test_get_profile_invalid_token(self):
        """Test getting profile with invalid token fails"""
        response = client.get(
            "/api/users/me",
            headers={"Authorization": "Bearer invalid_token_xyz"}
        )
        assert response.status_code == 401

class TestHealthCheck:
    """Test health check endpoint"""

    def test_health_check(self):
        """Test health endpoint returns OK"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "SkinCare Nepal AI" in data["message"]
