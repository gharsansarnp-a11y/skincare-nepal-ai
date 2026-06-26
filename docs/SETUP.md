# 🚀 Step-by-Step Setup Guide for Beginners

This guide assumes **NO Python experience**. Follow each step carefully.

## Total Time: 30-45 minutes

---

## STEP 1: Install Python (10 minutes)

### For Windows:

1. Go to [python.org](https://www.python.org/downloads/)
2. Click **"Download Python 3.11"** (or latest)
3. Run the installer
4. **IMPORTANT**: Check the box **"Add Python to PATH"** ✓
5. Click **"Install Now"**
6. Wait for installation to complete

### Verify Installation:

Open PowerShell (Windows) or Terminal (Mac) and type:

```powershell
python --version
```

You should see something like: `Python 3.11.X`

If you get "command not found", restart your computer and try again.

---

## STEP 2: Install PostgreSQL Database (10 minutes)

PostgreSQL is where all your data will be stored.

### For Windows:

1. Go to [postgresql.org/download](https://www.postgresql.org/download/windows/)
2. Download **PostgreSQL 15** (or latest)
3. Run the installer
4. Follow the wizard:
   - Accept license
   - **Create password for "postgres" user** - Remember this!
   - Port: 5432 (default)
   - Locale: [Default]
   - Click Install

5. After installation, it will ask to start Stack Builder - **Skip it**

### Verify Installation:

Open PowerShell and type:

```powershell
psql --version
```

You should see: `psql (PostgreSQL) 15.X`

---

## STEP 3: Clone Project from GitHub (5 minutes)

### Open PowerShell:

1. Press `Windows Key + R`
2. Type `powershell`
3. Press Enter

### Navigate to your project folder:

```powershell
cd "D:\Davinci Projects Files\CLAUDE"
```

### Check project exists:

```powershell
cd skincare-nepal-ai
ls
```

You should see: `backend/`, `docs/`, `requirements.txt`, `.env.example`, etc.

---

## STEP 4: Create Python Virtual Environment (5 minutes)

A virtual environment is a separate Python space for your project (like a sandbox).

### In PowerShell (in the skincare-nepal-ai folder):

```powershell
python -m venv venv
```

This creates a `venv` folder. Wait 1-2 minutes.

### Activate Virtual Environment:

```powershell
venv\Scripts\activate
```

You should see `(venv)` at the start of your PowerShell prompt:

```
(venv) PS D:\Davinci Projects Files\CLAUDE\skincare-nepal-ai>
```

✓ If you see `(venv)`, you're in the virtual environment!

---

## STEP 5: Install Project Dependencies (5 minutes)

All the libraries your project needs are listed in `requirements.txt`.

### In PowerShell (with venv activated):

```powershell
pip install -r requirements.txt
```

This will take 2-3 minutes. You'll see lots of "Installing collected packages..." messages. Let it finish.

When done, you'll see: `Successfully installed X packages`

---

## STEP 6: Setup Database (5 minutes)

### Create Database:

```powershell
createdb -U postgres skincare_nepal
```

It will ask for the password you set during PostgreSQL installation. Type it (you won't see the characters).

If successful, no message = good!

### Verify Database Created:

```powershell
psql -U postgres -l
```

You should see `skincare_nepal` in the list of databases.

---

## STEP 7: Configure Environment Variables (5 minutes)

Environment variables are settings your app needs.

### Copy Template:

```powershell
Copy-Item .env.example .env
```

### Edit .env File:

Open `.env` in VS Code or Notepad:

```powershell
code .env
```

Find this line:

```
DATABASE_URL=postgresql://username:password@localhost:5432/skincare_nepal
```

Replace with:

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/skincare_nepal
```

**Replace `YOUR_PASSWORD`** with the password you set for PostgreSQL.

**Example**:
```
DATABASE_URL=postgresql://postgres:MyPassword123@localhost:5432/skincare_nepal
```

### Set JWT Secret:

Find this line:
```
SECRET_KEY=your_super_secret_key_change_this_in_production_12345
```

You can leave it as is for development.

### Save & Close

---

## STEP 8: Run the API Server (5 minutes)

### Start Server:

```powershell
uvicorn backend.main:app --reload
```

Wait 5 seconds... you should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✓ **API is now running!**

---

## STEP 9: Test the API (5 minutes)

### Open Browser:

Go to: **http://localhost:8000/docs**

You should see an interactive API documentation page! 🎉

### Test Health Endpoint:

1. Find the **GET /health** endpoint
2. Click on it (it expands)
3. Click **"Try it out"**
4. Click **"Execute"**

You should see:
```json
{
  "status": "ok",
  "message": "SkinCare Nepal AI API is running!",
  "version": "0.1.0"
}
```

---

## STEP 10: Test User Registration (5 minutes)

### Try the POST /api/users/register endpoint:

1. In the same docs page, find **POST /api/users/register**
2. Click on it
3. Click **"Try it out"**
4. In the "Request body" box, paste:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+977-9841234567",
  "age": 25,
  "gender": "male"
}
```

5. Click **"Execute"**

You should get a response:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "message": "User registered successfully"
}
```

✓ **Congratulations! Your API is working!**

---

## What's Happening Behind the Scenes?

1. You sent data to the API
2. API received it and processed
3. Data was saved to PostgreSQL database
4. Response was sent back

All 3 working together = **Full-stack development!**

---

## Common Problems & Fixes

### Problem: "venv not found"
```powershell
# Make sure you're in the right folder
cd skincare-nepal-ai
# Try again
python -m venv venv
```

### Problem: "Database connection refused"
```powershell
# PostgreSQL might not be running
# On Windows, open "Services" and start PostgreSQL
# Or restart your computer
```

### Problem: "Permission denied" on .env
```powershell
# Right-click .env file
# Properties > Security > Edit
# Give yourself Full Control
```

### Problem: "ModuleNotFoundError: No module named 'fastapi'"
```powershell
# Make sure virtual environment is activated
# You should see (venv) in your prompt
venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: "Port 8000 already in use"
```powershell
# Another app is using port 8000
# Try a different port:
uvicorn backend.main:app --reload --port 8001
```

---

## Next: Add Google Cloud Vision API

When ready, we'll add the AI image analysis feature.

Steps:
1. Create Google Cloud account
2. Create service account
3. Download credentials JSON
4. Add to `credentials/google-cloud-key.json`
5. Update `.env` with path

For now, the API has a "mock" mode that returns test results.

---

## File Locations to Remember

```
D:\Davinci Projects Files\CLAUDE\skincare-nepal-ai\
├── .env                          ← Your settings (created in Step 7)
├── requirements.txt              ← Dependencies list
├── backend/
│   ├── main.py                   ← Main API file
│   ├── models.py                 ← Database tables
│   ├── database.py               ← Database connection
│   ├── vision_api.py             ← AI analysis
│   └── khalti_payment.py         ← Payment processing
├── venv/                         ← Virtual environment (created in Step 4)
└── docs/                         ← Documentation
```

---

## 🎉 You're Done!

Your API is running! Next steps:

1. **Keep the server running** (leave PowerShell open)
2. **Test more endpoints** at http://localhost:8000/docs
3. **Make small changes** to understand how it works
4. **Ask questions** when stuck

---

## How to Stop the Server

In PowerShell:
```
Ctrl + C
```

---

## How to Start Again

```powershell
cd "D:\Davinci Projects Files\CLAUDE\skincare-nepal-ai"
venv\Scripts\activate
uvicorn backend.main:app --reload
```

---

**Questions? Stuck?** Let me know and I'll help you fix it! 🚀
