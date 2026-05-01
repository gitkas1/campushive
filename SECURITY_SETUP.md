# 🔐 Security Setup - Protecting Your API Keys

## Overview
This guide explains how to safely manage your API keys and credentials so they're NEVER exposed on GitHub.

## ⚠️ What Should NEVER Be Committed to GitHub
- `serviceAccountKey.json` (Firebase credentials)
- `.env` (environment variables with real values)
- Any API keys, tokens, or secrets
- Private configuration files

## ✅ What IS Safe to Commit
- `.env.example` (template showing what variables are needed, with dummy values)
- `.gitignore` (tells Git what to ignore)
- Your application code
- Configuration files without actual secrets

---

## Setup Instructions

### 1. Already Protected
Your `.gitignore` has been created and includes:
```
.env                          # Your actual environment variables
*.json                        # Service account keys
serviceAccountKey.json        # Firebase credentials
```

### 2. Set Up Your Local Environment

**On your Windows machine**, create a `.env` file in your project root:

```
FLASK_ENV=development
SECRET_KEY=dev-key-change-in-production
FIREBASE_SERVICE_ACCOUNT_KEY=config/serviceAccountKey.json
```

#### Option A: Using a `.env` File (Recommended for Development)

1. In the root directory of your project, create `.env`:
```bash
# Windows PowerShell
New-Item -Item -Path .\.env -Force
```

2. Add your local values:
```
FLASK_ENV=development
SECRET_KEY=your-dev-secret-key
FIREBASE_SERVICE_ACCOUNT_KEY=config/serviceAccountKey.json
```

3. Place your `serviceAccountKey.json` in `backend/config/`

Your code already loads this automatically with `load_dotenv()` in `run.py`

#### Option B: Using Environment Variables (Recommended for Production/Deployment Platforms)

When deploying to platforms like **Heroku**, **Replit**, **Railway**, or **AWS**, set environment variables directly in their web dashboards instead of using a `.env` file:

**Heroku Example:**
```
Settings → Config Vars
FIREBASE_SERVICE_ACCOUNT_KEY = (paste entire JSON content)
SECRET_KEY = your-production-secret-key
```

---

## 3. Deploy to Production Safely

### If using Heroku/Railway/AWS/etc:
1. DO NOT include `.env` file
2. Add environment variables through their dashboard
3. Your app will read from the platform's environment automatically

### If using a VPS or Traditional Host:
1. Copy `.env.example` and rename to `.env`
2. Fill in real values on the server only
3. Ensure `.env` is in `.gitignore`

---

## 4. Verify It's Working

Your code already handles this! Check these files:

#### `backend/run.py` - ✅ Already loads .env
```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env file automatically
```

#### `backend/config/firebase_config.py` - ✅ Already uses environment variables
```python
SERVICE_ACCOUNT_KEY_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY', 'config/serviceAccountKey.json')
```

#### `backend/config/settings.py` - ✅ Already uses environment variables
```python
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
```

---

## 5. Before Pushing to GitHub

**CRITICAL CHECKLIST:**
- [ ] `.gitignore` exists (created)
- [ ] `.env` file is listed in `.gitignore` ✅
- [ ] You have a `.env` file locally (not committed)
- [ ] `.env.example` shows what variables are needed (created)
- [ ] Your `serviceAccountKey.json` is NOT in the repo
- [ ] Run `git status` to verify these files aren't staged

**Quick check:**
```bash
git status
```
You should NOT see:
- `.env`
- `serviceAccountKey.json`
- `*.json` (unless intentional)

---

## 6. If You Accidentally Committed Secrets

If you already pushed sensitive files to GitHub:

1. **Immediately rotate your Firebase credentials** in Firebase Console
2. Download a new `serviceAccountKey.json`
3. Use `git filter-branch` or `BFG Repo-Cleaner` to remove from history:
```bash
git filter-branch --tree-filter 'rm -f *.json' HEAD
git push origin --force
```
4. Update your GitHub repository settings if available

---

## Summary
✅ **Your setup is protected because:**
1. `.gitignore` prevents credentials from being committed
2. `python-dotenv` loads secrets from `.env` (local only)
3. Code uses `os.getenv()` to read from environment
4. `.env.example` documents what's needed without exposing secrets

🎯 **When deploying:**
- Local development: Use `.env` file (never commit it)
- Production: Set env vars in your hosting platform's dashboard

---

## Need Help?
- Check the `.env.example` file to see all required variables
- Make sure `.env` is in your `.gitignore`
- Never commit files in `.gitignore`
