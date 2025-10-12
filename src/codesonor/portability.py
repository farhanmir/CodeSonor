"""
Code Portability Score - Migration Planning

Analyzes how easily code can be ported to another language or framework.
Identifies platform-specific dependencies and migration challenges.
"""

import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class PortabilityAnalyzer:
    """Analyze code portability and migration difficulty."""

    # Framework-specific patterns
    FRAMEWORK_PATTERNS = {
        "flask": {
            "imports": ["from flask import", "import flask"],
            "decorators": ["@app.route", "@blueprint"],
            "functions": ["Flask(", "render_template(", "jsonify("],
        },
        "django": {
            "imports": ["from django", "import django"],
            "files": ["models.py", "views.py", "urls.py", "settings.py"],
            "functions": ["django.conf", "models.Model"],
        },
        "fastapi": {
            "imports": ["from fastapi import", "import fastapi"],
            "decorators": ["@app.get", "@app.post"],
            "functions": ["FastAPI("],
        },
        "express": {
            "imports": ["require('express')", "import express"],
            "functions": ["app.get(", "app.post(", "express()"],
        },
        "react": {
            "imports": ["from 'react'", "import React"],
            "functions": ["useState", "useEffect", "React.Component"],
        },
    }

    def __init__(self, repo_path: Path):
        """Initialize Portability Analyzer."""
        self.repo_path = repo_path

    def analyze_portability(self, target_framework: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze code portability.

        Args:
            target_framework: Target framework to migrate to (e.g., 'fastapi', 'react')

        Returns:
            Dictionary with portability analysis
        """
        results = {
            "current_framework": None,
            "portability_score": 0,
            "framework_dependencies": [],
            "platform_specific": [],
            "migration_challenges": [],
            "recommendations": [],
        }

        try:
            # Detect current framework
            results["current_framework"] = self._detect_framework()

            # Analyze dependencies
            results["framework_dependencies"] = self._find_framework_dependencies(
                results["current_framework"]
            )

            # Find platform-specific code
            results["platform_specific"] = self._find_platform_specific()

            # Calculate portability score
            results["portability_score"] = self._calculate_portability_score(
                results["framework_dependencies"], results["platform_specific"]
            )

            # If target specified, analyze migration
            if target_framework:
                results["migration_challenges"] = self._analyze_migration(
                    results["current_framework"],
                    target_framework,
                    results["framework_dependencies"],
                )

            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(results)

        except Exception as e:
            results["error"] = f"Analysis failed: {str(e)}"

        return results

    def _detect_framework(self) -> Optional[str]:
        """Detect the primary framework used."""
        framework_scores = Counter()

        # Check Python files
        py_files = list(self.repo_path.rglob("*.py"))
        for file_path in py_files[:100]:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")

                for framework, patterns in self.FRAMEWORK_PATTERNS.items():
                    score = 0
                    for import_pattern in patterns.get("imports", []):
                        if import_pattern in content:
                            score += 2
                    for func_pattern in patterns.get("functions", []):
                        if func_pattern in content:
                            score += 1
                    if score > 0:
                        framework_scores[framework] += score
            except Exception:
                continue

        # Check for specific files
        for framework, patterns in self.FRAMEWORK_PATTERNS.items():
            for file_name in patterns.get("files", []):
                if list(self.repo_path.rglob(file_name)):
                    framework_scores[framework] += 3

        # Check JavaScript files
        js_files = list(self.repo_path.rglob("*.js")) + list(self.repo_path.rglob("*.jsx"))
        for file_path in js_files[:50]:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")

                if "require('express')" in content or "import express" in content:
                    framework_scores["express"] += 3
                if "from 'react'" in content or "import React" in content:
                    framework_scores["react"] += 3
            except Exception:
                continue

        if framework_scores:
            return framework_scores.most_common(1)[0][0]
        return None

    def _find_framework_dependencies(self, framework: Optional[str]) -> List[Dict[str, Any]]:
        """Find code that depends on specific framework."""
        dependencies = []

        if not framework:
            return dependencies

        patterns = self.FRAMEWORK_PATTERNS.get(framework, {})
        code_files = list(self.repo_path.rglob("*.py")) + list(self.repo_path.rglob("*.js"))

        for file_path in code_files[:100]:
            if "node_modules" in str(file_path) or "venv" in str(file_path):
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                lines = content.split("\n")

                file_deps = []
                for line_num, line in enumerate(lines, 1):
                    # Check for framework-specific imports
                    for import_pattern in patterns.get("imports", []):
                        if import_pattern in line:
                            file_deps.append(
                                {
                                    "line": line_num,
                                    "type": "Import",
                                    "code": line.strip(),
                                }
                            )

                    # Check for decorators
                    for decorator in patterns.get("decorators", []):
                        if decorator in line:
                            file_deps.append(
                                {
                                    "line": line_num,
                                    "type": "Decorator",
                                    "code": line.strip(),
                                }
                            )

                if file_deps:
                    dependencies.append(
                        {
                            "file": str(file_path.relative_to(self.repo_path)),
                            "count": len(file_deps),
                            "examples": file_deps[:5],
                        }
                    )

            except Exception:
                continue

        return dependencies[:20]

    def _find_platform_specific(self) -> List[Dict[str, str]]:
        """Find platform-specific code."""
        platform_specific = []

        # Common platform-specific patterns
        patterns = {
            "Windows-only": [r"import win32", r"from win32", r"\.exe['\"]"],
            "Unix-only": [r"/usr/", r"/etc/", r"os\.fork\("],
            "Path separators": [r"\\\\", r"path\.split\('/'"],
        }

        code_files = list(self.repo_path.rglob("*.py"))

        for file_path in code_files[:50]:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")

                for platform, pattern_list in patterns.items():
                    for pattern in pattern_list:
                        if re.search(pattern, content):
                            platform_specific.append(
                                {
                                    "file": str(file_path.relative_to(self.repo_path)),
                                    "issue": platform,
                                    "pattern": pattern,
                                }
                            )
                            break
            except Exception:
                continue

        return platform_specific

    def _calculate_portability_score(
        self, dependencies: List[Dict], platform_specific: List[Dict]
    ) -> int:
        """Calculate portability score (0-100, higher = more portable)."""
        score = 100

        # Penalize for framework dependencies
        total_deps = sum(d["count"] for d in dependencies)
        score -= min(50, total_deps)  # Max penalty of 50

        # Penalize for platform-specific code
        score -= len(platform_specific) * 5

        return max(0, score)

    def _analyze_migration(
        self, source: Optional[str], target: str, dependencies: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Analyze migration challenges."""
        challenges = []

        if not source:
            return [{"challenge": "Unknown source framework - manual analysis needed"}]

        # Define migration difficulty
        migration_map = {
            ("flask", "fastapi"): {
                "difficulty": "Medium",
                "challenges": [
                    "Route decorators are similar but not identical",
                    "Request/response handling differs",
                    "Need to adapt middleware",
                ],
                "estimated_effort": "2-4 weeks for medium-sized app",
            },
            ("flask", "django"): {
                "difficulty": "Hard",
                "challenges": [
                    "Complete architectural shift (micro to batteries-included)",
                    "ORM differences (SQLAlchemy vs Django ORM)",
                    "URL routing completely different",
                    "Template syntax changes",
                ],
                "estimated_effort": "1-3 months",
            },
            ("express", "fastapi"): {
                "difficulty": "Hard",
                "challenges": [
                    "Language change (JavaScript to Python)",
                    "Different async paradigms",
                    "Middleware system differs",
                ],
                "estimated_effort": "2-4 months",
            },
        }

        migration_key = (source, target)
        migration_info = migration_map.get(
            migration_key,
            {
                "difficulty": "Unknown",
                "challenges": ["No predefined migration path - requires custom analysis"],
                "estimated_effort": "Variable",
            },
        )

        challenges.append(
            {
                "source": source,
                "target": target,
                "difficulty": migration_info["difficulty"],
                "main_challenges": migration_info["challenges"],
                "estimated_effort": migration_info["estimated_effort"],
                "files_to_modify": len(dependencies),
            }
        )

        return challenges

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate portability recommendations."""
        recommendations = []

        score = results["portability_score"]

        if score >= 70:
            recommendations.append("✅ Code is highly portable with minimal framework coupling")
        elif score >= 40:
            recommendations.append(
                "🟡 Moderate portability - some refactoring needed for migration"
            )
        else:
            recommendations.append("🔴 Low portability - heavily framework-dependent")

        if results["platform_specific"]:
            recommendations.append(
                f"⚠️ {len(results['platform_specific'])} platform-specific code patterns detected - "
                "use pathlib and cross-platform libraries"
            )

        if results["framework_dependencies"]:
            recommendations.append(
                "🔧 Consider abstracting framework-specific code into adapter layer for easier migration"
            )

        return recommendations
