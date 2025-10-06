# First Run Checklist for CodeSonor

Follow this checklist to get CodeSonor running for the first time!

## ✅ Pre-Installation Checklist

- [ ] Python 3.8 or higher installed
  - Check: Open PowerShell and type `python --version`
  - If not installed: Download from https://www.python.org/downloads/

- [ ] pip is available
  - Check: Type `pip --version` in PowerShell
  - Usually comes with Python

- [ ] You have a Google Gemini API key
  - Get one: https://makersuite.google.com/app/apikey
  - Sign in with Google account → Create API Key

## 📋 Installation Steps

### Step 1: Open PowerShell in Project Directory
```powershell
cd "c:\Users\Farhan Mir\Desktop\Projects\CodeSonor"
```

### Step 2: Create Virtual Environment
```powershell
python -m venv venv
```
**Expected result:** A new `venv` folder appears

### Step 3: Activate Virtual Environment
```powershell
venv\Scripts\activate
```
**Expected result:** Your prompt shows `(venv)` at the beginning

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```
**Expected result:** 
```
Successfully installed Flask-3.0.0 Flask-CORS-4.0.0 ...
```
This takes about 1-2 minutes.

### Step 5: Create Environment File
```powershell
Copy-Item .env.example .env
```
**Expected result:** A new `.env` file appears

### Step 6: Add Your API Key
1. Open `.env` file in a text editor (Notepad, VS Code, etc.)
2. Replace `your_gemini_api_key_here` with your actual API key
3. Save the file

Example:
```env
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN=  # Optional, leave empty for now
```

### Step 7: Start the Server
```powershell
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Step 8: Open in Browser
1. Open your web browser
2. Go to: `http://localhost:5000`
3. You should see the CodeSonor interface!

## 🧪 Test Run

### First Analysis Test:
1. In the input box, paste: `https://github.com/pallets/flask`
2. Click "Analyze"
3. Wait 5-15 seconds
4. You should see:
   - Repository information
   - Language distribution
   - AI-generated summaries
   - File list

**If it works:** ✅ Success! You're all set!

**If it doesn't work:** See troubleshooting below ⬇️

## 🔧 Troubleshooting

### Error: "python is not recognized"
**Problem:** Python not in PATH
**Solution:** 
1. Reinstall Python
2. Check "Add Python to PATH" during installation
3. Or use full path: `C:\Python3X\python.exe`

### Error: "No module named 'flask'"
**Problem:** Virtual environment not activated or packages not installed
**Solution:**
```powershell
venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "AI summary not available"
**Problem:** Gemini API key not set or invalid
**Solution:**
1. Open `.env` file
2. Check API key is correct (no quotes, no spaces)
3. Verify key works at https://makersuite.google.com/

### Error: "Could not fetch repository files"
**Problem:** GitHub API rate limit or network issue
**Solution:**
1. Check internet connection
2. Try a different repository
3. Add GitHub token to `.env` file:
   ```env
   GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
   ```

### Error: "Address already in use"
**Problem:** Port 5000 is taken by another application
**Solution:**
1. Close other applications using port 5000
2. Or change port in `app.py`:
   ```python
   app.run(debug=True, port=5001)
   ```
   Then visit `http://localhost:5001`

### Browser shows "Cannot connect"
**Problem:** Server not running or wrong URL
**Solution:**
1. Check terminal shows "Running on http://127.0.0.1:5000"
2. Use exact URL: `http://localhost:5000` or `http://127.0.0.1:5000`
3. Make sure server is still running (check terminal)

### Analysis takes forever
**Problem:** Large repository or slow API response
**Solution:**
1. This is normal for large repos (can take up to 30 seconds)
2. Try a smaller repository first
3. Check terminal for error messages

## 📝 Quick Reference

### Start the Server (After First Setup)
```powershell
cd "c:\Users\Farhan Mir\Desktop\Projects\CodeSonor"
venv\Scripts\activate
python app.py
```

### Or Use the Batch File
```powershell
.\start.bat
```

### Stop the Server
Press `Ctrl + C` in the PowerShell window

### Deactivate Virtual Environment
```powershell
deactivate
```

## 🎯 Next Steps After Success

1. ✅ **Bookmark the app** - `http://localhost:5000`
2. 📚 **Read README.md** - Learn all features
3. 🎨 **Customize** - Edit colors, add features
4. 🚀 **Deploy** - See DEPLOYMENT.md for hosting
5. 🐙 **Share** - Push to GitHub, share with friends

## 💡 Pro Tips

- **Use GitHub Token:** Add to `.env` for 5000 requests/hour instead of 60
- **Test Small First:** Start with small repos (< 100 files)
- **Check Logs:** Terminal shows helpful debug information
- **Multiple Tabs:** You can analyze multiple repos in different tabs
- **Save Analysis:** Copy results before analyzing another repo

## 📞 Need Help?

1. Check the error message in the browser
2. Look at terminal output for detailed errors
3. Review QUICKSTART.md for common issues
4. Check README.md troubleshooting section
5. Verify all steps in this checklist

## ✨ Congratulations!

If you've completed all steps successfully, CodeSonor is now running!

Try analyzing some interesting repositories:
- `https://github.com/django/django`
- `https://github.com/nodejs/node`
- `https://github.com/facebook/react`
- `https://github.com/microsoft/vscode`

**Happy analyzing! 🎉**

---

Last updated: October 6, 2025
