# CodeSonor 🔍

**CodeSonor** is an AI-powered web application that analyzes public GitHub repositories to provide instant insights into code structure, language distribution, and code quality.

## Features ✨

- 📊 **Language Distribution Analysis** - Visual breakdown of programming languages used in the repository
- 🤖 **AI-Powered Code Summaries** - Automatic documentation generation using Google's Gemini API
- 📈 **Repository Statistics** - File counts, stars, forks, and timeline information
- 🎨 **Beautiful UI** - Clean, responsive Bootstrap interface
- ⚡ **Fast Analysis** - Quick insights without reading every line of code
- 🔒 **Public Repos Only** - Analyzes any public GitHub repository

## Tech Stack 🛠️

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Requests** - HTTP library for GitHub API
- **Google Generative AI** - Gemini API for code analysis
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5 & CSS3**
- **Bootstrap 5** - Responsive UI framework
- **JavaScript (ES6+)** - Client-side logic
- **Bootstrap Icons** - Icon library

## Installation & Setup 🚀

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- A Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- A GitHub Personal Access Token ([Get one here](https://github.com/settings/tokens)) - **Required for API access**

### Step 1: Clone or Download the Repository
```bash
cd CodeSonor
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
1. Copy the example environment file:
   ```bash
   # Windows PowerShell
   Copy-Item .env.example .env

   # macOS/Linux
   cp .env.example .env
   ```

2. Edit the `.env` file and add your API keys:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   GITHUB_TOKEN=your_actual_github_token_here
   ```

   **Getting API Keys:**
   - **Gemini API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **GitHub Token**: Visit [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
     - Create a token with `public_repo` scope

### Step 5: Run the Application
```bash
python app.py
```

The server will start at `http://localhost:5000`

### Step 6: Open in Browser
Navigate to `http://localhost:5000` in your web browser.

## Usage 📖

1. **Enter Repository URL**: Paste any public GitHub repository URL into the input field
   - Example: `https://github.com/facebook/react`
   - Example: `https://github.com/microsoft/vscode`

2. **Click Analyze**: The application will:
   - Fetch repository information from GitHub API
   - Calculate language distribution
   - Analyze key source files with AI
   - Display comprehensive results

3. **View Results**: The report includes:
   - Repository metadata (name, description, stars, forks)
   - Total file count and creation/update dates
   - Language distribution with visual progress bars
   - AI-generated summaries of key code files
   - File structure overview

## Project Structure 📁

```
CodeSonor/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your actual environment variables (git-ignored)
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── static/               # Frontend files
    ├── index.html        # Main HTML page
    ├── style.css         # Custom styles
    └── script.js         # JavaScript logic
```

## API Endpoints 🔌

### `POST /analyze`
Analyzes a GitHub repository.

**Request Body:**
```json
{
  "url": "https://github.com/owner/repo"
}
```

**Response:**
```json
{
  "repository": {
    "name": "repo-name",
    "owner": "owner-name",
    "description": "Repository description",
    "stars": 1234,
    "forks": 567,
    "url": "https://github.com/owner/repo",
    "created_at": "2020-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "statistics": {
    "total_files": 150,
    "language_distribution": {
      "Python": 60.5,
      "JavaScript": 30.2,
      "HTML": 9.3
    }
  },
  "ai_analysis": [
    {
      "file": "src/main.py",
      "summary": "AI-generated summary..."
    }
  ],
  "file_list": ["file1.py", "file2.js", ...]
}
```

## Configuration ⚙️

### Language Extensions
The application recognizes the following file extensions:
- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- C/C++ (.c, .cpp)
- C# (.cs)
- Go (.go)
- Ruby (.rb)
- PHP (.php)
- Swift (.swift)
- Kotlin (.kt)
- Rust (.rs)
- And more...

### AI Analysis
- Analyzes up to 3 key source files per repository
- Prioritizes main, index, app, and server files
- Skips files larger than 50KB to avoid token limits
- Uses first 3000 characters of each file for analysis

## Troubleshooting 🔧

### "Error fetching repository files"
- Ensure the repository URL is correct and public
- Check your internet connection
- Verify GitHub API is accessible

### "AI summary not available"
- Make sure `GEMINI_API_KEY` is set in `.env` file
- Verify your API key is valid and active
- Check if you've exceeded API quota

### Rate Limiting
- GitHub API has rate limits (60 requests/hour without token)
- Add a `GITHUB_TOKEN` to your `.env` file for higher limits (5000 requests/hour)

## Future Enhancements 🚀

- [ ] Support for private repositories (with OAuth)
- [ ] Code quality metrics and linting analysis
- [ ] Dependency vulnerability scanning
- [ ] Historical trend analysis
- [ ] PDF report generation
- [ ] Comparison between multiple repositories
- [ ] Docker containerization

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments 🙏

- GitHub API for repository data
- Google Gemini for AI-powered analysis
- Bootstrap for beautiful UI components
- Flask for the backend framework

---

**Developed by Farhan Mir**