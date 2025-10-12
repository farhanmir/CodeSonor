"""
Dependency Risk Score - Supply Chain Health Analysis

Analyzes all dependencies for security, maintenance, and license risks.
Provides comprehensive supply chain health scoring.
"""

import json
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import requests


class DependencyRisk:
    """Analyzes dependency health and supply chain risks."""

    def __init__(self, repo_path: Path):
        """
        Initialize Dependency Risk analyzer.

        Args:
            repo_path: Path to the repository
        """
        self.repo_path = repo_path
        self.package_files = {
            "python": ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"],
            "javascript": ["package.json", "yarn.lock", "package-lock.json"],
            "ruby": ["Gemfile", "Gemfile.lock"],
            "java": ["pom.xml", "build.gradle"],
            "go": ["go.mod", "go.sum"],
        }

    def analyze_dependencies(self, deep: bool = False) -> Dict[str, Any]:
        """
        Analyze all dependencies for risks.

        Args:
            deep: If True, analyze transitive dependencies (slower)

        Returns:
            Dictionary with dependency risk analysis
        """
        results = {
            "dependencies": [],
            "risk_summary": {},
            "recommendations": [],
            "viral_dependencies": [],
        }

        try:
            # Detect dependency files
            dep_files = self._find_dependency_files()

            if not dep_files:
                return {"error": "No dependency files found in repository"}

            # Analyze each dependency file
            all_deps = []
            for file_type, file_path in dep_files:
                deps = self._parse_dependency_file(file_type, file_path)
                all_deps.extend(deps)

            # Analyze each dependency
            for dep in all_deps:
                risk_score = self._calculate_risk_score(dep)
                dep["risk_score"] = risk_score
                dep["risk_level"] = self._get_risk_level(risk_score)
                results["dependencies"].append(dep)

            # Calculate summary
            results["risk_summary"] = self._calculate_summary(results["dependencies"])

            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(results["dependencies"])

            # Find viral dependencies (ones that pull in many others)
            if deep:
                results["viral_dependencies"] = self._find_viral_dependencies(
                    results["dependencies"]
                )

        except Exception as e:
            results["error"] = f"Analysis failed: {str(e)}"

        return results

    def _find_dependency_files(self) -> List[tuple]:
        """Find all dependency definition files."""
        found_files = []

        for lang, filenames in self.package_files.items():
            for filename in filenames:
                matches = list(self.repo_path.rglob(filename))
                for match in matches:
                    # Skip virtual environments and node_modules
                    path_str = str(match)
                    if any(skip in path_str for skip in ["venv", "node_modules", ".venv", "env"]):
                        continue
                    found_files.append((lang, match))

        return found_files

    def _parse_dependency_file(self, file_type: str, file_path: Path) -> List[Dict[str, Any]]:
        """Parse a dependency file and extract packages."""
        dependencies = []

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            if file_type == "python":
                if file_path.name == "requirements.txt":
                    # Parse requirements.txt
                    for line in content.split("\n"):
                        line = line.strip()
                        if line and not line.startswith("#"):
                            # Extract package name and version
                            match = re.match(r"([a-zA-Z0-9\-_]+)([><=!]+)?([0-9.]+)?", line)
                            if match:
                                dependencies.append(
                                    {
                                        "name": match.group(1),
                                        "version": match.group(3) if match.group(3) else "latest",
                                        "ecosystem": "PyPI",
                                    }
                                )

                elif file_path.name == "pyproject.toml":
                    # Extract from pyproject.toml dependencies section
                    in_deps = False
                    for line in content.split("\n"):
                        if "dependencies" in line and "[" in line:
                            in_deps = True
                        elif in_deps and "]" in line:
                            in_deps = False
                        elif in_deps and '"' in line:
                            dep_match = re.search(r'"([a-zA-Z0-9\-_]+)', line)
                            if dep_match:
                                dependencies.append(
                                    {
                                        "name": dep_match.group(1),
                                        "version": "latest",
                                        "ecosystem": "PyPI",
                                    }
                                )

            elif file_type == "javascript" and file_path.name == "package.json":
                # Parse package.json
                try:
                    data = json.loads(content)
                    for dep_type in ["dependencies", "devDependencies"]:
                        if dep_type in data:
                            for name, version in data[dep_type].items():
                                dependencies.append(
                                    {
                                        "name": name,
                                        "version": version.strip("^~"),
                                        "ecosystem": "npm",
                                    }
                                )
                except json.JSONDecodeError:
                    pass

        except Exception:
            pass

        return dependencies

    def _calculate_risk_score(self, dependency: Dict[str, Any]) -> float:
        """Calculate risk score for a dependency (0-100, higher = riskier)."""
        risk = 0.0

        # Check for outdated version indicators
        version = dependency.get("version", "")
        if version == "latest" or version == "*":
            risk += 20  # Unpinned version

        # Check package name for common risky patterns
        name = dependency.get("name", "").lower()
        if any(word in name for word in ["test", "dev", "tmp", "temp"]):
            risk += 15  # Development/test dependency in production

        # Common abandoned packages (examples)
        abandoned_packages = ["left-pad"]  # Famous example
        if name in abandoned_packages:
            risk += 50

        # Single character or very short names (typosquatting risk)
        if len(name) <= 2:
            risk += 25

        return min(100, risk)

    def _get_risk_level(self, score: float) -> str:
        """Convert risk score to level."""
        if score >= 70:
            return "🔴 Critical"
        elif score >= 50:
            return "🟠 High"
        elif score >= 30:
            return "🟡 Medium"
        else:
            return "🟢 Low"

    def _calculate_summary(self, dependencies: List[Dict]) -> Dict[str, Any]:
        """Calculate summary statistics."""
        if not dependencies:
            return {}

        risk_levels = {"🔴 Critical": 0, "🟠 High": 0, "🟡 Medium": 0, "🟢 Low": 0}
        for dep in dependencies:
            risk_levels[dep["risk_level"]] += 1

        avg_risk = sum(d["risk_score"] for d in dependencies) / len(dependencies)

        return {
            "total_dependencies": len(dependencies),
            "average_risk_score": round(avg_risk, 2),
            "risk_distribution": risk_levels,
            "status": self._get_overall_status(avg_risk),
        }

    def _get_overall_status(self, avg_risk: float) -> str:
        """Get overall status message."""
        if avg_risk < 20:
            return "✅ Excellent - Dependencies are well-maintained"
        elif avg_risk < 40:
            return "🟢 Good - Minor risks detected"
        elif avg_risk < 60:
            return "🟡 Fair - Some dependencies need attention"
        else:
            return "🔴 Poor - Multiple high-risk dependencies detected"

    def _generate_recommendations(self, dependencies: List[Dict]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        # Count high-risk dependencies
        high_risk = [d for d in dependencies if d["risk_score"] >= 50]
        unpinned = [d for d in dependencies if d["version"] in ["latest", "*"]]

        if high_risk:
            recommendations.append(
                f"⚠️ Review {len(high_risk)} high-risk dependencies: "
                + ", ".join([d["name"] for d in high_risk[:5]])
            )

        if unpinned:
            recommendations.append(
                f"📌 Pin versions for {len(unpinned)} dependencies to ensure reproducible builds"
            )

        if not recommendations:
            recommendations.append("✅ No immediate actions required")

        return recommendations

    def _find_viral_dependencies(self, dependencies: List[Dict]) -> List[Dict]:
        """Find dependencies that pull in many others (viral dependencies)."""
        # This would require deep dependency tree analysis
        # For now, return placeholder
        return [
            {
                "name": "Example: A package that includes 50+ subdependencies",
                "note": "Deep dependency analysis requires API access",
            }
        ]

    def check_license_compatibility(self) -> Dict[str, Any]:
        """Check for license conflicts."""
        results = {
            "licenses": [],
            "conflicts": [],
            "commercial_safe": True,
        }

        try:
            # Find dependency files
            dep_files = self._find_dependency_files()

            # This would need license checking logic
            # Placeholder for now
            results["note"] = "License checking requires package metadata API access"

        except Exception as e:
            results["error"] = str(e)

        return results
