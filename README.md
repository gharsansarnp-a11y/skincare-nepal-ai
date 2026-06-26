# SkinCare Nepal AI - Backend API

🇳🇵 Nepal's first AI-powered dermatology platform combining AI analysis, doctor consultations, and Ayurvedic skincare.

## Overview

This is the backend API for SkinCare Nepal AI built with:
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **AI/ML**: Google Cloud Vision API
- **Hosting**: Railway.app (production) / Local development

## Current Status

- **Phase**: MVP (Minimum Viable Product) - Week 1-2 of 12-week roadmap
- **Features**: User registration, AI skin analysis, database setup
- **Testing**: Can be run locally with test data

## Project Structure

```
skincare-nepal-ai/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── models.py            # Database table definitions
│   ├── database.py          # PostgreSQL connection
│   ├── vision_api.py        # Google Cloud Vision integration
│   ├── khalti_payment.py    # Payment gateway integration
│   └── requirements.txt
├── docs/
│   ├── SETUP.md            # Detailed setup guide
│   ├── API.md              # API documentation
│   └── DATABASE.md         # Database schema
├── .env.example            # Environment variables template
├── .gitignore
└── README.md              # This file
```

## Quick Start (5 minutes)

### 1. Prerequisites
- Python 3.9+ installed ([python.org](https://python.org))
- PostgreSQL 12+ installed ([postgresql.org](https://postgresql.org))
- Git installed ([git-scm.com](https://git-scm.com))

### 2. Clone & Setup

```bash
# Navigate to project
cd skincare-nepal-ai

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb skincare_nepal

# Update .env file with database URL
# Copy .env.example to .env and edit
cp .env.example .env

# Edit .env and set:
# DATABASE_URL=postgresql://username:password@localhost:5432/skincare_nepal
```

### 4. Run API

```bash
# Start development server
uvicorn backend.main:app --reload

# Server will run at: http://localhost:8000
# API docs at: http://localhost:8000/docs
# ReDoc at: http://localhost:8000/redoc
```

## API Endpoints

### Health Check
```
GET /health
```
Check if API is running.

### User Registration
```
POST /api/users/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+977-9841234567",
  "age": 25,
  "gender": "male"
}
```

### Upload Skin Photo (AI Analysis)
```
POST /api/analysis/upload
Content-Type: multipart/form-data

Parameters:
- user_id: 1
- photo_type: "front" | "left" | "right"
- file: image.jpg
```

Response:
```json
{
  "analysis_id": 1,
  "photo_type": "front",
  "conditions_detected": [
    {"name": "Acne", "confidence": 0.85},
    {"name": "Oily Skin", "confidence": 0.78}
  ],
  "skin_health_score": 65,
  "recommendations": [...]
}
```

### Get Analysis Results
```
GET /api/analysis/{analysis_id}
```

### Get User Profile
```
GET /api/users/{user_id}
```

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/user-authentication
   ```

2. **Make changes to code**
   ```
   Edit backend/*.py files
   ```

3. **Test locally**
   ```bash
   # Test endpoint with curl
   curl -X GET http://localhost:8000/health
   ```

4. **Commit & push**
   ```bash
   git add .
   git commit -m "Add user authentication"
   git push origin feature/user-authentication
   ```

### Testing

Run tests with pytest:
```bash
pytest backend/ -v
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/skincare_nepal

# Google Cloud Vision API
GOOGLE_CLOUD_CREDENTIALS_PATH=./credentials/google-cloud-key.json

# Payment Gateways
KHALTI_PUBLIC_KEY=your_key_here
KHALTI_SECRET_KEY=your_secret_here
STRIPE_PUBLIC_KEY=your_key_here
STRIPE_SECRET_KEY=your_secret_here

# JWT
SECRET_KEY=your_super_secret_key_here

# Server
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

## Database Schema

Main tables:
- `users` - User accounts
- `analysis_results` - AI skin analysis results
- `doctors` - Dermatologist profiles
- `consultations` - Doctor-patient sessions
- `products` - Skincare products
- `orders` - Product orders
- `chat_messages` - Messages between users and doctors

See `docs/DATABASE.md` for full schema.

## Deployment

### To Railway.app (Production)

1. **Create Railway account**: railway.app
2. **Connect GitHub repo**
3. **Set environment variables** in Railway dashboard
4. **Deploy with**: `git push`

### Local PostgreSQL

```bash
# Install PostgreSQL
# Create database
createdb skincare_nepal

# Connect with psql
psql -U postgres -d skincare_nepal
```

### Google Cloud Vision API Setup

1. Create Google Cloud project
2. Enable Vision API
3. Create service account + key
4. Download JSON key → `credentials/google-cloud-key.json`
5. Set `GOOGLE_CLOUD_CREDENTIALS_PATH` in .env

## Common Issues

### "ModuleNotFoundError: No module named 'backend'"
```bash
# Make sure __init__.py exists in backend/
touch backend/__init__.py
```

### "Database connection failed"
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Update DATABASE_URL in .env
# Format: postgresql://username:password@localhost:5432/database_name
```

### "Google Cloud Vision API error"
```bash
# Check credentials path
ls credentials/google-cloud-key.json

# Verify permissions on file
chmod 600 credentials/google-cloud-key.json
```

## Next Steps

- [ ] Week 2: User authentication (JWT)
- [ ] Week 3: Khalti payment integration
- [ ] Week 4: Deploy to Railway
- [ ] Week 5: Doctor portal
- [ ] Week 6: Chat integration

See `docs/ROADMAP.md` for full 12-week plan.

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

## License

MIT License - See LICENSE file

## Support

Questions? Issues?
- Create GitHub issue
- Email: support@skincarenepal.app
- WhatsApp: [Contact info]

---

**Built with ❤️ for Nepal**
