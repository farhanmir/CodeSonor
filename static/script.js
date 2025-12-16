const analyzeBtn = document.getElementById('analyzeBtn');
const repoUrlInput = document.getElementById('repoUrl');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
let currentAnalysisData = null;

// Data Display Elements
const repoName = document.getElementById('repoName');
const repoDescription = document.getElementById('repoDescription');
const repoOwner = document.getElementById('repoOwner');
const repoLink = document.getElementById('repoLink');
const repoStars = document.getElementById('repoStars');
const repoForks = document.getElementById('repoForks');
const repoCreated = document.getElementById('repoCreated');
const repoUpdated = document.getElementById('repoUpdated');
const totalFiles = document.getElementById('totalFiles');
const languageStats = document.getElementById('languageStats');
const aiAnalysis = document.getElementById('aiAnalysis');
const fileList = document.getElementById('fileList');
const teamDnaResults = document.getElementById('teamDnaResults');
const depRiskResults = document.getElementById('depRiskResults');

async function analyzeRepository() {
    const url = repoUrlInput.value.trim();
    
    if (!url) {
        showError('Please enter a GitHub repository URL');
        return;
    }

    // Basic URL validation
    if (!url.includes('github.com')) {
        showError('Please enter a valid GitHub URL');
        return;
    }

    // UI Reset
    hideError();
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'block';
    analyzeBtn.disabled = true;

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze repository');
        }

        currentAnalysisData = data;
        displayResults(data);

    } catch (error) {
        showError(error.message);
    } finally {
        loadingSection.style.display = 'none';
        analyzeBtn.disabled = false;
    }
}

function displayResults(data) {
    // 1. Basic Stats (assuming simplified structure for now or adapting to new structure)
    // The new app.py might behave slightly differently, let's adapt:
    // If getting GitHub metadata (stars etc) required the API call we removed, we might need to rely on what we have.
    // However, RepoCloner doesn't give stars/forks easily without API. 
    // To keep it simple and authentic to "Clean Update", we'll just show what we have or placeholder if missing.
    
    // NOTE: app.py refactor removed the GitHub API call for repo metadata (stars, forks) to standardizing on cloning.
    // We will handle potential missing metadata gracefully.
    
    if (data.repository) {
        repoName.textContent = data.repository.name || 'Repository';
        repoDescription.textContent = data.repository.description || 'No description';
        repoOwner.textContent = data.repository.owner || 'Unknown';
        repoLink.href = data.repository.url || '#';
        repoStars.textContent = data.repository.stars || '-';
        repoForks.textContent = data.repository.forks || '-';
        repoCreated.textContent = new Date(data.repository.created_at).toLocaleDateString() || '-';
        repoUpdated.textContent = new Date(data.repository.updated_at).toLocaleDateString() || '-';
    } else {
        // Fallback if metadata not provided by backend (since we removed API call)
        repoName.textContent = "Analysis Results";
        repoDescription.textContent = "Deep analysis via local clone.";
        repoOwner.textContent = "-";
        repoStars.textContent = "-";
        repoForks.textContent = "-";
    }

    // 2. Statistics
    totalFiles.textContent = data.statistics.total_files;
    
    // Language Distribution
    renderLanguageStats(data.statistics.languages);

    // 3. AI Analysis
    renderAIAnalysis(data.ai_analysis);

    // 4. File List (Optional, if provided)
    if (data.file_list) {
        fileList.innerHTML = data.file_list.map(f => `<div class="file-item">${f}</div>`).join('');
    } else {
        fileList.innerHTML = '<div class="text-muted">File list not available in summary view</div>';
    }

    // 5. Team DNA
    renderTeamDNA(data.team_dna);

    // 6. Dependency Risk
    renderDepRisk(data.dependency_risk);

    resultsSection.style.display = 'block';
}

