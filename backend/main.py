"""
SkinCare Nepal AI - FastAPI Backend (Minimal MVP)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SkinCare Nepal AI API",
    description="AI-powered skincare analysis platform for Nepal",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== HEALTH CHECK =====
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running!", "version": "0.1.0"}

# ===== HOME =====
@app.get("/")
def home():
    """Welcome endpoint"""
    return {
        "name": "SkinCare Nepal AI",
        "description": "AI-powered skincare analysis & consultation",
        "endpoints": {
            "/health": "Health check",
            "/api/users/register": "User registration",
            "/api/auth/login": "User login",
            "/api/users/me": "Get current user",
        }
    }

# ===== SIMPLE USER ENDPOINTS (without database) =====
from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    phone: str
    age: int
    gender: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Mock user storage (in-memory for MVP testing)
mock_users = {}

@app.post("/api/users/register")
def register_user(user: UserRegister):
    """Register a new user"""
    if user.email in mock_users:
        return {"error": "User already exists"}, 400

    mock_users[user.email] = {
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "age": user.age,
        "gender": user.gender,
    }
    return {
        "id": len(mock_users),
        "name": user.name,
        "email": user.email,
        "message": "User registered successfully"
    }

@app.post("/api/auth/login")
def login_user(request: LoginRequest):
    """User login"""
    if request.email not in mock_users:
        return {"error": "User not found"}, 401

    return {
        "access_token": "mock_token_" + request.email,
        "token_type": "bearer",
        "user_id": 1,
        "email": request.email
    }

@app.get("/api/users/me")
def get_current_user():
    """Get current user"""
    return {
        "id": 1,
        "email": "test@example.com",
        "name": "Test User",
        "message": "Mock user data - database not configured yet"
    }

# ===== SKIN ANALYSIS MOCK =====
@app.post("/api/analysis/upload")
def analyze_skin():
    """Mock skin analysis endpoint"""
    return {
        "analysis_id": 1,
        "skin_health_score": 75,
        "conditions_detected": ["slight_acne", "oily_skin"],
        "recommendations": [
            "Use gentle cleanser twice daily",
            "Apply sunscreen SPF 30+",
            "Consider salicylic acid treatment"
        ]
    }

# ===== PAYMENT MOCK =====
@app.post("/api/payments/initiate")
def initiate_payment(amount: int):
    """Mock payment initiation"""
    return {
        "payment_id": "PAY123456",
        "amount": amount,
        "status": "pending",
        "message": "Mock payment - Khalti not configured yet"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
