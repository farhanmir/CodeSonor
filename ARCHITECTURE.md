# CodeSonor Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                            USER BROWSER                              │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │              Frontend (static/index.html)                   │   │
│  │                                                              │   │
│  │  1. User enters GitHub URL                                  │   │
│  │  2. Click "Analyze" button                                  │   │
│  │  3. JavaScript sends POST request                           │   │
│  │  4. Show loading animation                                  │   │
│  │  5. Receive and display results                             │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              ↓ ↑                                    │
│                         HTTP/JSON                                   │
│                              ↓ ↑                                    │
└─────────────────────────────┼─┼────────────────────────────────────┘
                               ↓ ↑
┌─────────────────────────────┼─┼────────────────────────────────────┐
│                         FLASK SERVER                                │
│                            (app.py)                                 │
│                              ↓ ↑                                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │         POST /analyze Endpoint                              │   │
│  │                                                              │   │
│  │  1. Parse GitHub URL                                        │   │
│  │  2. Validate input                                          │   │
│  │  3. Call GitHub API                                         │   │
│  │  4. Calculate language stats                                │   │
│  │  5. Call Gemini AI                                          │   │
│  │  6. Format response                                         │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              ↓ ↑                                    │
└─────────────────────────────┼─┼────────────────────────────────────┘
                               ↓ ↑
         ┌─────────────────────┴─┴────────────────────┐
         ↓                                             ↑
    ┌────────┐                                   ┌─────────┐
    │ GitHub │                                   │ Gemini  │
    │  API   │                                   │   AI    │
    └────────┘                                   └─────────┘
         ↓                                             ↑
    Returns:                                      Returns:
    - Repo info                                   - Code summaries
    - File list                                   - Documentation
    - Metadata
```

## Component Breakdown

### 1. Frontend (Browser)
```
index.html
├── Header & Navigation
├── Input Section
│   └── GitHub URL input + Analyze button
├── Loading Section (hidden by default)
├── Error Section (hidden by default)
└── Results Section (hidden by default)
    ├── Repository Info Card
    ├── Statistics & Language Distribution
    ├── AI Analysis Cards
    └── File List

style.css
├── Layout styles
├── Component styling
├── Responsive design
└── Language-specific colors

script.js
├── analyzeRepository() - Main function
├── displayResults() - Render data
├── API communication (fetch)
└── UI state management
```

### 2. Backend (Flask Server)
```
app.py
├── Flask app setup
├── Route: / (serve frontend)
├── Route: /analyze (POST)
│   ├── parse_github_url()
│   ├── fetch_repository_contents()
│   ├── get_all_files()
│   ├── calculate_language_stats()
│   └── analyze_key_files()
│       └── generate_ai_summary()
└── Helper functions
```

### 3. External APIs
```
GitHub API (api.github.com)
├── GET /repos/{owner}/{repo}
├── GET /repos/{owner}/{repo}/contents/{path}
└── Rate limiting: 60/hr (unauth) or 5000/hr (with token)

Gemini API (Google AI)
├── generate_content() - Code analysis
└── Model: gemini-pro
```

## Data Flow

### Request Flow
```
1. User Input
   └─> "https://github.com/owner/repo"

2. Frontend Processing
   └─> Validate URL
       └─> Send POST to /analyze

3. Backend Processing
   └─> Parse URL (owner, repo)
       └─> Fetch repo info from GitHub
           └─> Recursively get all files
               └─> Calculate language distribution
                   └─> Analyze key files with AI
                       └─> Compile JSON report

4. Response Processing
   └─> Receive JSON
       └─> Update DOM elements
           └─> Display results
```

### Data Structures

**Request (Frontend → Backend):**
```json
{
  "url": "https://github.com/owner/repo"
}
```

**Response (Backend → Frontend):**
```json
{
  "repository": {
    "name": "string",
    "owner": "string",
    "description": "string",
    "stars": number,
    "forks": number,
    "url": "string",
    "created_at": "ISO date",
    "updated_at": "ISO date"
  },
  "statistics": {
    "total_files": number,
    "language_distribution": {
      "Language": percentage
    }
  },
  "ai_analysis": [
    {
      "file": "path/to/file",
      "summary": "AI-generated summary"
    }
  ],
  "file_list": ["file1", "file2", ...]
}
```

## File Analysis Logic

```
get_all_files()
    ├── Fetch /contents/ from GitHub
    ├── For each item:
    │   ├── If file → Add to list
    │   └── If directory → Recurse
    └── Return complete file list

calculate_language_stats()
    ├── For each file:
    │   ├── Get extension
    │   ├── Map to language
    │   └── Add size to language total
    ├── Calculate percentages
    └── Sort by percentage (descending)

analyze_key_files()
    ├── Filter files by:
    │   ├── Extension (priority languages)
    │   └── Size (< 50KB)
    ├── Prioritize by name:
    │   └── main, index, app, server
    ├── Take top 3 files
    ├── For each file:
    │   ├── Download content
    │   ├── Send to Gemini API
    │   └── Get summary
    └── Return analyses
```

## Error Handling

```
Frontend
├── Invalid URL format → Show error alert
├── Empty input → Show error alert
├── Network error → Show error alert
└── API error → Display error message

Backend
├── Invalid GitHub URL → 400 Bad Request
├── Repository not found → 404 Not Found
├── GitHub API error → 500 Server Error
├── AI API error → Continue with partial results
└── Rate limiting → 429 Too Many Requests
```

## Environment Configuration

```
Development (.env)
├── GEMINI_API_KEY=xxx
└── GITHUB_TOKEN=xxx (optional)

Production
├── Same variables
├── Debug mode: OFF
└── HTTPS enabled
```

## Performance Optimization

```
Strategies:
├── Lazy loading (analyze on demand)
├── File size limits (skip large files)
├── Analysis limits (top 3 files only)
├── GitHub token (higher rate limits)
├── Error recovery (continue on failure)
└── Response truncation (first 50 files shown)
```

## Security Measures

```
├── Environment variables (no hardcoded secrets)
├── Input validation (URL parsing)
├── CORS configuration (controlled access)
├── No credential storage
├── Error message sanitization
└── .gitignore (exclude .env)
```

## Deployment Architecture

```
Production Setup:
├── Web Server (Gunicorn)
├── Platform (Render/Railway/Heroku)
├── Environment Variables (secure storage)
├── HTTPS/SSL (automatic)
├── CDN for static files (optional)
└── Monitoring (logs, errors)
```

## Technology Stack Summary

```
Languages:
├── Python 3.8+ (Backend)
├── JavaScript ES6+ (Frontend)
├── HTML5 (Structure)
└── CSS3 (Styling)

Frameworks:
├── Flask 3.0 (Web framework)
├── Bootstrap 5.3 (UI framework)

Libraries:
├── requests (HTTP client)
├── google-generativeai (AI)
├── flask-cors (CORS)
└── python-dotenv (Config)

APIs:
├── GitHub REST API v3
└── Google Gemini API

Tools:
├── pip (Package manager)
├── venv (Virtual environment)
└── Git (Version control)
```

---

This architecture provides:
✅ Separation of concerns (frontend/backend)
✅ Scalable design (easy to add features)
✅ Error resilience (graceful degradation)
✅ Security best practices
✅ Production-ready deployment
