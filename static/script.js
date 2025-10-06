// API endpoint - adjust if deploying to a different server
const API_URL = 'http://localhost:5000';

async function analyzeRepository() {
    const repoUrl = document.getElementById('repoUrl').value.trim();
    
    // Validate input
    if (!repoUrl) {
        showError('Please enter a GitHub repository URL');
        return;
    }
    
    if (!repoUrl.includes('github.com')) {
        showError('Please enter a valid GitHub repository URL');
        return;
    }
    
    // Hide previous results and errors
    hideResults();
    hideError();
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: repoUrl })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze repository');
        }
        
        // Hide loading
        hideLoading();
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        hideLoading();
        showError(error.message);
        console.error('Analysis error:', error);
    }
}

function displayResults(data) {
    // Repository Information
    document.getElementById('repoName').textContent = data.repository.name;
    document.getElementById('repoDescription').textContent = data.repository.description || 'No description available';
    document.getElementById('repoOwner').textContent = data.repository.owner;
    document.getElementById('repoLink').href = data.repository.url;
    document.getElementById('repoStars').textContent = data.repository.stars.toLocaleString();
    document.getElementById('repoForks').textContent = data.repository.forks.toLocaleString();
    
    // Statistics
    document.getElementById('totalFiles').textContent = data.statistics.total_files;
    document.getElementById('repoCreated').textContent = formatDate(data.repository.created_at);
    document.getElementById('repoUpdated').textContent = formatDate(data.repository.updated_at);
    
    // Language Distribution
    displayLanguageStats(data.statistics.language_distribution);
    
    // AI Analysis
    displayAIAnalysis(data.ai_analysis);
    
    // File List
    displayFileList(data.file_list);
    
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

function displayLanguageStats(languageDistribution) {
    const container = document.getElementById('languageStats');
    container.innerHTML = '';
    
    if (Object.keys(languageDistribution).length === 0) {
        container.innerHTML = '<p class="text-muted">No recognized programming languages found.</p>';
        return;
    }
    
    // Create color mapping
    const colorMap = {
        'Python': 'lang-python',
        'JavaScript': 'lang-javascript',
        'TypeScript': 'lang-typescript',
        'Java': 'lang-java',
        'C++': 'lang-cpp',
        'C': 'lang-c',
        'C#': 'lang-csharp',
        'Go': 'lang-go',
        'Ruby': 'lang-ruby',
        'PHP': 'lang-php',
        'Swift': 'lang-swift',
        'Kotlin': 'lang-kotlin',
        'Rust': 'lang-rust',
        'HTML': 'lang-html',
        'CSS': 'lang-css',
    };
    
    for (const [language, percentage] of Object.entries(languageDistribution)) {
        const colorClass = colorMap[language] || 'lang-default';
        
        const langDiv = document.createElement('div');
        langDiv.className = 'language-bar';
        langDiv.innerHTML = `
            <div class="language-bar-label">
                <span><strong>${language}</strong></span>
                <span>${percentage}%</span>
            </div>
            <div class="progress language-bar-progress">
                <div class="progress-bar ${colorClass}" role="progressbar" 
                     style="width: ${percentage}%;" 
                     aria-valuenow="${percentage}" 
                     aria-valuemin="0" 
                     aria-valuemax="100">
                </div>
            </div>
        `;
        container.appendChild(langDiv);
    }
}

function displayAIAnalysis(aiAnalyses) {
    const container = document.getElementById('aiAnalysis');
    container.innerHTML = '';
    
    if (!aiAnalyses || aiAnalyses.length === 0) {
        container.innerHTML = '<p class="text-muted">No AI analysis available. This may happen if the repository has no analyzable code files or if the AI API is not configured.</p>';
        return;
    }
    
    aiAnalyses.forEach((analysis, index) => {
        const analysisDiv = document.createElement('div');
        analysisDiv.className = 'ai-analysis-item';
        analysisDiv.innerHTML = `
            <h5><i class="bi bi-file-earmark-code"></i> ${analysis.file}</h5>
            <div class="analysis-content">
                ${formatAISummary(analysis.summary)}
            </div>
        `;
        container.appendChild(analysisDiv);
    });
}

function formatAISummary(summary) {
    // Convert the summary to HTML with proper formatting
    const lines = summary.split('\n');
    let formatted = '<div>';
    
    lines.forEach(line => {
        if (line.trim().startsWith('#')) {
            // Header
            formatted += `<h6>${line.replace(/^#+\s*/, '')}</h6>`;
        } else if (line.trim().startsWith('*') || line.trim().startsWith('-')) {
            // List item
            formatted += `<li>${line.replace(/^[*-]\s*/, '')}</li>`;
        } else if (line.trim()) {
            // Regular paragraph
            formatted += `<p>${line}</p>`;
        }
    });
    
    formatted += '</div>';
    return formatted;
}

function displayFileList(files) {
    const container = document.getElementById('fileList');
    container.innerHTML = '';
    
    if (!files || files.length === 0) {
        container.innerHTML = '<p class="text-muted">No files found.</p>';
        return;
    }
    
    files.forEach(file => {
        const fileDiv = document.createElement('div');
        fileDiv.className = 'file-item';
        fileDiv.innerHTML = `<i class="bi bi-file-earmark"></i> ${file}`;
        container.appendChild(fileDiv);
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
}

function showLoading() {
    document.getElementById('loadingSection').style.display = 'block';
    document.getElementById('analyzeBtn').disabled = true;
}

function hideLoading() {
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('analyzeBtn').disabled = false;
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorSection').style.display = 'block';
}

function hideError() {
    document.getElementById('errorSection').style.display = 'none';
}

function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
}

// Allow Enter key to trigger analysis
document.getElementById('repoUrl').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        analyzeRepository();
    }
});
