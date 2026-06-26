# ⚡ Quick Start (TL;DR Version)

## Installation (First Time Only)

```powershell
# 1. Install Python 3.11+
# Download from python.org

# 2. Install PostgreSQL 15+
# Download from postgresql.org

# 3. Navigate to project
cd "D:\Davinci Projects Files\CLAUDE\skincare-nepal-ai"

# 4. Create virtual environment
python -m venv venv

# 5. Activate virtual environment
venv\Scripts\activate

# 6. Install dependencies
pip install -r requirements.txt

# 7. Create database
createdb -U postgres skincare_nepal

# 8. Configure .env
# Copy .env.example to .env
# Edit DATABASE_URL with your PostgreSQL password
Copy-Item .env.example .env
code .env
```

## Running the Server (Every Time)

```powershell
# Navigate to project folder
cd "D:\Davinci Projects Files\CLAUDE\skincare-nepal-ai"

# Activate virtual environment
venv\Scripts\activate

# Start server
uvicorn backend.main:app --reload

# Open browser to http://localhost:8000/docs
```

## Stop Server

```
Ctrl + C (in PowerShell)
```

## Useful Commands

```powershell
# Test API health
curl http://localhost:8000/health

# View database
psql -U postgres -d skincare_nepal

# List all tables
\dt

# Deactivate virtual environment
deactivate
```

## Project Structure

```
skincare-nepal-ai/
├── backend/
│   ├── main.py              ← API endpoints
│   ├── models.py            ← Database tables
│   ├── database.py          ← Database connection
│   ├── vision_api.py        ← AI analysis
│   └── khalti_payment.py    ← Payment processing
├── docs/
│   ├── SETUP.md            ← Full setup guide (YOU ARE HERE)
│   ├── API.md              ← API documentation
│   └── DATABASE.md         ← Database schema
├── requirements.txt         ← Dependencies
├── .env.example            ← Environment variables template
├── .env                    ← Your settings (create from .env.example)
└── README.md               ← Full documentation
```

## Common Endpoints to Test

1. **Health Check** (API is running?)
   ```
   GET http://localhost:8000/health
   ```

2. **Register User**
   ```
   POST http://localhost:8000/api/users/register
   ```

3. **Upload Photo & Analyze**
   ```
   POST http://localhost:8000/api/analysis/upload
   ```

4. **Get User Profile**
   ```
   GET http://localhost:8000/api/users/{user_id}
   ```

Visit http://localhost:8000/docs to test all endpoints interactively!

## What's Included

✅ FastAPI backend setup
✅ PostgreSQL database configuration
✅ User registration system
✅ AI skin analysis structure (Google Cloud Vision ready)
✅ Khalti payment integration skeleton
✅ Database models (Users, Analysis, Doctors, Products, Orders, Chats)
✅ Full API documentation

## What's Next

Week 2-3:
- [ ] Add JWT authentication
- [ ] Add Khalti payment integration
- [ ] Add doctor registration
- [ ] Add chat functionality

Week 4:
- [ ] Deploy to Railway.app

---

For detailed setup help, see `docs/SETUP.md`
