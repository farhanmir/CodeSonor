"""Tests for CodeSonor package"""

import pytest
from codesonor.github_client import GitHubClient
from codesonor.language_stats import LanguageAnalyzer


class TestGitHubClient:
    """Tests for GitHub client functionality"""
    
    def test_parse_url_valid(self):
        """Test parsing valid GitHub URLs"""
        client = GitHubClient()
        
        # Test HTTPS URL
        owner, repo = client.parse_url("https://github.com/python/cpython")
        assert owner == "python"
        assert repo == "cpython"
        
        # Test git URL
        owner, repo = client.parse_url("git@github.com:python/cpython.git")
        assert owner == "python"
        assert repo == "cpython"
    
    def test_parse_url_invalid(self):
        """Test parsing invalid URLs"""
        client = GitHubClient()
        
        with pytest.raises(ValueError):
            client.parse_url("https://gitlab.com/user/repo")
        
        with pytest.raises(ValueError):
            client.parse_url("not-a-url")


class TestLanguageAnalyzer:
    """Tests for language analysis functionality"""
    
    def test_language_extensions(self):
        """Test language detection from file extensions"""
        analyzer = LanguageAnalyzer()
        
        # Test various extensions
        assert ".py" in analyzer.LANGUAGE_EXTENSIONS["Python"]
        assert ".js" in analyzer.LANGUAGE_EXTENSIONS["JavaScript"]
        assert ".java" in analyzer.LANGUAGE_EXTENSIONS["Java"]
        assert ".cpp" in analyzer.LANGUAGE_EXTENSIONS["C++"]
    
    def test_calculate_stats(self):
        """Test language statistics calculation"""
        analyzer = LanguageAnalyzer()
        
        files = [
            {"name": "app.py", "path": "src/app.py"},
            {"name": "utils.py", "path": "src/utils.py"},
            {"name": "script.js", "path": "static/script.js"},
            {"name": "README.md", "path": "README.md"},
        ]
        
        stats = analyzer.calculate_stats(files)
        
        assert "Python" in stats
        assert "JavaScript" in stats
        assert stats["Python"]["count"] == 2
        assert stats["JavaScript"]["count"] == 1
        assert stats["Python"]["percentage"] > stats["JavaScript"]["percentage"]
    
    def test_get_primary_language(self):
        """Test primary language detection"""
        analyzer = LanguageAnalyzer()
        
        stats = {
            "Python": {"count": 10, "percentage": 70.0},
            "JavaScript": {"count": 3, "percentage": 21.0},
            "CSS": {"count": 1, "percentage": 9.0},
        }
        
        primary = analyzer.get_primary_language(stats)
        assert primary == "Python"
    
    def test_filter_by_language(self):
        """Test filtering files by language"""
        analyzer = LanguageAnalyzer()
        
        files = [
            {"name": "app.py", "path": "src/app.py"},
            {"name": "utils.py", "path": "src/utils.py"},
            {"name": "script.js", "path": "static/script.js"},
        ]
        
        python_files = analyzer.filter_by_language(files, "Python")
        assert len(python_files) == 2
        assert all(f["name"].endswith(".py") for f in python_files)
        
        js_files = analyzer.filter_by_language(files, "JavaScript")
        assert len(js_files) == 1
        assert js_files[0]["name"] == "script.js"


class TestImports:
    """Test that all modules can be imported"""
    
    def test_import_github_client(self):
        """Test importing GitHubClient"""
        from codesonor import GitHubClient
        assert GitHubClient is not None
    
    def test_import_language_analyzer(self):
        """Test importing LanguageAnalyzer"""
        from codesonor import LanguageAnalyzer
        assert LanguageAnalyzer is not None
    
    def test_import_repository_analyzer(self):
        """Test importing RepositoryAnalyzer"""
        from codesonor import RepositoryAnalyzer
        assert RepositoryAnalyzer is not None
    
    def test_package_version(self):
        """Test that package has version"""
        import codesonor
        assert hasattr(codesonor, "__version__")
        assert codesonor.__version__ == "0.1.0"
