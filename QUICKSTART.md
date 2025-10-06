# Quick Start Guide

## Get CodeSonor Running in 5 Minutes

### 1. Install Dependencies
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get Your API Keys

**Gemini API Key:**
- Visit: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy the key

**GitHub Token (Required):**
- Visit: https://github.com/settings/tokens
- Click "Generate new token" → "Generate new token (classic)"
- Name it: `CodeSonor`
- Select scope: **public_repo**
- Generate and copy the token

### 3. Configure Environment
```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your keys:
```env
GEMINI_API_KEY=your_actual_key_here
GITHUB_TOKEN=your_actual_token_here
```

### 4. Run
```powershell
python app.py
```

Open browser: http://localhost:5000

### 5. Test
Try analyzing: `https://github.com/pallets/flask`

---

## Troubleshooting

**"Import 'flask' could not be resolved"**
- Activate venv: `venv\Scripts\activate`
- Install: `pip install -r requirements.txt`

**"GitHub authentication required"**
- Add GitHub token to `.env` file
- Token must have `public_repo` scope

**Analysis taking too long**
- Large repos (like VS Code) can take 30-60 seconds
- Try smaller repos first
- Check terminal for progress

---

That's it! See README.md for full documentation.
