# CodeSonor CLI - Quick Start Script
# This script builds and installs the CLI tool locally for testing

Write-Host "🚀 CodeSonor CLI Setup" -ForegroundColor Cyan
Write-Host "=====================`n" -ForegroundColor Cyan

# Step 1: Install build dependencies
Write-Host "📦 Installing build dependencies..." -ForegroundColor Yellow
pip install build twine pytest click rich requests google-generativeai python-dotenv

# Step 2: Install in development mode
Write-Host "`n📦 Installing CodeSonor in development mode..." -ForegroundColor Yellow
pip install -e .

# Step 3: Verify installation
Write-Host "`n✅ Verifying installation..." -ForegroundColor Green
codesonor --help

Write-Host "`n`n🎉 Setup complete!" -ForegroundColor Green
Write-Host "You can now use the 'codesonor' command anywhere!`n" -ForegroundColor Green

Write-Host "Example usage:" -ForegroundColor Cyan
Write-Host "  codesonor analyze https://github.com/pallets/flask" -ForegroundColor White
Write-Host "  codesonor summary https://github.com/python/cpython`n" -ForegroundColor White

Write-Host "⚠️  Don't forget to set your API keys:" -ForegroundColor Yellow
Write-Host "  `$env:GEMINI_API_KEY = 'your_key_here'" -ForegroundColor White
Write-Host "  `$env:GITHUB_TOKEN = 'your_token_here'`n" -ForegroundColor White
