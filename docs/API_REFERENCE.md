# 📚 API Reference - SkinCare Nepal AI

Complete API endpoint documentation with examples.

**Base URL:** `http://localhost:8000` (dev) or `https://your-domain.app` (prod)

---

## Authentication

### JWT Token Format
```
Header: Authorization: Bearer <your_jwt_token>
```

### Example JWT Token
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlbWFpbEBleGFtcGxlLmNvbSIsInVzZXJfaWQiOjEsImV4cCI6MTY4MjQ1OTg3MH0.xxx...
```

---

## 🏥 Health & Status

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "message": "SkinCare Nepal AI API is running!",
  "version": "0.1.0"
}
```

---

## 👤 User Management

### Register New User
```http
POST /api/users/register
Content-Type: application/json
```

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+977-9841234567",
  "age": 25,
  "gender": "male",
  "password": "SecurePassword123"
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "message": "User registered successfully"
}
```

**Error (400):**
```json
{
  "detail": "User with this email or phone already exists"
}
```

---

### User Login
```http
POST /api/auth/login
Content-Type: application/json
```

**Request:**
```json
{
  "email": "john@example.com",
  "password": "SecurePassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "message": "Login successful"
}
```

**Error (401):**
```json
{
  "detail": "Invalid email or password"
}
```

---

### Get Current User Profile (Protected)
```http
GET /api/users/me
Authorization: Bearer <your_jwt_token>
```

**Response (200):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+977-9841234567",
  "age": 25,
  "gender": "male",
  "created_at": "2026-06-26T06:53:22.532579"
}
```

**Error (401):**
```json
{
  "detail": "Invalid or expired token"
}
```

---

### Get User by ID
```http
GET /api/users/{user_id}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+977-9841234567",
  "age": 25,
  "gender": "male",
  "created_at": "2026-06-26T06:53:22.532579"
}
```

**Error (404):**
```json
{
  "error": "User not found"
}
```

---

## 💳 Payments

### Initiate Payment (Protected)
```http
POST /api/payments/initiate
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

**Request:**
```json
{
  "amount_npr": 500,
  "product_name": "Dermatologist Consultation",
  "description": "30-minute consultation with Dr. Sharma"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Test mode - payment initialized",
  "payment_url": "https://khalti.com/...",
  "token": "TEST_TOKEN_CONS_USER1_20260626",
  "purchase_order_id": "CONS_USER1_20260626120000"
}
```

---

### Verify Payment (Protected)
```http
POST /api/payments/verify
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

**Query Parameters:**
- `order_id`: Purchase order ID
- `token`: Payment token from Khalti

**Response (200):**
```json
{
  "success": true,
  "message": "Payment verified successfully",
  "transaction_id": "TEST_TOKEN_CONS_USER1",
  "order_id": "CONS_USER1_20260626120000"
}
```

---

## 🔍 AI Skin Analysis

### Upload Photo for Analysis (Protected)
```http
POST /api/analysis/upload
Authorization: Bearer <your_jwt_token>
Content-Type: multipart/form-data
```

**Parameters:**
- `user_id`: Your user ID
- `photo_type`: "front" | "left" | "right"
- `file`: Image file (.jpg, .png)

**Response (200):**
```json
{
  "analysis_id": 1,
  "photo_type": "front",
  "conditions_detected": [
    {
      "name": "Acne",
      "confidence": 0.85,
      "severity": "medium"
    },
    {
      "name": "Oily Skin",
      "confidence": 0.78,
      "severity": "low"
    }
  ],
  "skin_health_score": 65,
  "recommendations": [
    {
      "type": "cleanser",
      "time": "morning",
      "recommendation": "Salicylic acid face wash (BHA)",
      "priority": "high"
    }
  ]
}
```

---

### Get Analysis Results
```http
GET /api/analysis/{analysis_id}
```

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "photo_type": "front",
  "skin_health_score": 65,
  "conditions": [
    {"name": "Acne", "confidence": 0.85}
  ],
  "created_at": "2026-06-26T07:10:00"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authorization header missing"
}
```

### 403 Forbidden
```json
{
  "detail": "User account is inactive"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting (Future)

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1682459870
```

---

## Pagination (Future)

```http
GET /api/users?page=1&limit=10
```

**Response:**
```json
{
  "data": [...],
  "page": 1,
  "total": 100,
  "pages": 10
}
```

---

## API Versioning

Current version: `v0.1.0`

**Version in URLs (future):**
```
/api/v1/users/register
/api/v2/users/register
```

---

## cURL Examples

### Register
```bash
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "email": "john@example.com",
    "phone": "+977-9841234567",
    "age": 25,
    "gender": "male",
    "password": "Pass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "Pass123"
  }'
```

### Protected Endpoint
```bash
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Upload Photo
```bash
curl -X POST http://localhost:8000/api/analysis/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "user_id=1" \
  -F "photo_type=front" \
  -F "file=@photo.jpg"
```

---

## Testing with Postman

1. Import collection from `/docs/Postman_Collection.json` (create manually)
2. Set `base_url` variable: `http://localhost:8000`
3. Set `jwt_token` variable after login
4. Run requests

---

## WebSocket (Coming Soon)

Real-time chat with doctors:
```javascript
ws://localhost:8000/ws/chat/{consultation_id}
```

---

## GraphQL (Coming Soon)

Alternative to REST:
```
POST /graphql
```

---

**API is fully documented and ready for integration!** 📡