function renderLanguageStats(languages) {
    languageStats.innerHTML = '';
    
    if (!languages || Object.keys(languages).length === 0) {
        languageStats.innerHTML = '<p class="text-muted">No language data available</p>';
        return;
    }

    // Convert to array if it's a dict {Lang: Count} or {Lang: Percentage}
    // Our new LanguageStats usually returns {Lang: {files: X, code: Y, comment: Z}} or similar, 
    // but let's assume simple dict for now or handle list.
    // If it's the complex list from LanguageStats:
    let langArray = [];
    if (Array.isArray(languages)) {
         // Assuming [{name: 'Python', count: 10}]
         langArray = languages;
    } else {
         // Object to array
         for (const [lang, stats] of Object.entries(languages)) {
             // quick hack for simple percentage visualization
             langArray.push({name: lang, percentage: stats.percentage || 0}); 
         }
    }

    langArray.forEach(lang => {
        const name = lang.name || lang;
        const percentage = lang.percentage || 0;
        const safeName = name.toLowerCase().replace('#', 'sharp').replace('++', 'pp');
        
        const html = `
            <div class="language-bar">
                <div class="language-bar-label">
                    <span>${name}</span>
                    <span>${percentage}%</span>
                </div>
                <div class="progress language-bar-progress">
                    <div class="progress-bar lang-${safeName} lang-default" 
                         role="progressbar" 
                         style="width: ${percentage}%" 
                         aria-valuenow="${percentage}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                    </div>
                </div>
            </div>
        `;
        languageStats.insertAdjacentHTML('beforeend', html);
    });
}

function renderAIAnalysis(analyses) {
    aiAnalysis.innerHTML = '';
    
    if (!analyses || analyses.length === 0) {
        aiAnalysis.innerHTML = `
            <div class="alert alert-info">
                <i class="bi bi-info-circle"></i> 
                AI Analysis unavailable. Check if GEMINI_API_KEY is configured.
            </div>`;
        return;
    }

    analyses.forEach(item => {
        const html = `
            <div class="ai-analysis-item">
                <h5><i class="bi bi-file-earmark-code"></i> ${item.file}</h5>
                <pre>${item.summary}</pre>
            </div>
        `;
        aiAnalysis.insertAdjacentHTML('beforeend', html);
    });
}

function renderTeamDNA(dna) {
    teamDnaResults.innerHTML = '';
    
    if (!dna || dna.error) {
         teamDnaResults.innerHTML = `<div class="alert alert-warning">${dna?.error || 'No data'}</div>`;
         return;
    }

    // Render Contributor List summary
    let contributorsHtml = '<ul class="list-group list-group-flush">';
    for (const [name, profile] of Object.entries(dna.contributors || {})) {
        contributorsHtml += `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>${name}</span>
                <span class="badge bg-secondary rounded-pill">${profile.total_commits} commits</span>
            </li>
        `;
    }
    contributorsHtml += '</ul>';

    // Render Anomalies
    let anomaliesHtml = '';
    if (dna.anomalies && dna.anomalies.length > 0) {
        anomaliesHtml = '<h6 class="mt-3 text-danger">Anomalies Detected:</h6><ul class="list-unstyled">';
        dna.anomalies.forEach(a => {
             anomaliesHtml += `<li><i class="bi bi-exclamation-circle text-danger"></i> <strong>${a.contributor}</strong>: ${a.description}</li>`;
        });
        anomaliesHtml += '</ul>';
    }

    teamDnaResults.innerHTML = contributorsHtml + anomaliesHtml;
}

function renderDepRisk(risk) {
    depRiskResults.innerHTML = '';
    
    if (!risk) {
        depRiskResults.innerHTML = '<p>No dependency data found.</p>';
        return;
    }
    
    // Simple Score Display
    const scoreColor = risk.risk_score > 50 ? 'text-danger' : (risk.risk_score > 20 ? 'text-warning' : 'text-success');
    
    const html = `
        <div class="text-center mb-3">
             <h2 class="${scoreColor}">${risk.risk_score || 0}/100</h2>
             <span class="text-muted">Risk Score</span>
        </div>
        <div class="list-group">
            ${(risk.vulnerabilities || []).slice(0, 5).map(v => 
                `<div class="list-group-item list-group-item-danger">
                    <strong>${v.package}</strong>: ${v.issue}
                </div>`
            ).join('')}
        </div>
        <p class="mt-2 small text-muted">Total Dependencies Analyzed: ${risk.total_dependencies || 0}</p>
    `;
    depRiskResults.innerHTML = html;
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    resultsSection.style.display = 'none';
}

function hideError() {
    errorSection.style.display = 'none';
}

async function exportMarkdown() {
    if (!currentAnalysisData) return;
    
    try {
        const response = await fetch('/export/markdown', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentAnalysisData)
        });
        
        if (!response.ok) throw new Error('Export failed');
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `codesonor-report-${currentAnalysisData.repository.name || 'repo'}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        showError("Export failed: " + error.message);
    }
}
