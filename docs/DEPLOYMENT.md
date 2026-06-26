# 🚀 Deployment Guide - Railway.app

Deploy your SkinCare Nepal AI backend to production in 5 minutes.

## Prerequisites

- GitHub account
- Railway.app account (free tier available)
- PostgreSQL (optional, SQLite works for MVP)
- Environment variables ready

## Step-by-Step Deployment

### Step 1: Push Code to GitHub

```bash
# Create GitHub repository
# https://github.com/new

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/skincare-nepal-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Grant permissions to access your repos

### Step 3: Create New Project on Railway

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Select `skincare-nepal-ai` repository
4. Railway auto-detects Python project ✅

### Step 4: Configure Environment Variables

In Railway dashboard, go to **Variables** tab:

```env
# Database
DATABASE_URL=sqlite:///./skincare_nepal.db

# Or use PostgreSQL (Railway can provision):
# DATABASE_URL=postgresql://username:password@hostname/dbname

# JWT
SECRET_KEY=your-super-secret-key-change-this

# Google Cloud Vision
GOOGLE_CLOUD_CREDENTIALS_PATH=./credentials/google-cloud-key.json

# Khalti Payments
KHALTI_PUBLIC_KEY=your_public_key
KHALTI_SECRET_KEY=your_secret_key

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=production
```

### Step 5: Deploy

1. Click "Deploy" button
2. Wait for build (2-3 minutes)
3. View logs in Railway dashboard
4. Get your live URL: `https://your-project-railway.app`

## Testing Production Deployment

```bash
# Test health endpoint
curl https://your-project-railway.app/health

# Test registration
curl -X POST https://your-project-railway.app/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","phone":"+977-9800000000","age":25,"gender":"male","password":"TestPass123"}'

# View API docs
https://your-project-railway.app/docs
```

## Production Checklist

- [ ] Environment variables configured
- [ ] Database URL set (PostgreSQL recommended)
- [ ] Google Cloud credentials uploaded
- [ ] Khalti keys configured
- [ ] HTTPS enabled (Railway auto-enables)
- [ ] Health endpoint returns 200
- [ ] User registration working
- [ ] Login generates JWT token
- [ ] Protected endpoints require auth

## Scaling (Future)

### Add PostgreSQL Database

1. In Railway, click "+ Add Service"
2. Select "PostgreSQL"
3. Auto-generates `DATABASE_URL`
4. Restart application

### Add Redis Cache (Optional)

For session caching and rate limiting:

```bash
# In Railway, add Redis service
# Set REDIS_URL in variables
```

### Add Monitoring

```bash
# Railway built-in monitoring:
# - View logs
# - Monitor CPU/Memory
- Track deployment history
```

## Common Issues

### Issue: Port already in use
**Solution:** Railway auto-assigns ports. Check environment variables.

### Issue: Database connection failed
**Solution:** 
- Verify DATABASE_URL is correct
- For PostgreSQL, ensure it's provisioned
- For SQLite, ensure file permissions

### Issue: Google Cloud Vision API key error
**Solution:**
- Verify credentials file path
- Check service account has Vision API enabled
- Re-download credentials JSON

## Environment-Specific Settings

### Development (localhost:8000)
```
ENVIRONMENT=development
API_HOST=0.0.0.0
API_PORT=8000
```

### Production (railway.app)
```
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=$PORT  # Railway sets this
```

## Monitoring & Logs

### View Real-Time Logs
Railway dashboard → Deployments → View Logs

### Common Log Patterns
```
INFO: Application startup complete  ✅
ERROR: Connection refused            ❌
WARNING: Could not connect to DB     ⚠️
```

## Rollback & Updates

### Deploy New Version
```bash
# Make changes locally
git add .
git commit -m "Update API"
git push origin main

# Railway auto-deploys on push
# Check deployment status in dashboard
```

### Rollback to Previous Version
Railway dashboard → Deployments → Click previous version → "Rollback"

## Cost Estimation (Monthly)

| Service | Cost | Notes |
|---------|------|-------|
| Railway App | $0-5 | Pay-as-you-go |
| PostgreSQL | $5-15 | If using Railway DB |
| Total | $5-20 | Very affordable |

## Next: Configure Custom Domain

```bash
# Add custom domain in Railway
# Point DNS records:
# A record: railway-ip
# CNAME: your-domain.com -> railway-project.app
```

## Support & Debugging

- Railway Docs: https://docs.railway.app
- Discord Community: https://railway.app/support
- Check logs for error details
- Test endpoints locally first

---

**Your app is now live! 🎉**

Share your deployment URL:
```
https://your-project-railway.app/docs
```
