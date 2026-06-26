"""
SkinCare Nepal AI - FastAPI Backend Entry Point

This is the main file that starts the API server.
All API endpoints are defined here or imported from other modules.

To run: uvicorn backend.main:app --reload
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from datetime import timedelta

# Import our custom modules
from backend.database import engine, get_db
from backend import models
from backend.vision_api import analyze_skin_image
from backend.auth import (
    hash_password, verify_password, create_access_token,
    verify_token, get_token_from_header, Token, LoginRequest
)
from backend.khalti_payment import initiate_payment, verify_payment

# Load environment variables from .env file
load_dotenv()

# Create the FastAPI app instance
app = FastAPI(
    title="SkinCare Nepal AI API",
    description="AI-powered skincare analysis & consultation platform for Nepal",
    version="0.1.0"
)

# Create database tables on startup (optional - database connection not required for MVP health check)
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not connect to database: {e}")
    print("API will run but database features will be limited")

# Configure CORS (Cross-Origin Resource Sharing) to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== HEALTH CHECK ENDPOINT =====
@app.get("/health")
def health_check():
    """
    Simple endpoint to check if API is running.
    Useful for testing before implementing real features.
    """
    return {
        "status": "ok",
        "message": "SkinCare Nepal AI API is running!",
        "version": "0.1.0"
    }

# ===== USER REGISTRATION ENDPOINT =====
from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    phone: str
    age: int
    gender: str
    password: str

@app.post("/api/users/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user with password authentication.

    Request body:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+977-9841234567",
        "age": 25,
        "gender": "male",
        "password": "SecurePassword123"
    }

    Response:
    {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "message": "User registered successfully"
    }
    """

    # Validate password length
    if len(user.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters long"
        )

    # Check if user already exists
    existing_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.phone == user.phone)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email or phone already exists"
        )

    # Create new user with hashed password
    new_user = models.User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        age=user.age,
        gender=user.gender,
        password_hash=hash_password(user.password)
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "message": "User registered successfully"
    }

# ===== LOGIN ENDPOINT =====
@app.post("/api/auth/login", response_model=Token)
def login_user(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login user and get JWT access token.

    Request body:
    {
        "email": "john@example.com",
        "password": "SecurePassword123"
    }

    Response:
    {
        "access_token": "eyJhbGc...",
        "token_type": "bearer",
        "user_id": 1,
        "message": "Login successful"
    }
    """

    # Find user by email
    user = db.query(models.User).filter(
        models.User.email == credentials.email
    ).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    # Create JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "message": "Login successful"
    }

# ===== VERIFY TOKEN HELPER =====
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    Dependency to verify JWT token and get current user.
    Use this in protected endpoints.
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    token = get_token_from_header(authorization)
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid token format"
        )

    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    email = token_data.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

# ===== PROTECTED PROFILE ENDPOINT =====
@app.get("/api/users/me")
def get_my_profile(current_user = Depends(get_current_user)):
    """
    Get current user's profile (protected endpoint).

    Header:
    Authorization: Bearer <your_jwt_token>

    Response:
    {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        ...
    }
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "age": current_user.age,
        "gender": current_user.gender,
        "created_at": current_user.created_at
    }

# ===== PAYMENT ENDPOINTS =====
class PaymentRequest(BaseModel):
    amount_npr: float  # Amount in Nepali Rupees
    product_name: str  # "Consultation", "Product", etc.
    description: str

