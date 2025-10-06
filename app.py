from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
from collections import defaultdict
import base64

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Configure Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

# Language extensions mapping
LANGUAGE_EXTENSIONS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.cpp': 'C++',
    '.c': 'C',
    '.cs': 'C#',
    '.go': 'Go',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.swift': 'Swift',
    '.kt': 'Kotlin',
    '.rs': 'Rust',
    '.html': 'HTML',
    '.css': 'CSS',
    '.jsx': 'React',
    '.tsx': 'TypeScript React',
    '.vue': 'Vue',
    '.sql': 'SQL',
    '.sh': 'Shell',
    '.json': 'JSON',
    '.xml': 'XML',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.md': 'Markdown',
}

def get_github_headers():
    """Get headers for GitHub API requests"""
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    return headers

def parse_github_url(url):
    """Parse GitHub URL to extract owner and repo name"""
    # Remove trailing slashes and .git
    url = url.rstrip('/').replace('.git', '')
    
    # Handle different GitHub URL formats
    if 'github.com' in url:
        parts = url.split('github.com/')[-1].split('/')
        if len(parts) >= 2:
            return parts[0], parts[1]
    
    return None, None

def fetch_repository_contents(owner, repo, path=''):
    """Fetch contents of a GitHub repository recursively"""
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    
    try:
        response = requests.get(url, headers=get_github_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repository contents: {e}")
        return None

def get_all_files(owner, repo, path='', files_list=None):
    """Recursively get all files in the repository"""
    if files_list is None:
        files_list = []
    
    contents = fetch_repository_contents(owner, repo, path)
    
    if contents is None:
        return files_list
    
    for item in contents:
        if item['type'] == 'file':
            files_list.append({
                'name': item['name'],
                'path': item['path'],
                'size': item['size'],
                'download_url': item.get('download_url')
            })
        elif item['type'] == 'dir':
            # Recursively fetch directory contents
            get_all_files(owner, repo, item['path'], files_list)
    
    return files_list

def calculate_language_stats(files):
    """Calculate language distribution based on file extensions"""
    language_sizes = defaultdict(int)
    total_size = 0
    
    for file in files:
        ext = os.path.splitext(file['name'])[1].lower()
        if ext in LANGUAGE_EXTENSIONS:
            language = LANGUAGE_EXTENSIONS[ext]
            size = file['size']
            language_sizes[language] += size
            total_size += size
    
    # Convert to percentages
    language_stats = {}
    for language, size in language_sizes.items():
        if total_size > 0:
            percentage = (size / total_size) * 100
            language_stats[language] = round(percentage, 2)
    
    # Sort by percentage
    language_stats = dict(sorted(language_stats.items(), key=lambda x: x[1], reverse=True))
    
    return language_stats

def get_file_content(download_url):
    """Fetch the content of a file from GitHub"""
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching file content: {e}")
        return None

def generate_ai_summary(code, filename):
    """Generate AI summary for code using Gemini API"""
    if not GEMINI_API_KEY:
        return "AI summary not available. Please configure GEMINI_API_KEY."
    
    try:
        prompt = f"""Analyze this code file named '{filename}' and provide:
1. A brief summary (2-3 sentences) of what this code does
2. The main purpose/functionality
3. Key components or classes (if any)

Code:
```
{code[:3000]}  # Limit to first 3000 chars to avoid token limits
```

Provide a concise, professional summary."""

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating AI summary: {e}")
        return f"Error generating summary: {str(e)}"

def analyze_key_files(files):
    """Analyze key source code files with AI"""
    # Priority extensions for analysis
    priority_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.go', '.rb']
    
    # Filter and prioritize files
    key_files = []
    for file in files:
        ext = os.path.splitext(file['name'])[1].lower()
        if ext in priority_extensions and file['size'] < 50000:  # Skip very large files
            # Prioritize main files, index files, app files
            name_lower = file['name'].lower()
            if any(keyword in name_lower for keyword in ['main', 'index', 'app', 'server']):
                key_files.insert(0, file)
            else:
                key_files.append(file)
    
    # Analyze up to 3 key files
    analyses = []
    for file in key_files[:3]:
        if file.get('download_url'):
            content = get_file_content(file['download_url'])
            if content:
                summary = generate_ai_summary(content, file['name'])
                analyses.append({
                    'file': file['path'],
                    'summary': summary
                })
    
    return analyses

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('static', 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze_repository():
    """Analyze a GitHub repository"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'GitHub URL is required'}), 400
    
    github_url = data['url']
    
    # Parse GitHub URL
    owner, repo = parse_github_url(github_url)
    
    if not owner or not repo:
        return jsonify({'error': 'Invalid GitHub URL format'}), 400
    
    try:
        # Fetch repository info
        repo_info_url = f'https://api.github.com/repos/{owner}/{repo}'
        repo_response = requests.get(repo_info_url, headers=get_github_headers())
        repo_response.raise_for_status()
        repo_info = repo_response.json()
        
        # Get all files
        files = get_all_files(owner, repo)
        
        if not files:
            return jsonify({'error': 'Could not fetch repository files'}), 404
        
        # Calculate language statistics
        language_stats = calculate_language_stats(files)
        
        # Analyze key files with AI
        ai_analyses = analyze_key_files(files)
        
        # Compile the analysis report
        analysis_report = {
            'repository': {
                'name': repo_info['name'],
                'owner': repo_info['owner']['login'],
                'description': repo_info.get('description', 'No description available'),
                'stars': repo_info['stargazers_count'],
                'forks': repo_info['forks_count'],
                'url': repo_info['html_url'],
                'created_at': repo_info['created_at'],
                'updated_at': repo_info['updated_at'],
            },
            'statistics': {
                'total_files': len(files),
                'language_distribution': language_stats,
            },
            'ai_analysis': ai_analyses,
            'file_list': [f['path'] for f in files[:50]]  # First 50 files
        }
        
        return jsonify(analysis_report), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'GitHub API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
