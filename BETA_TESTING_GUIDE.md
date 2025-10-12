# 🧪 Beta Testing Guide - CodeSonor v0.5.0

Welcome to the beta testing phase for CodeSonor v0.5.0! This guide will help you test all 12 revolutionary new features.

## 🚀 Quick Start

### 1. Install Beta Version

```bash
# Clone the beta branch
git clone -b beta https://github.com/farhanmir/CodeSonor.git
cd CodeSonor

# Install in development mode
pip install -e .

# Install optional dependencies for full functionality
pip install gitpython scikit-learn numpy networkx packaging license-expression
```

### 2. Run Quick Test

```bash
# Quick sanity check - tests all features
python quick_test.py
```

### 3. Run Comprehensive Tests

```bash
# Run pytest suite
pytest tests/test_beta_features.py -v

# Run manual testing script with real repos
python test_beta_manual.py
```

## 📋 Testing Checklist

Use this checklist to track your testing progress:

### Core Features

- [ ] **🏛️ Code Archaeology** - Historical evolution analysis
  - [ ] Works on git repositories with history
  - [ ] Identifies quality trends over time
  - [ ] Detects hotspots correctly
  - [ ] Timeline data is accurate

- [ ] **🧬 Team DNA** - Contributor behavioral analysis
  - [ ] Analyzes contributor patterns
  - [ ] Detects coding styles
  - [ ] Identifies collaboration patterns
  - [ ] Handles repositories with multiple contributors

- [ ] **⚠️ Dependency Risk Score** - Supply chain health
  - [ ] Reads pyproject.toml / setup.py / requirements.txt
  - [ ] Analyzes dependency tree
  - [ ] Detects outdated packages
  - [ ] Identifies license issues

- [ ] **🔮 Code Climate Prediction** - AI-powered forecasting
  - [ ] Predicts technical debt trends
  - [ ] Works with and without ML libraries
  - [ ] Provides actionable insights
  - [ ] Graceful degradation when sklearn unavailable

- [ ] **🌐 Cross-Repo Intelligence** - Learn from similar projects
  - [ ] Finds similar projects on GitHub
  - [ ] Provides relevant benchmarks
  - [ ] Handles API rate limits gracefully
  - [ ] Returns useful recommendations

- [ ] **🎓 Onboarding Assistant** - New developer guidance
  - [ ] Generates learning paths
  - [ ] Identifies critical files
  - [ ] Creates day-by-day plans
  - [ ] Provides helpful code tours

- [ ] **👃 Smart Code Smell Detection** - Context-aware linting
  - [ ] Detects code smells accurately
  - [ ] Provides context-based severity
  - [ ] Predicts when smells become problems
  - [ ] Works on Python files

- [ ] **⚖️ License Compatibility Matrix** - Deep license analysis
  - [ ] Detects project license
  - [ ] Analyzes dependency licenses
  - [ ] Identifies conflicts
  - [ ] Provides compliance recommendations

- [ ] **⚡ Performance Prediction** - Static performance analysis
  - [ ] Detects O(n²) and O(n³) complexity
  - [ ] Identifies bottlenecks
  - [ ] Predicts scalability issues
  - [ ] Provides optimization suggestions

- [ ] **🎯 AI Code Review Tutor** - Educational reviews
  - [ ] Provides educational explanations
  - [ ] Generates interactive quizzes
  - [ ] Includes learning resources
  - [ ] Teaches best practices

- [ ] **🔄 Code Portability Score** - Migration planning
  - [ ] Detects framework dependencies
  - [ ] Calculates portability score
  - [ ] Generates migration roadmap
  - [ ] Identifies platform-specific code

- [ ] **👥 Team Health Insights** - Collaboration analytics
  - [ ] Calculates team health score
  - [ ] Detects bottlenecks
  - [ ] Identifies bus factor
  - [ ] Analyzes collaboration patterns

### Integration Testing

- [ ] All features work together on the same repository
- [ ] No conflicts between modules
- [ ] Memory usage is reasonable
- [ ] Performance is acceptable (< 30s per feature on medium repos)

### Error Handling

- [ ] Graceful handling of missing dependencies
- [ ] Clear error messages
- [ ] Works on non-git directories (where applicable)
- [ ] Handles empty repositories
- [ ] Handles repositories without Python code

### Platform Testing

- [ ] Works on Windows
- [ ] Works on macOS
- [ ] Works on Linux
- [ ] Python 3.9 compatible
- [ ] Python 3.10 compatible
- [ ] Python 3.11 compatible
- [ ] Python 3.12 compatible

## 🧪 Testing Scenarios

