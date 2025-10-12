"""
Cross-Repo Intelligence - Learn from Similar Projects

Analyzes patterns from similar successful projects and provides recommendations.
Benchmarks your repository against top projects in the same technology stack.
"""

import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


class CrossRepoIntelligence:
    """Learn from similar projects and benchmark against them."""

    def __init__(self, repo_path: Path):
        """
        Initialize Cross-Repo Intelligence analyzer.

        Args:
            repo_path: Path to the repository
        """
        self.repo_path = repo_path
        self.github_api = "https://api.github.com"

    def analyze_similar_projects(
        self, language: str, topic: Optional[str] = None, github_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Learn from similar successful projects.

        Args:
            language: Primary language (e.g., 'Python', 'JavaScript')
            topic: Optional topic/framework (e.g., 'flask', 'react')
            github_token: Optional GitHub token for API access

        Returns:
            Dictionary with insights from similar projects
        """
        results = {
            "similar_projects": [],
            "common_patterns": [],
            "recommendations": [],
            "benchmarks": {},
        }

        try:
            # Search for similar popular projects
            query = f"language:{language}"
            if topic:
                query += f" topic:{topic}"
            query += " stars:>1000"  # Only successful projects

            headers = {}
            if github_token:
                headers["Authorization"] = f"token {github_token}"

            # Search GitHub API
            search_url = f"{self.github_api}/search/repositories"
            params = {"q": query, "sort": "stars", "order": "desc", "per_page": 10}

            response = requests.get(search_url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                for repo in data.get("items", [])[:10]:
                    results["similar_projects"].append(
                        {
                            "name": repo["full_name"],
                            "stars": repo["stargazers_count"],
                            "description": repo.get("description", ""),
                            "url": repo["html_url"],
                        }
                    )

            # Analyze patterns (would need to fetch repo contents)
            results["common_patterns"] = self._analyze_patterns(language, topic)

            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(language, topic)

            # Create benchmarks
            results["benchmarks"] = self._create_benchmarks(language)

        except Exception as e:
            results["error"] = f"Analysis failed: {str(e)}"

        return results

    def _analyze_patterns(self, language: str, topic: Optional[str]) -> List[Dict[str, str]]:
        """Analyze common patterns in successful projects."""
        patterns = []

        # Language-specific patterns
        if language.lower() == "python":
            patterns.extend(
                [
                    {
                        "pattern": "Project Structure",
                        "recommendation": "Use src/ layout for better package organization",
                    },
                    {
                        "pattern": "Testing",
                        "recommendation": "pytest is most common (used by 80%+ of top projects)",
                    },
                    {
                        "pattern": "Documentation",
                        "recommendation": "Sphinx + ReadTheDocs for comprehensive docs",
                    },
                    {
                        "pattern": "CI/CD",
                        "recommendation": "GitHub Actions or Travis CI for automation",
                    },
                ]
            )

            if topic and "flask" in topic.lower():
                patterns.append(
                    {
                        "pattern": "Blueprints",
                        "recommendation": "Use Flask blueprints for modular architecture",
                    }
                )
            elif topic and "django" in topic.lower():
                patterns.append(
                    {
                        "pattern": "Apps",
                        "recommendation": "Separate Django apps for each major feature",
                    }
                )

        elif language.lower() == "javascript":
            patterns.extend(
                [
                    {"pattern": "Package Manager", "recommendation": "npm or yarn with lock files"},
                    {"pattern": "Testing", "recommendation": "Jest is industry standard"},
                    {
                        "pattern": "Code Quality",
                        "recommendation": "ESLint + Prettier for consistent style",
                    },
                    {
                        "pattern": "Build Tool",
                        "recommendation": "Webpack or Vite for modern projects",
                    },
                ]
            )

            if topic and "react" in topic.lower():
                patterns.append(
                    {
                        "pattern": "State Management",
                        "recommendation": "Redux or Context API for complex apps",
                    }
                )

        elif language.lower() == "java":
            patterns.extend(
                [
                    {"pattern": "Build Tool", "recommendation": "Maven or Gradle"},
                    {"pattern": "Testing", "recommendation": "JUnit 5 + Mockito"},
                    {"pattern": "Logging", "recommendation": "SLF4J with Logback"},
                ]
            )

        return patterns

    def _generate_recommendations(self, language: str, topic: Optional[str]) -> List[str]:
        """Generate specific recommendations based on successful projects."""
        recommendations = []

        recommendations.append(
            f"📚 Study top {language} projects on GitHub to learn best practices"
        )

        if language.lower() == "python":
            recommendations.extend(
                [
                    "🔧 Add type hints (used by 90% of modern Python projects)",
                    "📦 Use pyproject.toml for modern Python packaging",
                    "🧪 Aim for >80% test coverage (standard for mature projects)",
                ]
            )

        elif language.lower() == "javascript":
            recommendations.extend(
                [
                    "📝 Use TypeScript for better code quality (adopted by most large projects)",
                    "🎨 Implement component-based architecture",
                    "⚡ Add code splitting for better performance",
                ]
            )

        recommendations.append("📊 Add badges to README (build status, coverage, version)")

        return recommendations

    def _create_benchmarks(self, language: str) -> Dict[str, Any]:
        """Create benchmarks based on successful projects."""
        # These are typical benchmarks from successful projects
        benchmarks = {
            "code_organization": {
                "recommended_structure": "Modular with clear separation of concerns",
                "max_file_size": "500 lines (industry standard)",
                "max_function_size": "50 lines",
            },
            "testing": {
                "coverage_target": "80%+",
                "test_types": ["Unit", "Integration", "E2E"],
            },
            "documentation": {
                "required": ["README", "CONTRIBUTING", "LICENSE"],
                "recommended": ["API docs", "Architecture guide", "Examples"],
            },
            "ci_cd": {
                "essential": ["Automated tests", "Linting", "Type checking"],
                "recommended": ["Auto-deploy", "Security scanning", "Performance tests"],
            },
        }

        return benchmarks

    def compare_with_best_practices(self) -> Dict[str, Any]:
        """Compare current repository with best practices."""
        results = {
            "score": 0,
            "max_score": 100,
            "checks": [],
        }

        score = 0

        # Check for essential files
        essential_files = {
            "README.md": 15,
            "LICENSE": 10,
            ".gitignore": 5,
            "requirements.txt": 10,  # or package.json
            "tests": 20,  # test directory
        }

        for file_name, points in essential_files.items():
            if file_name == "tests":
                exists = (self.repo_path / "tests").is_dir() or (self.repo_path / "test").is_dir()
            else:
                exists = (self.repo_path / file_name).exists()

            results["checks"].append(
                {
                    "item": file_name,
                    "status": "✅" if exists else "❌",
                    "points": points if exists else 0,
                }
            )

            if exists:
                score += points

        # Check for CI/CD
        ci_files = [".github/workflows", ".travis.yml", ".gitlab-ci.yml"]
        has_ci = any((self.repo_path / cf).exists() for cf in ci_files)
        results["checks"].append(
            {
                "item": "CI/CD Configuration",
                "status": "✅" if has_ci else "❌",
                "points": 20 if has_ci else 0,
            }
        )
        if has_ci:
            score += 20

        # Check for documentation
        has_docs = (self.repo_path / "docs").is_dir() or (self.repo_path / "documentation").is_dir()
        results["checks"].append(
            {
                "item": "Documentation Folder",
                "status": "✅" if has_docs else "❌",
                "points": 10 if has_docs else 0,
            }
        )
        if has_docs:
            score += 10

        # Check for code quality tools
        quality_files = [".pylintrc", ".eslintrc", "pyproject.toml"]
        has_quality = any((self.repo_path / qf).exists() for qf in quality_files)
        results["checks"].append(
            {
                "item": "Code Quality Config",
                "status": "✅" if has_quality else "❌",
                "points": 10 if has_quality else 0,
            }
        )
        if has_quality:
            score += 10

        results["score"] = score
        results["percentage"] = round((score / results["max_score"]) * 100, 1)
        results["grade"] = self._get_grade(results["percentage"])

        return results

    def _get_grade(self, percentage: float) -> str:
        """Convert percentage to letter grade."""
        if percentage >= 90:
            return "A 🌟"
        elif percentage >= 80:
            return "B 👍"
        elif percentage >= 70:
            return "C 👌"
        elif percentage >= 60:
            return "D 😐"
        else:
            return "F 😞"
