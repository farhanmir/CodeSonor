"""
CodeSonor - AI-Powered GitHub Repository Analyzer

A powerful CLI tool for analyzing GitHub repositories with AI-powered insights.
Supports 8 LLM providers and advanced code analysis features.

New in v0.5.0:
- Code Archaeology: Historical evolution analysis
- Team DNA: Contributor behavioral patterns
- Dependency Risk Score: Supply chain health
- Code Climate Prediction: AI-powered forecasting
- Cross-Repo Intelligence: Learn from similar projects
- Onboarding Assistant: New developer guidance
- Smart Code Smell Detection: Context-aware linting
- License Compatibility Matrix: Deep license analysis
- Performance Prediction: Static performance analysis
- AI Code Review Tutor: Educational reviews
- Code Portability Score: Migration planning
- Team Health Insights: Collaboration analytics
"""

__version__ = "0.5.0"
__author__ = "Farhan Mir"

from .analyzer import RepositoryAnalyzer
from .github_client import GitHubClient
from .language_stats import LanguageAnalyzer

__all__ = ["RepositoryAnalyzer", "GitHubClient", "LanguageAnalyzer"]
