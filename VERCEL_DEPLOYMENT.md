# Vercel Deployment Guide for NextWish

## Important Limitations

⚠️ **Vercel Serverless Functions have limitations:**

1. **File Upload Size**: Maximum 4.5MB per request
2. **No Persistent Storage**: Files cannot be saved permanently
3. **Read-Only Filesystem**: Cannot write to `/generated` or `/uploads`
4. **Function Timeout**: 10 seconds (hobby), 60 seconds (pro)

## Recommended Solutions

### Option 1: Use Vercel with External Storage (Recommended)

You'll need to modify the app to use cloud storage:

**Storage Options:**
- **AWS S3** - Most popular, good pricing
- **Cloudinary** - Image-specific, easy to use
- **Google Cloud Storage** - Good integration
- **Azure Blob Storage** - Microsoft cloud

**Required Changes:**
1. Upload files to cloud storage instead of local disk
2. Store greeting URLs pointing to cloud-hosted files
3. Generate greetings on-the-fly or store templates in cloud

### Option 2: Deploy to Different Platform

Better platforms for file-heavy applications:

**Railway.app** (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Render.com**
```bash
# Connect GitHub repo
# Auto-deploys on push
# Free tier available
```

**Heroku**
```bash
heroku create nextwish-birthday
git push heroku main
```

**DigitalOcean App Platform**
- Connect GitHub
- Auto-deploy
- Good for Flask apps

## Current Vercel Setup

Files created for Vercel (but won't work fully with file uploads):

### 1. `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "static/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ]
}
```

### 2. `api/index.py`
Entry point for Vercel that imports your Flask app.

### 3. `requirements.txt`
Python dependencies for Vercel to install.

## Recommended: Deploy to Railway

Railway is perfect for this app because:
- ✅ Supports file uploads
- ✅ Persistent storage
- ✅ Easy Flask deployment
- ✅ Free tier available
- ✅ GitHub integration

### Railway Deployment Steps:

1. **Install Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Login:**
```bash
railway login
```

3. **Initialize project:**
```bash
cd NextWish_Backend
railway init
```

4. **Add environment variables:**
```bash
railway variables set FLASK_ENV=production
```

5. **Deploy:**
```bash
railway up
```

6. **Get URL:**
```bash
railway domain
```

### Railway Configuration

Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `Procfile`:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

Update `requirements.txt`:
```
Flask==3.0.0
Flask-CORS==4.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

## Alternative: Modify App for Vercel

If you must use Vercel, you need to:

### 1. Use Temporary Storage
```python
import tempfile
import os

# In app.py
TEMP_DIR = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = os.path.join(TEMP_DIR, 'uploads')
app.config['GENERATED_FOLDER'] = os.path.join(TEMP_DIR, 'generated')
```

### 2. Use Cloud Storage (AWS S3 Example)
```python
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET_KEY']
)

def upload_to_s3(file_data, filename, bucket='nextwish-greetings'):
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=filename,
            Body=file_data,
            ContentType='text/html'
        )
        return f"https://{bucket}.s3.amazonaws.com/{filename}"
    except ClientError as e:
        print(e)
        return None
```

### 3. Update Generate Function
```python
# Instead of saving to disk, upload to S3
html_url = upload_to_s3(html_content, f"{greeting_id}/index.html")
```

## Deployment Comparison

| Platform | File Upload | Storage | Complexity | Cost |
|----------|------------|---------|------------|------|
| **Railway** | ✅ Full | Persistent | Low | Free tier |
| **Render** | ✅ Full | Persistent | Low | Free tier |
| **Heroku** | ✅ Full | Ephemeral* | Low | Paid |
| **Vercel** | ⚠️ Limited | None | High** | Free tier |
| **DigitalOcean** | ✅ Full | Persistent | Medium | $5/mo |

*Ephemeral: Files deleted on restart
**High complexity due to need for external storage

## Quick Fix for Your Current Error

The 500 error is because:
1. Vercel can't create `/generated` or `/uploads` directories
2. File operations fail in serverless environment

**Immediate Solution:** Deploy to Railway instead

```bash
# Quick Railway deploy
npm i -g @railway/cli
railway login
railway init
railway up
```

Your app will work perfectly on Railway without any code changes!

## Summary

❌ **Don't use Vercel for this app** - File uploads don't work in serverless
✅ **Use Railway.app** - Perfect for Flask apps with file handling
✅ **Use Render.com** - Another great alternative
✅ **Use traditional VPS** - DigitalOcean, Linode, etc.

The current architecture requires a traditional server environment, not serverless.
