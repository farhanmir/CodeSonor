# Deployment Guide for CodeSonor

This guide covers how to deploy CodeSonor to various cloud platforms.

## Option 1: Deploy to Render (Recommended - Free Tier Available)

### Prerequisites
- GitHub account
- Render account (free at https://render.com)

### Steps

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Create a `render.yaml` file** (already included if you use the one below)

3. **Connect to Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: `codesonor`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   
4. **Add Environment Variables**
   - Add `GEMINI_API_KEY` with your key
   - Add `GITHUB_TOKEN` (optional)

5. **Deploy** - Render will automatically build and deploy

### Additional file needed for Render:

Create `gunicorn_config.py`:
```python
bind = "0.0.0.0:10000"
workers = 2
threads = 4
timeout = 120
```

Add to `requirements.txt`:
```
gunicorn==21.2.0
```

## Option 2: Deploy to Railway

### Prerequisites
- GitHub account
- Railway account (https://railway.app)

### Steps

1. **Push code to GitHub** (if not already done)

2. **Deploy on Railway**
   - Visit https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your CodeSonor repository
   - Railway auto-detects Python and installs dependencies

3. **Configure Environment Variables**
   - In Railway dashboard, go to Variables
   - Add `GEMINI_API_KEY`
   - Add `GITHUB_TOKEN` (optional)

4. **Set Start Command** (if not auto-detected)
   - Add Procfile or set in Railway settings:
   - `gunicorn app:app`

5. **Generate Domain**
   - Railway provides a free domain automatically
   - Or add your custom domain

## Option 3: Deploy to Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Create required files**

   Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

   Add to `requirements.txt`:
   ```
   gunicorn==21.2.0
   ```

2. **Create Heroku app**
   ```bash
   heroku login
   heroku create codesonor-app
   ```

3. **Set environment variables**
   ```bash
   heroku config:set GEMINI_API_KEY=your_key_here
   heroku config:set GITHUB_TOKEN=your_token_here
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open app**
   ```bash
   heroku open
   ```

## Option 4: Deploy to PythonAnywhere

### Steps

1. **Create PythonAnywhere account** (free tier available)

2. **Upload your code**
   - Use Git clone or upload files manually

3. **Create a virtual environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 codesonor
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to Web tab → Add a new web app
   - Choose Flask
   - Point to your `app.py`

5. **Set environment variables**
   - In PythonAnywhere dashboard, add variables in WSGI configuration

6. **Reload** the web app

## Option 5: Deploy with Docker

### Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

### Create `.dockerignore`:

```
venv/
__pycache__/
*.pyc
.env
.git/
```

### Build and run:

```bash
docker build -t codesonor .
docker run -p 5000:5000 --env-file .env codesonor
```

## Important Notes for Production

### 1. Update Flask Configuration

In `app.py`, change:
```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')  # Set debug=False for production
```

### 2. Update Frontend API URL

In `static/script.js`, update the API URL:
```javascript
// For production, use relative URL or your deployed backend URL
const API_URL = window.location.origin;  // Uses current domain
```

### 3. Security Considerations

- Never commit `.env` file to Git
- Use environment variables for all secrets
- Enable HTTPS on your domain
- Consider rate limiting for the API
- Add input validation and sanitization

### 4. Performance Optimization

- Enable caching for static files
- Use a CDN for Bootstrap/icons
- Consider Redis for caching GitHub API responses
- Implement request queuing for AI analysis

### 5. Monitoring

- Set up error logging (e.g., Sentry)
- Monitor API usage and costs
- Track response times
- Set up uptime monitoring

## Environment Variables Checklist

For any deployment platform, ensure these are set:

- ✅ `GEMINI_API_KEY` (required)
- ✅ `GITHUB_TOKEN` (optional but recommended)
- ✅ `FLASK_ENV=production` (for production deployments)

## Testing Your Deployment

After deploying:

1. Visit your deployed URL
2. Try analyzing a public repository
3. Check error logs if issues occur
4. Monitor API usage and quotas

## Troubleshooting Deployment Issues

### Build Fails
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Check build logs for specific errors

### App Crashes
- Check application logs
- Verify environment variables are set
- Ensure gunicorn is in requirements.txt

### API Not Working
- Check CORS settings in app.py
- Verify API endpoints are accessible
- Check network/firewall settings

---

Need help? Check the platform-specific documentation or raise an issue on GitHub!
