from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import os
import shutil
import tempfile
import git
from dotenv import load_dotenv
from pathlib import Path

# Import Codesonor modules
from src.codesonor.ai_analyzer import AIAnalyzer
from src.codesonor.team_dna import TeamDNA
from src.codesonor.dep_risk import DependencyRisk
from src.codesonor.archaeology import CodeArchaeology
from src.codesonor.smart_smell import SmartSmellDetector
from src.codesonor.language_stats import LanguageStats

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

class RepoCloner:
    """Context manager for cloning and cleaning up repositories."""
    def __init__(self, url):
        self.url = url
        self.temp_dir = tempfile.mkdtemp()
        self.repo_dir = None

    def __enter__(self):
        try:
            print(f"Cloning {self.url} to {self.temp_dir}...")
            # Modify URL to include token if available to avoid rate limits/auth issues
            auth_url = self.url
            if GITHUB_TOKEN and 'github.com' in self.url and '@' not in self.url:
               auth_url = self.url.replace('https://', f'https://{GITHUB_TOKEN}@')
            
            git.Repo.clone_from(auth_url, self.temp_dir, depth=500) # Depth 500 for archaeology
            self.repo_dir = Path(self.temp_dir)
            return self.repo_dir
        except Exception as e:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Cleaning up {self.temp_dir}...")
        # On Windows, git processes might hold file locks, so we might need retry logic or ignore errors
        try:
             # Forcefully remove read-only files if necessary (common git issue on windows)
            def on_rm_error(func, path, exc_info):
                os.chmod(path, 0o777)
                func(path)
                
            shutil.rmtree(self.temp_dir, onerror=on_rm_error)
        except Exception as e:
            print(f"Error cleaning up: {e}")

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/analyze', methods=['POST'])
def analyze_repository():
    data = request.get_json()
    github_url = data.get('url')
    
    if not github_url:
        return jsonify({'error': 'GitHub URL is required'}), 400

    try:
        # Clone and Analyze
        with RepoCloner(github_url) as repo_path:
            results = {}
            
            # 1. Base Statistics & Language
            lang_stats = LanguageStats(repo_path).get_stats()
            results['statistics'] = {
                'languages': lang_stats,
                'total_files': sum(l['count'] for l in lang_stats.values()) if isinstance(lang_stats, dict) else 0 
                # Note: LanguageStats implementation might return dict or list, assuming dict based on prev usage
            }

            # 2. AI Analysis (Summaries)
            # We recreate the AI Analyzer here
            ai_analyzer = AIAnalyzer(api_key=GEMINI_API_KEY, provider='gemini')
            if ai_analyzer.is_available():
                # Get key files manualy or reuse logic? 
                # For simplicity, we'll list files and pick top 3 like before
                files = []
                for root, _, filenames in os.walk(repo_path):
                    if '.git' in root: continue
                    for f in filenames:
                        files.append({'name': f, 'path': str(Path(root) / f), 'size': os.path.getsize(Path(root) / f)})
                
                # Simple heuristic for key files
                key_files = sorted(
                    [f for f in files if f['path'].endswith(('.py', '.js', '.ts', '.java', '.go'))],
                    key=lambda x: x['size']
                )[:3]
                
                summaries = []
                for f in key_files:
                    try:
                        with open(f['path'], 'r', encoding='utf-8', errors='ignore') as file_obj:
                            content = file_obj.read()
                            summary = ai_analyzer.generate_summary(content, f['name'])
                            summaries.append({'file': f['name'], 'summary': summary})
                    except: pass
                results['ai_analysis'] = summaries
            
            # 3. Team DNA
            team_dna = TeamDNA(repo_path)
            results['team_dna'] = team_dna.analyze_contributors(limit=100)

            # 4. Dependency Risk
            dep_risk = DependencyRisk(repo_path)
            results['dependency_risk'] = dep_risk.analyze_dependencies()

            # 5. Archaeology (History)
            pass # Skipping for speed in this iteration unless requested, or add basic stats
            archaeology = CodeArchaeology(repo_path)
            results['archaeology'] = archaeology.analyze_evolution(weeks=12)

            return jsonify(results), 200

    except Exception as e:
        print(f"Analysis failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/export/markdown', methods=['POST'])
def export_markdown():
    """Export analysis results to Markdown."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    # Generate Markdown Report
    md = f"# CodeSonor Analysis Report\n\n"
    md += f"**Repository:** {data.get('repository', {}).get('name', 'Unknown')}\n"
    md += f"**Date:** {data.get('repository', {}).get('updated_at', '')}\n\n"
    
    md += "## 📊 Statistics\n"
    md += f"- **Total Files:** {data.get('statistics', {}).get('total_files', 0)}\n"
    md += "- **Languages:**\n"
    for lang, stats in data.get('statistics', {}).get('languages', {}).items():
        # Handle simple dict or complex object
        val = stats if isinstance(stats, (int, float, str)) else stats.get('percentage', 0)
        md += f"  - {lang}: {val}%\n"
        
    md += "\n## 🧬 Team DNA\n"
    contributors = data.get('team_dna', {}).get('contributors', {})
    for name, profile in contributors.items():
        md += f"- **{name}**: {profile.get('total_commits', 0)} commits\n"
        
    md += "\n## 🛡️ Dependency Risk\n"
    risk = data.get('dependency_risk', {})
    md += f"- **Score:** {risk.get('risk_score', 'N/A')}/100\n"
    md += f"- **Status:** {risk.get('status', 'Unknown')}\n"
    
    return Response(md, mimetype='text/markdown')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