### Scenario 1: Small Python Project
```bash
# Test on a small project like 'requests'
git clone https://github.com/psf/requests test-repo
cd test-repo

# Run a feature
python -c "
from codesonor.archaeology import CodeArchaeology
from pathlib import Path
archaeology = CodeArchaeology(Path('.'))
result = archaeology.analyze()
print(result)
"
```

### Scenario 2: Large Framework
```bash
# Test on Django
git clone https://github.com/django/django test-repo
cd test-repo

# Test team health
python -c "
from codesonor.team_health import TeamHealthAnalyzer
from pathlib import Path
analyzer = TeamHealthAnalyzer(Path('.'))
result = analyzer.analyze()
print(f'Health Score: {result.get(\"health_score\", 0)}')
"
```

### Scenario 3: ML Project
```bash
# Test on scikit-learn
git clone https://github.com/scikit-learn/scikit-learn test-repo
cd test-repo

# Test performance predictor
python -c "
from codesonor.perf_predictor import PerformancePredictor
from pathlib import Path
predictor = PerformancePredictor(Path('.'))
result = predictor.analyze()
print(f'Bottlenecks: {len(result.get(\"bottlenecks\", []))}')
"
```

### Scenario 4: Your Own Project
```bash
# Test on your actual project
cd /path/to/your/project

# Run all features
python /path/to/CodeSonor/test_beta_manual.py
```

## 🐛 Reporting Issues

If you find bugs or issues, please report them with:

### Bug Report Template
```
**Feature**: [Which of the 12 features]
**Python Version**: [e.g., 3.11]
**OS**: [Windows/macOS/Linux]
**Error Message**: [Full error message]
**Steps to Reproduce**:
1. ...
2. ...
3. ...

**Expected Behavior**: [What should happen]
**Actual Behavior**: [What actually happened]
**Repository Tested**: [Public repo URL or description]
```

Create an issue at: https://github.com/farhanmir/CodeSonor/issues

## 📊 GitHub Actions Testing

The beta branch has comprehensive CI/CD:

### Automated Tests
- **Beta Features Testing**: Runs on every push to beta branch
  - Unit tests for all 12 features
  - Integration tests
  - Real repository testing (Flask, Requests, Pytest)
  
- **Cross-Platform Testing**: Windows, macOS, Linux
  
- **Python Version Testing**: 3.9, 3.10, 3.11, 3.12
  
- **Performance Benchmarks**: Ensures features run efficiently
  
- **Security Scanning**: Checks for vulnerabilities

### Manual GitHub Actions Trigger

You can manually trigger tests:

1. Go to: https://github.com/farhanmir/CodeSonor/actions
2. Select "Beta Features Testing"
3. Click "Run workflow"
4. Choose beta branch
5. Click "Run workflow"

## 🎯 Success Criteria

For the beta to be promoted to v0.5.0 or v1.0.0:

- [ ] **10/12 features** working reliably (83% pass rate)
- [ ] **All critical bugs fixed**
- [ ] **Performance acceptable** (< 1 minute per feature on large repos)
- [ ] **Documentation complete**
- [ ] **At least 5 beta testers** provide feedback
- [ ] **Works on all 3 major platforms**
- [ ] **Compatible with Python 3.9-3.12**

## 📈 Performance Expectations

| Repository Size | Feature Runtime | Memory Usage |
|----------------|----------------|--------------|
| Small (<1k files) | < 10 seconds | < 200 MB |
| Medium (1k-5k files) | < 30 seconds | < 500 MB |
| Large (>5k files) | < 2 minutes | < 1 GB |

## 🔄 Update Process

To get latest beta updates:

```bash
cd CodeSonor
git pull origin beta
pip install -e . --upgrade
```

## 💡 Tips for Testing

1. **Start Small**: Test on small repos first to understand features
2. **Use Real Projects**: Test on actual projects you work on
3. **Check Logs**: Look at detailed output for insights
4. **Compare Results**: Run same feature on different repos
5. **Mix Features**: Try combining multiple features
6. **Test Edge Cases**: Empty repos, non-Python projects, etc.

## 🤝 Contributing Feedback

We want to hear from you! Share:

- **What worked well**
- **What didn't work**
- **Feature requests**
- **Performance issues**
- **Documentation improvements**
- **UX suggestions**

## 📅 Timeline

- **Beta Start**: October 12, 2025
- **Testing Period**: 1-2 weeks
- **Bug Fix Phase**: 3-5 days
- **Final Testing**: 2-3 days
- **Release**: Target late October 2025

## 🎉 Thank You!

Thank you for being a beta tester! Your feedback will help make CodeSonor better for everyone.

---

**Questions?** Open an issue or discussion on GitHub!

**Found a critical bug?** Label it as `priority: critical` and `beta-bug`
