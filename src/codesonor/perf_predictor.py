"""
Performance Prediction - Static Performance Analysis

Predicts performance bottlenecks without running code.
Estimates complexity and resource usage from code structure.
"""

import ast
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional


class PerformancePredictor:
    """Predict performance issues from code analysis."""

    def __init__(self, repo_path: Path):
        """Initialize Performance Predictor."""
        self.repo_path = repo_path

    def analyze_performance(self) -> Dict[str, Any]:
        """
        Analyze code for potential performance issues.

        Returns:
            Dictionary with performance predictions
        """
        results = {
            "bottlenecks": [],
            "complexity_issues": [],
            "memory_concerns": [],
            "recommendations": [],
        }

        try:
            # Find Python files
            py_files = [f for f in self.repo_path.rglob("*.py") if "venv" not in str(f)]

            for file_path in py_files[:50]:
                file_issues = self._analyze_file(file_path)
                results["bottlenecks"].extend(file_issues.get("bottlenecks", []))
                results["complexity_issues"].extend(file_issues.get("complexity", []))
                results["memory_concerns"].extend(file_issues.get("memory", []))

            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(results)

            # Calculate summary
            results["summary"] = {
                "total_issues": len(results["bottlenecks"])
                + len(results["complexity_issues"])
                + len(results["memory_concerns"]),
                "critical_bottlenecks": len(
                    [b for b in results["bottlenecks"] if b.get("severity") == "Critical"]
                ),
            }

        except Exception as e:
            results["error"] = f"Analysis failed: {str(e)}"

        return results

    def _analyze_file(self, file_path: Path) -> Dict[str, List[Dict]]:
        """Analyze a single file for performance issues."""
        issues = {"bottlenecks": [], "complexity": [], "memory": []}

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            # Parse AST
            try:
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    # Detect nested loops (O(n²), O(n³), etc.)
                    if isinstance(node, (ast.For, ast.While)):
                        loop_issues = self._analyze_loop(node, file_path)
                        issues["bottlenecks"].extend(loop_issues)

                    # Detect large data structures
                    if isinstance(node, (ast.List, ast.Dict)):
                        if hasattr(node, "elts") and len(node.elts) > 1000:
                            issues["memory"].append(
                                {
                                    "file": str(file_path.relative_to(self.repo_path)),
                                    "line": node.lineno if hasattr(node, "lineno") else 0,
                                    "issue": f"Large literal with {len(node.elts)} elements",
                                    "impact": "High memory usage at startup",
                                }
                            )

                    # Detect recursive functions
                    if isinstance(node, ast.FunctionDef):
                        if self._is_recursive(node):
                            issues["bottlenecks"].append(
                                {
                                    "file": str(file_path.relative_to(self.repo_path)),
                                    "line": node.lineno,
                                    "function": node.name,
                                    "issue": "Recursive function without memoization",
                                    "recommendation": "Add @lru_cache decorator for better performance",
                                }
                            )

            except SyntaxError:
                pass

        except Exception:
            pass

        return issues

    def _analyze_loop(self, node: ast.AST, file_path: Path) -> List[Dict]:
        """Analyze loop for performance issues."""
        issues = []

        # Check for nested loops
        nesting_level = self._count_loop_nesting(node)

        if nesting_level > 1:
            complexity_notation = "O(n²)" if nesting_level == 2 else f"O(n^{nesting_level})"
            severity = "Critical" if nesting_level >= 3 else "High"

            issues.append(
                {
                    "file": str(file_path.relative_to(self.repo_path)),
                    "line": node.lineno if hasattr(node, "lineno") else 0,
                    "issue": f"Nested loop detected - {complexity_notation} complexity",
                    "severity": severity,
                    "estimated_time": self._estimate_loop_time(nesting_level),
                    "recommendation": "Consider using set operations or hash maps for O(n) complexity",
                }
            )

        return issues

    def _count_loop_nesting(self, node: ast.AST, depth: int = 0) -> int:
        """Count the depth of loop nesting."""
        max_depth = depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While)):
                child_depth = self._count_loop_nesting(child, depth + 1)
                max_depth = max(max_depth, child_depth)

        return max_depth

    def _estimate_loop_time(self, nesting_level: int) -> str:
        """Estimate execution time for nested loops."""
        estimates = {
            1: "Fast - O(n) for typical datasets",
            2: "Moderate - ~30s for 10K items, 5min for 100K items",
            3: "Slow - Minutes for 1K items, hours for 10K items",
            4: "Very slow - Impractical for >100 items",
        }
        return estimates.get(nesting_level, "Unknown")

    def _is_recursive(self, func_node: ast.FunctionDef) -> bool:
        """Check if function is recursive."""
        func_name = func_node.name

        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == func_name:
                    return True

        return False

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate performance recommendations."""
        recommendations = []

        if results["bottlenecks"]:
            recommendations.append(
                f"⚡ {len(results['bottlenecks'])} potential bottlenecks detected - consider algorithmic improvements"
            )

        if results["memory_concerns"]:
            recommendations.append(
                "💾 Large data structures found - consider lazy loading or streaming"
            )

        # Specific advice based on complexity issues
        nested_loops = [
            b for b in results["bottlenecks"] if "nested loop" in b.get("issue", "").lower()
        ]
        if nested_loops:
            recommendations.append(
                "🔄 Replace nested loops with set operations or dictionaries for O(n) complexity"
            )

        if not recommendations:
            recommendations.append("✅ No major performance issues predicted")

        return recommendations

    def predict_scalability(self, expected_data_size: str = "medium") -> Dict[str, Any]:
        """
        Predict how code will perform at scale.

        Args:
            expected_data_size: Expected data size (small, medium, large, xlarge)

        Returns:
            Scalability predictions
        """
        size_multipliers = {
            "small": 100,
            "medium": 10000,
            "large": 100000,
            "xlarge": 1000000,
        }

        multiplier = size_multipliers.get(expected_data_size, 10000)

        analysis = self.analyze_performance()

        predictions = {
            "data_size": expected_data_size,
            "items": multiplier,
            "warnings": [],
            "critical_issues": [],
        }

        # Check each bottleneck
        for bottleneck in analysis.get("bottlenecks", []):
            if "O(n²)" in bottleneck.get("issue", ""):
                if multiplier > 10000:
                    predictions["critical_issues"].append(
                        {
                            "location": f"{bottleneck['file']}:{bottleneck.get('line', 0)}",
                            "issue": "O(n²) complexity will be extremely slow at this scale",
                            "estimated_time": f"Hours to complete with {multiplier} items",
                        }
                    )
            elif "O(n^3)" in bottleneck.get("issue", ""):
                predictions["critical_issues"].append(
                    {
                        "location": f"{bottleneck['file']}:{bottleneck.get('line', 0)}",
                        "issue": "O(n³) complexity is impractical at any scale",
                        "estimated_time": "Will not complete in reasonable time",
                    }
                )

        # Memory predictions
        if analysis.get("memory_concerns"):
            if multiplier > 100000:
                predictions["warnings"].append(
                    "⚠️ Large data structures may cause out-of-memory errors at this scale"
                )

        predictions["overall_status"] = self._get_scalability_status(predictions)

        return predictions

    def _get_scalability_status(self, predictions: Dict) -> str:
        """Get overall scalability status."""
        if predictions["critical_issues"]:
            return "🔴 Will NOT scale - critical performance issues"
        elif predictions["warnings"]:
            return "🟡 Will scale with optimizations needed"
        else:
            return "🟢 Should scale well"
