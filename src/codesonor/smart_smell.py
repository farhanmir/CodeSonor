"""
Smart Code Smell Detection - Context-Aware Linting

Detects code smells with context and predicts when they'll become problems.
Goes beyond static analysis to provide situational recommendations.
"""

import ast
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class SmartSmellDetector:
    """Context-aware code smell detection."""

    def __init__(self, repo_path: Path):
        """Initialize Smart Smell Detector."""
        self.repo_path = repo_path

    def detect_smells(self, context: str = "production") -> Dict[str, Any]:
        """
        Detect code smells with context awareness.

        Args:
            context: Context (production, development, startup, enterprise)

        Returns:
            Dictionary with detected smells and recommendations
        """
        results = {
            "smells": [],
            "critical_issues": [],
            "context_warnings": [],
            "summary": {},
        }

        try:
            # Find Python files
            py_files = [
                f
                for f in self.repo_path.rglob("*.py")
                if "venv" not in str(f) and "node_modules" not in str(f)
            ]

            for file_path in py_files[:50]:  # Limit for performance
                file_smells = self._analyze_file(file_path, context)
                results["smells"].extend(file_smells)

            # Categorize by severity
            results["critical_issues"] = [
                s for s in results["smells"] if s["severity"] == "Critical"
            ]
            results["context_warnings"] = [
                s for s in results["smells"] if s.get("context_specific")
            ]

            # Generate summary
            results["summary"] = self._generate_summary(results["smells"], context)

        except Exception as e:
            results["error"] = f"Detection failed: {str(e)}"

        return results

    def _analyze_file(self, file_path: Path, context: str) -> List[Dict[str, Any]]:
        """Analyze a single file for code smells."""
        smells = []

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.split("\n")

            # Parse AST for Python files
            try:
                tree = ast.parse(content)
                smells.extend(self._analyze_ast(tree, file_path, context))
            except SyntaxError:
                pass

            # Line-based checks
            for line_num, line in enumerate(lines, 1):
                # Detect potential issues
                line_smells = self._check_line(line, line_num, context)
                for smell in line_smells:
                    smell["file"] = str(file_path.relative_to(self.repo_path))
                    smells.append(smell)

        except Exception:
            pass

        return smells

    def _analyze_ast(self, tree: ast.AST, file_path: Path, context: str) -> List[Dict[str, Any]]:
        """Analyze AST for code smells."""
        smells = []

        for node in ast.walk(tree):
            # Detect long functions
            if isinstance(node, ast.FunctionDef):
                func_lines = node.end_lineno - node.lineno if hasattr(node, "end_lineno") else 0
                if func_lines > 50:
                    severity = "Critical" if context == "production" else "Medium"
                    smells.append(
                        {
                            "type": "Long Function",
                            "line": node.lineno,
                            "description": f"Function '{node.name}' is {func_lines} lines long",
                            "severity": severity,
                            "context_specific": context == "production",
                            "recommendation": "Break into smaller functions for maintainability",
                        }
                    )

            # Detect deeply nested code
            if isinstance(node, (ast.If, ast.For, ast.While)):
                depth = self._calculate_nesting_depth(node)
                if depth > 3:
                    smells.append(
                        {
                            "type": "Deep Nesting",
                            "line": node.lineno if hasattr(node, "lineno") else 0,
                            "description": f"Nesting depth of {depth} detected",
                            "severity": "Medium",
                            "recommendation": "Refactor to reduce complexity",
                        }
                    )

            # Detect too many parameters
            if isinstance(node, ast.FunctionDef):
                param_count = len(node.args.args)
                if param_count > 5:
                    smells.append(
                        {
                            "type": "Too Many Parameters",
                            "line": node.lineno,
                            "description": f"Function '{node.name}' has {param_count} parameters",
                            "severity": "Low",
                            "recommendation": "Consider using a config object or dataclass",
                        }
                    )

        return smells

    def _calculate_nesting_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth."""
        max_depth = current_depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                child_depth = self._calculate_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)

        return max_depth

    def _check_line(self, line: str, line_num: int, context: str) -> List[Dict[str, Any]]:
        """Check a single line for issues."""
        smells = []

        # Global variables (bad in production)
        if re.match(r"^[A-Z_]+\s*=", line) and context == "production":
            smells.append(
                {
                    "type": "Global Variable",
                    "line": line_num,
                    "description": "Global variable detected",
                    "severity": "Medium",
                    "context_specific": True,
                    "recommendation": "Global state causes issues in multi-threaded/multi-server environments",
                }
            )

        # Hardcoded credentials
        if re.search(r'(password|secret|key|token)\s*=\s*["\']', line, re.IGNORECASE):
            smells.append(
                {
                    "type": "Hardcoded Secret",
                    "line": line_num,
                    "description": "Potential hardcoded secret detected",
                    "severity": "Critical",
                    "recommendation": "Move secrets to environment variables or secret management",
                }
            )

        # Print statements (bad in production)
        if "print(" in line and context in ["production", "enterprise"]:
            smells.append(
                {
                    "type": "Print Statement",
                    "line": line_num,
                    "description": "Print statement found in production code",
                    "severity": "Low",
                    "context_specific": True,
                    "recommendation": "Use proper logging instead of print()",
                }
            )

        # SQL injection risks
        if re.search(r"execute\([^)]*%s[^)]*\)", line) or re.search(r"execute\([^)]*\+", line):
            smells.append(
                {
                    "type": "SQL Injection Risk",
                    "line": line_num,
                    "description": "Potential SQL injection vulnerability",
                    "severity": "Critical",
                    "recommendation": "Use parameterized queries",
                }
            )

        return smells

    def _generate_summary(self, smells: List[Dict], context: str) -> Dict[str, Any]:
        """Generate summary of detected smells."""
        if not smells:
            return {"status": "✅ No significant code smells detected"}

        severity_count = {"Critical": 0, "Medium": 0, "Low": 0}
        type_count = defaultdict(int)

        for smell in smells:
            severity_count[smell.get("severity", "Low")] += 1
            type_count[smell["type"]] += 1

        return {
            "total_smells": len(smells),
            "by_severity": dict(severity_count),
            "most_common": dict(type_count.most_common(5)),
            "status": self._get_status(severity_count, context),
        }

    def _get_status(self, severity_count: Dict, context: str) -> str:
        """Get overall status message."""
        if severity_count["Critical"] > 0:
            return (
                f"🔴 {severity_count['Critical']} critical issues found - immediate action required"
            )
        elif severity_count["Medium"] > 5:
            return "🟡 Multiple medium-severity issues detected"
        else:
            return "🟢 Code quality is acceptable"

    def predict_impact(self, smell_type: str, current_scale: str = "small") -> Dict[str, str]:
        """
        Predict when a code smell will become a problem.

        Args:
            smell_type: Type of smell detected
            current_scale: Current scale (small, medium, large)

        Returns:
            Dictionary with impact prediction
        """
        predictions = {
            "Global Variable": {
                "small": "✅ Works fine now with single instance",
                "medium": "⚠️ Will cause issues when scaling to multiple servers",
                "large": "🔴 Already causing race conditions and bugs",
            },
            "Long Function": {
                "small": "🟡 Maintainable now but will be hard to test",
                "medium": "⚠️ Becoming a bottleneck for new features",
                "large": "🔴 Major refactoring needed",
            },
            "Deep Nesting": {
                "small": "🟡 Hard to read but functional",
                "medium": "⚠️ Increasing bug rate due to complexity",
                "large": "🔴 Untest able and error-prone",
            },
        }

        prediction = predictions.get(smell_type, {}).get(current_scale, "Unknown")

        return {
            "smell": smell_type,
            "current_scale": current_scale,
            "impact": prediction,
            "timeline": self._get_timeline(current_scale),
        }

    def _get_timeline(self, current_scale: str) -> str:
        """Get timeline for when issue will become critical."""
        timelines = {
            "small": "Will become problematic in 6-12 months as you scale",
            "medium": "Already showing issues - fix within 1-3 months",
            "large": "Critical - fix immediately",
        }
        return timelines.get(current_scale, "Unknown")
