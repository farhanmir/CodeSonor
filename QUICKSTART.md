# Quick Start Guide for CodeSonor

This guide will help you get CodeSonor up and running in just a few minutes!

## Prerequisites Checklist

- [ ] Python 3.8 or higher installed
- [ ] pip package manager
- [ ] Google Gemini API key
- [ ] (Optional) GitHub Personal Access Token

## Setup Steps

### 1. Install Python Dependencies

Open PowerShell in the project directory and run:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file by copying the example:

```powershell
Copy-Item .env.example .env
```

Then open `.env` in a text editor and add your API keys:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
GITHUB_TOKEN=YOUR_GITHUB_TOKEN_HERE
```

### 3. Get Your Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

### 4. (Optional) Get Your GitHub Token

For higher API rate limits:

1. Visit: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name like "CodeSonor"
4. Select scopes: `public_repo` (at minimum)
5. Generate and copy the token
6. Paste it in your `.env` file

### 5. Run the Application

```powershell
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 6. Open in Browser

Navigate to: http://localhost:5000

## Testing the Application

Try analyzing a sample repository:

1. Paste this URL: `https://github.com/flask/flask`
2. Click "Analyze"
3. Wait for the results (should take 5-15 seconds)

## Troubleshooting

### Import Error: No module named 'flask'

**Solution:** Make sure you activated the virtual environment and installed dependencies:
```powershell
venv\Scripts\activate
pip install -r requirements.txt
```

### AI summary not available

**Solution:** Check that your `GEMINI_API_KEY` is correctly set in the `.env` file.

### Rate limit exceeded

**Solution:** Add a `GITHUB_TOKEN` to your `.env` file to increase the rate limit from 60 to 5000 requests per hour.

### Port 5000 already in use

**Solution:** The port might be in use by another application. Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Change to any available port
```

## Next Steps

- Customize the UI in `static/index.html` and `static/style.css`
- Modify language detection in `app.py`
- Add more AI analysis features
- Deploy to a cloud platform (Heroku, Railway, etc.)

## Getting Help

If you encounter issues:
1. Check the terminal/console for error messages
2. Review the troubleshooting section in README.md
3. Make sure all dependencies are installed
4. Verify your API keys are valid

Enjoy using CodeSonor! 🚀
