#!/bin/bash
# SkinCare Nepal AI - One-Command Deployment to Railway
# Usage: bash deploy.sh

set -e

echo "🚀 SkinCare Nepal AI - Railway Deployment Setup"
echo "================================================"

# Check prerequisites
echo "Checking prerequisites..."
command -v git >/dev/null 2>&1 || { echo "❌ Git is required"; exit 1; }

echo "✅ Git found"

# Initialize git if needed
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: SkinCare Nepal AI MVP"
fi

# Add GitHub remote
echo ""
echo "📝 Setting up GitHub remote..."
echo "Create a repo at: https://github.com/new"
read -p "Enter your GitHub username: " GITHUB_USER
read -p "Enter repository name (default: skincare-nepal-ai): " REPO_NAME
REPO_NAME=${REPO_NAME:-skincare-nepal-ai}

git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git" 2>/dev/null || git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "🚀 Next Steps:"
echo "1. Go to https://railway.app"
echo "2. Sign up with GitHub"
echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
echo "4. Select '$REPO_NAME'"
echo "5. Add environment variables:"
echo "   - DATABASE_URL=sqlite:///./skincare_nepal.db"
echo "   - SECRET_KEY=your-secret-key"
echo "   - KHALTI_PUBLIC_KEY=your_key"
echo "   - KHALTI_SECRET_KEY=your_secret"
echo ""
echo "6. Click Deploy!"
echo "7. Get your live URL from Railway dashboard"
echo ""
echo "📚 Documentation: docs/DEPLOYMENT.md"