@app.post("/api/payments/initiate")
def initiate_payment_endpoint(
    payment_request: PaymentRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Initiate a payment for consultation/product.

    Header:
    Authorization: Bearer <jwt_token>

    Request body:
    {
        "amount_npr": 500,
        "product_name": "Dermatologist Consultation",
        "description": "30-minute consultation with Dr. Sharma"
    }

    Response:
    {
        "success": True,
        "payment_url": "https://khalti.com/...",
        "token": "payment_token",
        "purchase_order_id": "CONS_USER4_20260626"
    }
    """
    # Generate unique order ID
    from datetime import datetime
    purchase_order_id = f"CONS_USER{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    # Convert NPR to paisa (1 NPR = 100 paisa)
    amount_paisa = int(payment_request.amount_npr * 100)

    # Initiate payment with Khalti
    result = initiate_payment(
        amount=amount_paisa,
        purchase_order_id=purchase_order_id,
        customer_name=current_user.name,
        customer_email=current_user.email,
        customer_phone=current_user.phone,
        product_name=payment_request.product_name,
        return_url=f"https://skincarenepal.app/payment/verify?order_id={purchase_order_id}"
    )

    return result

@app.post("/api/payments/verify")
def verify_payment_endpoint(
    order_id: str,
    token: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify payment after Khalti callback.

    Query params:
    - order_id: Purchase order ID
    - token: Payment token from Khalti

    Response:
    {
        "success": True,
        "message": "Payment verified",
        "transaction_id": "txn_123"
    }
    """
    # Verify with Khalti
    result = verify_payment(token=token, amount=None)  # Amount not needed for verification

    if result.get("success"):
        # Save payment record to database
        # (In a full implementation, create a Payment model and save here)
        return {
            "success": True,
            "message": "Payment verified successfully",
            "transaction_id": result.get("transaction_id", token),
            "order_id": order_id
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=result.get("error", "Payment verification failed")
        )

# ===== AI SKIN ANALYSIS ENDPOINT =====
@app.post("/api/analysis/upload")
async def upload_skin_photo(
    user_id: int,
    photo_type: str,  # "front", "left", "right"
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a skin photo and get AI analysis.

    Parameters:
    - user_id: ID of the user (from registration)
    - photo_type: "front" or "left" or "right" (3-photo scan required)
    - file: Image file (.jpg, .png)

    Response:
    {
        "analysis_id": 1,
        "photo_type": "front",
        "conditions_detected": [
            {"name": "Acne", "confidence": 0.85},
            {"name": "Oily Skin", "confidence": 0.78}
        ],
        "skin_health_score": 65,
        "message": "Analysis completed"
    }
    """

    # Verify user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Save uploaded file temporarily
    file_path = f"uploads/{user_id}_{photo_type}.jpg"
    os.makedirs("uploads", exist_ok=True)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Call Google Cloud Vision API
    analysis_result = analyze_skin_image(file_path)

    # Save analysis to database
    new_analysis = models.AnalysisResult(
        user_id=user_id,
        photo_type=photo_type,
        raw_data=analysis_result,
        skin_health_score=analysis_result.get("skin_health_score", 50),
        conditions_detected=analysis_result.get("conditions", [])
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return {
        "analysis_id": new_analysis.id,
        "photo_type": photo_type,
        "conditions_detected": analysis_result.get("conditions", []),
        "skin_health_score": analysis_result.get("skin_health_score", 50),
        "recommendations": analysis_result.get("recommendations", []),
        "message": "Analysis completed"
    }

# ===== GET ANALYSIS RESULTS =====
@app.get("/api/analysis/{analysis_id}")
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """
    Get previous analysis results by ID.
    """
    analysis = db.query(models.AnalysisResult).filter(
        models.AnalysisResult.id == analysis_id
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "id": analysis.id,
        "user_id": analysis.user_id,
        "photo_type": analysis.photo_type,
        "skin_health_score": analysis.skin_health_score,
        "conditions": analysis.conditions_detected,
        "created_at": analysis.created_at
    }

# ===== USER PROFILE ENDPOINT =====
@app.get("/api/users/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Get user profile information.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "age": user.age,
        "gender": user.gender,
        "created_at": user.created_at
    }

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to SkinCare Nepal AI",
        "documentation": "/docs",
        "health": "/health"
    }

# ===== ERROR HANDLER =====
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000))
    )
