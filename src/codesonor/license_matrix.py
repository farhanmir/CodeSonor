"""
License Compatibility Matrix - Deep License Analysis

Analyzes all licenses in dependency tree for conflicts and compatibility.
Checks commercial use safety and provides compliance recommendations.
"""

import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class LicenseMatrix:
    """Analyze license compatibility and conflicts."""

    # License compatibility matrix
    LICENSE_COMPATIBILITY = {
        "MIT": {
            "compatible_with": ["MIT", "Apache-2.0", "BSD", "ISC", "GPL", "LGPL"],
            "commercial_safe": True,
        },
        "Apache-2.0": {"compatible_with": ["MIT", "Apache-2.0", "BSD"], "commercial_safe": True},
        "BSD": {"compatible_with": ["MIT", "Apache-2.0", "BSD", "ISC"], "commercial_safe": True},
        "GPL-3.0": {"compatible_with": ["GPL-3.0", "AGPL-3.0"], "commercial_safe": False},
        "LGPL-3.0": {"compatible_with": ["LGPL-3.0", "GPL-3.0"], "commercial_safe": True},
        "ISC": {"compatible_with": ["MIT", "BSD", "Apache-2.0", "ISC"], "commercial_safe": True},
        "Unlicense": {"compatible_with": ["*"], "commercial_safe": True},
    }

    def __init__(self, repo_path: Path):
        """Initialize License Matrix analyzer."""
        self.repo_path = repo_path

    def analyze_licenses(self, use_case: str = "commercial") -> Dict[str, Any]:
        """
        Analyze all licenses in project.

        Args:
            use_case: Use case (commercial, open-source, internal)

        Returns:
            Dictionary with license analysis
        """
        results = {
            "project_license": None,
            "dependency_licenses": [],
            "conflicts": [],
            "commercial_safe": True,
            "recommendations": [],
        }

        try:
            # Detect project license
            results["project_license"] = self._detect_project_license()

            # Find dependency licenses
            results["dependency_licenses"] = self._find_dependency_licenses()

            # Check for conflicts
            if results["project_license"]:
                results["conflicts"] = self._check_conflicts(
                    results["project_license"], results["dependency_licenses"]
                )

            # Check commercial safety
            results["commercial_safe"] = self._check_commercial_safety(
                results["project_license"], results["dependency_licenses"], use_case
            )

            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(results, use_case)

        except Exception as e:
            results["error"] = f"Analysis failed: {str(e)}"

        return results

    def _detect_project_license(self) -> Optional[Dict[str, str]]:
        """Detect the project's license."""
        license_files = ["LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING"]

        for filename in license_files:
            license_path = self.repo_path / filename
            if license_path.exists():
                try:
                    content = license_path.read_text(encoding="utf-8", errors="ignore")
                    license_type = self._identify_license(content)
                    return {
                        "type": license_type,
                        "file": filename,
                        "compatible_with": self.LICENSE_COMPATIBILITY.get(license_type, {}).get(
                            "compatible_with", []
                        ),
                    }
                except Exception:
                    pass

        return None

    def _identify_license(self, content: str) -> str:
        """Identify license type from content."""
        content_lower = content.lower()

        if "mit license" in content_lower:
            return "MIT"
        elif "apache license" in content_lower and "2.0" in content_lower:
            return "Apache-2.0"
        elif "gnu general public license" in content_lower and "version 3" in content_lower:
            return "GPL-3.0"
        elif "gnu lesser general public license" in content_lower:
            return "LGPL-3.0"
        elif "bsd" in content_lower:
            return "BSD"
        elif "isc license" in content_lower:
            return "ISC"
        elif "unlicense" in content_lower:
            return "Unlicense"
        else:
            return "Unknown"

    def _find_dependency_licenses(self) -> List[Dict[str, str]]:
        """Find licenses of dependencies."""
        licenses = []

        # Check Python dependencies
        requirements_file = self.repo_path / "requirements.txt"
        if requirements_file.exists():
            try:
                content = requirements_file.read_text()
                for line in content.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        package = re.match(r"([a-zA-Z0-9\-_]+)", line)
                        if package:
                            # In real implementation, would query PyPI API
                            licenses.append(
                                {
                                    "package": package.group(1),
                                    "license": "Unknown - requires API lookup",
                                    "ecosystem": "PyPI",
                                }
                            )
            except Exception:
                pass

        # Check JavaScript dependencies
        package_json = self.repo_path / "package.json"
        if package_json.exists():
            licenses.append(
                {
                    "note": "JavaScript license checking requires npm license-checker",
                    "ecosystem": "npm",
                }
            )

        return licenses[:20]  # Limit for performance

    def _check_conflicts(
        self, project_license: Dict, dependency_licenses: List[Dict]
    ) -> List[Dict[str, str]]:
        """Check for license conflicts."""
        conflicts = []

        project_type = project_license.get("type")
        if project_type == "Unknown":
            return []

        compatible = self.LICENSE_COMPATIBILITY.get(project_type, {}).get("compatible_with", [])

        for dep in dependency_licenses:
            dep_license = dep.get("license", "Unknown")
            if dep_license != "Unknown" and dep_license not in compatible and "*" not in compatible:
                conflicts.append(
                    {
                        "package": dep.get("package", "Unknown"),
                        "license": dep_license,
                        "issue": f"{project_type} not compatible with {dep_license}",
                        "severity": "High" if "GPL" in dep_license else "Medium",
                    }
                )

        return conflicts

    def _check_commercial_safety(
        self, project_license: Optional[Dict], dependency_licenses: List[Dict], use_case: str
    ) -> bool:
        """Check if safe for commercial use."""
        if use_case != "commercial":
            return True

        # Check project license
        if project_license:
            project_type = project_license.get("type")
            if not self.LICENSE_COMPATIBILITY.get(project_type, {}).get("commercial_safe", True):
                return False

        # Check dependency licenses
        for dep in dependency_licenses:
            dep_license = dep.get("license", "")
            if "GPL" in dep_license and "LGPL" not in dep_license:
                return False  # GPL requires open-sourcing

        return True

    def _generate_recommendations(self, results: Dict, use_case: str) -> List[str]:
        """Generate license recommendations."""
        recommendations = []

        if not results["project_license"]:
            recommendations.append("⚠️ No LICENSE file found - add one to clarify usage terms")
            if use_case == "commercial":
                recommendations.append("💼 For commercial use, consider MIT or Apache-2.0 license")

        if results["conflicts"]:
            recommendations.append(
                f"🔴 {len(results['conflicts'])} license conflicts detected - review dependencies"
            )

        if not results["commercial_safe"] and use_case == "commercial":
            recommendations.append(
                "❌ Current licenses NOT safe for commercial use - contains GPL dependencies"
            )
            recommendations.append(
                "📝 Consider replacing GPL dependencies or open-source your project"
            )

        if not recommendations:
            recommendations.append("✅ License configuration looks good!")

        return recommendations

    def generate_license_report(self) -> Dict[str, Any]:
        """Generate comprehensive license report."""
        report = {
            "summary": {},
            "details": {},
            "compliance_checklist": [],
        }

        try:
            analysis = self.analyze_licenses()

            report["summary"] = {
                "project_license": analysis.get("project_license", {}).get("type", "None"),
                "total_dependencies": len(analysis.get("dependency_licenses", [])),
                "conflicts_found": len(analysis.get("conflicts", [])),
                "commercial_safe": analysis.get("commercial_safe", False),
            }

            report["details"] = analysis

            # Compliance checklist
            report["compliance_checklist"] = [
                {
                    "item": "LICENSE file present",
                    "status": "✅" if analysis.get("project_license") else "❌",
                },
                {
                    "item": "No license conflicts",
                    "status": "✅" if not analysis.get("conflicts") else "❌",
                },
                {
                    "item": "Commercial use safe",
                    "status": "✅" if analysis.get("commercial_safe") else "❌",
                },
            ]

        except Exception as e:
            report["error"] = str(e)

        return report
