"""
Database Models - Defines the structure of all tables

Using SQLAlchemy ORM to define tables in a Pythonic way.
Each class represents a table in PostgreSQL.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# ===== USER TABLE =====
class User(Base):
    """
    Stores user account information
    """
    __tablename__ = "users"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)  # "male", "female", "other"
    password_hash = Column(String(255), nullable=False)  # Bcrypt hashed password
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    analyses = relationship("AnalysisResult", back_populates="user")
    consultations = relationship("Consultation", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"


# ===== ANALYSIS RESULT TABLE =====
class AnalysisResult(Base):
    """
    Stores AI skin analysis results for each photo upload
    """
    __tablename__ = "analysis_results"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    photo_type = Column(String(20), nullable=False)  # "front", "left", "right"
    photo_url = Column(String(500), nullable=True)  # Path to stored image

    # Analysis scores (0-100)
    skin_health_score = Column(Integer, default=50)
    acne_score = Column(Integer, default=0)
    pigmentation_score = Column(Integer, default=0)
    hydration_score = Column(Integer, default=50)
    sensitivity_score = Column(Integer, default=0)

    # Detected conditions (stored as JSON)
    conditions_detected = Column(JSON, default=[])  # [{"name": "Acne", "confidence": 0.85}, ...]
    recommendations = Column(JSON, default=[])  # [{"type": "cleanser", "product": "..."}, ...]

    # Raw API response (for debugging)
    raw_data = Column(JSON, nullable=True)

    # Status
    is_reviewed_by_doctor = Column(Boolean, default=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    doctor_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="analyses")
    doctor = relationship("Doctor", back_populates="analyses_reviewed")

    def __repr__(self):
        return f"<AnalysisResult(id={self.id}, user_id={self.user_id}, photo_type={self.photo_type})>"


# ===== DOCTOR TABLE =====
class Doctor(Base):
    """
    Stores dermatologist information
    """
    __tablename__ = "doctors"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, nullable=False)
    specialization = Column(String(100), default="Dermatology")
    nmc_license_number = Column(String(50), unique=True, nullable=False)  # Nepal Medical Council
    nmc_verified = Column(Boolean, default=False)
    bio = Column(Text, nullable=True)
    profile_photo_url = Column(String(500), nullable=True)

    # Rating and stats
    average_rating = Column(Float, default=0.0)
    total_consultations = Column(Integer, default=0)
    response_time_hours = Column(Integer, default=24)  # Target response time

    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    analyses_reviewed = relationship("AnalysisResult", back_populates="doctor")
    consultations = relationship("Consultation", back_populates="doctor")

    def __repr__(self):
        return f"<Doctor(id={self.id}, name={self.name}, nmc={self.nmc_license_number})>"


# ===== CONSULTATION TABLE =====
class Consultation(Base):
    """
    Stores paid consultation sessions between user and doctor
    """
    __tablename__ = "consultations"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"), nullable=True)

    # Consultation details
    status = Column(String(20), default="pending")  # "pending", "active", "completed", "cancelled"
    consultation_type = Column(String(20), default="chat")  # "chat", "video", "both"

    # Payment info
    amount = Column(Float, nullable=False)  # In NPR
    currency = Column(String(10), default="NPR")
    payment_method = Column(String(50), nullable=True)  # "khalti", "stripe", "bank_transfer"
    payment_id = Column(String(100), nullable=True)  # Reference to payment gateway
    is_paid = Column(Boolean, default=False)

    # Ratings
    user_rating = Column(Integer, nullable=True)  # 1-5
    user_review = Column(Text, nullable=True)

    # Timestamps
    scheduled_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="consultations")
    doctor = relationship("Doctor", back_populates="consultations")

    def __repr__(self):
        return f"<Consultation(id={self.id}, user_id={self.user_id}, doctor_id={self.doctor_id}, status={self.status})>"


# ===== PRODUCT TABLE =====
class Product(Base):
    """
    Stores skincare products available for purchase
    """
    __tablename__ = "products"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    category = Column(String(100), nullable=False)  # "face_wash", "moisturizer", "sunscreen", "ayurveda", etc.
    brand = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)  # In NPR
    image_url = Column(String(500), nullable=True)

    # Commission for affiliate/marketplace
    commission_percentage = Column(Float, default=15.0)  # 10-20% depending on partner
    partner_name = Column(String(100), nullable=True)  # "Bhaskar", "Patanjali", "ePharmacy", etc.
    partner_url = Column(String(500), nullable=True)  # Link to product page

    # Inventory
    stock_quantity = Column(Integer, default=0)
    is_in_stock = Column(Boolean, default=True)

    # Status
    is_active = Column(Boolean, default=True)
    is_recommended = Column(Boolean, default=False)  # Featured products
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    orders = relationship("Order", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"


# ===== ORDER TABLE =====
class Order(Base):
    """
    Stores product orders
    """
    __tablename__ = "orders"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    consultation_id = Column(Integer, ForeignKey("consultations.id"), nullable=True)  # Optional: recommended by doctor

    # Order details
    quantity = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)
    currency = Column(String(10), default="NPR")

    # Payment
    payment_method = Column(String(50), nullable=True)
    payment_id = Column(String(100), nullable=True)
    is_paid = Column(Boolean, default=False)

    # Shipping
    status = Column(String(20), default="pending")  # "pending", "processing", "shipped", "delivered", "cancelled"
    tracking_number = Column(String(100), nullable=True)
    delivery_date = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User")
    product = relationship("Product", back_populates="orders")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status})>"


# ===== CHAT MESSAGE TABLE =====
class ChatMessage(Base):
    """
    Stores messages between user and doctor
    """
    __tablename__ = "chat_messages"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"), nullable=False, index=True)
    sender_type = Column(String(20), nullable=False)  # "user" or "doctor"
    sender_id = Column(Integer, nullable=False)  # Either user_id or doctor_id
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, consultation_id={self.consultation_id}, sender_type={self.sender_type})>"
