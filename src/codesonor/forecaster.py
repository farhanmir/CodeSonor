"""
Code Climate Prediction - AI-Powered Future Forecasting

Uses machine learning to predict future code quality issues and technical debt.
Provides early warnings and trend-based recommendations.
"""

import math
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import numpy as np
    from sklearn.linear_model import LinearRegression

    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

try:
    from git import Repo

    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False


class CodeClimatePredictor:
    """Predicts future code quality trends using ML."""

    def __init__(self, repo_path: Path):
        """
        Initialize Code Climate Predictor.

        Args:
            repo_path: Path to the repository
        """
        self.repo_path = repo_path
        self.repo = None

        if GIT_AVAILABLE:
            try:
                self.repo = Repo(repo_path)
            except Exception:
                pass

    def forecast_quality(self, months_ahead: int = 3) -> Dict[str, Any]:
        """
        Forecast code quality trends.

        Args:
            months_ahead: Number of months to forecast

        Returns:
            Dictionary with predictions and recommendations
        """
        if not ML_AVAILABLE:
            return {
                "error": "scikit-learn not installed. Install with: pip install scikit-learn numpy"
            }

        if not self.repo:
            return {"error": "Git repository not available"}

        results = {
            "predictions": [],
            "warnings": [],
            "recommendations": [],
            "confidence": "Unknown",
        }

        try:
            # Collect historical data
            historical_data = self._collect_historical_data()

            if len(historical_data) < 10:
                return {"error": "Insufficient historical data (need at least 10 commits)"}

            # Make predictions
            predictions = self._make_predictions(historical_data, months_ahead)
            results["predictions"] = predictions

            # Identify warnings
            results["warnings"] = self._identify_warnings(predictions)

            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(
                predictions, historical_data
            )

            # Calculate confidence
            results["confidence"] = self._calculate_confidence(historical_data)

        except Exception as e:
            results["error"] = f"Forecast failed: {str(e)}"

        return results

    def _collect_historical_data(self, limit: int = 200) -> List[Dict[str, Any]]:
        """Collect historical code quality metrics."""
        data_points = []

        try:
            commits = list(self.repo.iter_commits("HEAD", max_count=limit))

            for i, commit in enumerate(commits):
                # Calculate metrics for this commit
                metrics = self._calculate_commit_metrics(commit)
                metrics["sequence"] = i
                metrics["date"] = datetime.fromtimestamp(commit.committed_date)
                data_points.append(metrics)

        except Exception:
            pass

        return data_points

    def _calculate_commit_metrics(self, commit) -> Dict[str, float]:
        """Calculate code quality metrics for a commit."""
        metrics = {
            "complexity": 50.0,
            "debt_score": 0.0,
            "file_count": 0,
            "line_count": 0,
        }

        try:
            # Get file stats
            metrics["file_count"] = len(commit.stats.files)

            # Count lines added
            for file_stats in commit.stats.files.values():
                metrics["line_count"] += file_stats.get("insertions", 0)

            # Detect technical debt indicators
            message = commit.message.lower()
            debt_keywords = ["todo", "fixme", "hack", "workaround", "temp", "quick fix"]
            debt_count = sum(1 for keyword in debt_keywords if keyword in message)
            metrics["debt_score"] = debt_count * 10.0

            # Estimate complexity (simple heuristic)
            if metrics["file_count"] > 10:
                metrics["complexity"] += 20
            if metrics["line_count"] > 500:
                metrics["complexity"] += 15

        except Exception:
            pass

        return metrics

    def _make_predictions(
        self, historical_data: List[Dict], months_ahead: int
    ) -> List[Dict[str, Any]]:
        """Make predictions using linear regression."""
        predictions = []

        try:
            # Prepare data for regression
            X = np.array([[d["sequence"]] for d in historical_data])

            # Predict complexity trend
            y_complexity = np.array([d["complexity"] for d in historical_data])
            model_complexity = LinearRegression()
            model_complexity.fit(X, y_complexity)

            # Predict debt trend
            y_debt = np.array([d["debt_score"] for d in historical_data])
            model_debt = LinearRegression()
            model_debt.fit(X, y_debt)

            # Make future predictions
            last_sequence = historical_data[-1]["sequence"]
            last_date = historical_data[-1]["date"]

            # Predict for each month
            for month in range(1, months_ahead + 1):
                future_sequence = last_sequence + (month * 30)  # Assume 30 commits/month
                future_date = last_date + timedelta(days=month * 30)

                complexity_pred = model_complexity.predict([[future_sequence]])[0]
                debt_pred = model_debt.predict([[future_sequence]])[0]

                predictions.append(
                    {
                        "month": month,
                        "date": future_date.strftime("%Y-%m"),
                        "complexity": round(complexity_pred, 2),
                        "debt_score": round(max(0, debt_pred), 2),
                        "status": self._get_status(complexity_pred, debt_pred),
                    }
                )

        except Exception:
            pass

        return predictions

    def _get_status(self, complexity: float, debt: float) -> str:
        """Get status based on predicted metrics."""
        if complexity > 80 or debt > 50:
            return "🔴 Critical - Intervention needed"
        elif complexity > 65 or debt > 30:
            return "🟠 Warning - Monitor closely"
        else:
            return "🟢 Healthy - Continue current practices"

    def _identify_warnings(self, predictions: List[Dict]) -> List[str]:
        """Identify specific warnings from predictions."""
        warnings = []

        if not predictions:
            return warnings

        # Check for increasing complexity
        first_complexity = predictions[0]["complexity"]
        last_complexity = predictions[-1]["complexity"]

        if last_complexity > first_complexity + 15:
            warnings.append(
                f"⚠️ Complexity expected to increase {last_complexity - first_complexity:.1f}% "
                f"over next {len(predictions)} months"
            )

        # Check for technical debt accumulation
        first_debt = predictions[0]["debt_score"]
        last_debt = predictions[-1]["debt_score"]

        if last_debt > first_debt + 20:
            warnings.append("⚠️ Technical debt accumulating rapidly - refactoring recommended")

        # Check for critical thresholds
        for pred in predictions:
            if "Critical" in pred["status"]:
                warnings.append(
                    f"🔴 Critical threshold predicted by {pred['date']} - plan refactoring now"
                )
                break

        if not warnings:
            warnings.append("✅ No major issues predicted in forecast period")

        return warnings

    def _generate_recommendations(
        self, predictions: List[Dict], historical_data: List[Dict]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        if not predictions:
            return ["Unable to generate recommendations"]

        # Analyze trend
        trend_increasing = predictions[-1]["complexity"] > predictions[0]["complexity"]

        if trend_increasing:
            recommendations.append("📊 Consider implementing code quality gates in CI/CD")
            recommendations.append("🔄 Schedule regular refactoring sprints (monthly recommended)")

        # Check current debt level
        current_debt = historical_data[0]["debt_score"] if historical_data else 0
        if current_debt > 30:
            recommendations.append("🧹 Address existing technical debt before adding new features")

        # File size recommendations
        avg_file_count = sum(d["file_count"] for d in historical_data) / len(historical_data)
        if avg_file_count > 15:
            recommendations.append(
                "📁 Commits are touching many files - consider smaller, focused changes"
            )

        return recommendations

    def _calculate_confidence(self, historical_data: List[Dict]) -> str:
        """Calculate prediction confidence based on data quality."""
        if len(historical_data) < 20:
            return "Low - Limited historical data"
        elif len(historical_data) < 50:
            return "Medium - Moderate historical data"
        else:
            return "High - Substantial historical data"

    def predict_file_issues(self, file_path: str) -> Dict[str, Any]:
        """
        Predict when a specific file might need refactoring.

        Args:
            file_path: Path to the file relative to repo root

        Returns:
            Dictionary with file-specific predictions
        """
        if not self.repo:
            return {"error": "Git repository not available"}

        results = {
            "file": file_path,
            "history": [],
            "prediction": None,
        }

        try:
            # Get commit history for this file
            commits = list(self.repo.iter_commits("HEAD", paths=file_path, max_count=50))

            if len(commits) < 5:
                return {"error": "Insufficient history for this file"}

            # Analyze file change frequency
            change_count = len(commits)
            first_commit = commits[-1]
            last_commit = commits[0]

            days_span = (
                datetime.fromtimestamp(last_commit.committed_date)
                - datetime.fromtimestamp(first_commit.committed_date)
            ).days

            if days_span > 0:
                changes_per_month = (change_count / days_span) * 30

                results["history"] = {
                    "total_commits": change_count,
                    "days_tracked": days_span,
                    "changes_per_month": round(changes_per_month, 2),
                }

                # Make prediction
                if changes_per_month > 10:
                    results["prediction"] = {
                        "status": "🔴 High churn rate",
                        "recommendation": "This file changes frequently - candidate for refactoring",
                        "estimated_refactor_date": "Within 1-2 months",
                    }
                elif changes_per_month > 5:
                    results["prediction"] = {
                        "status": "🟡 Moderate churn",
                        "recommendation": "Monitor this file for growing complexity",
                        "estimated_refactor_date": "Within 3-6 months",
                    }
                else:
                    results["prediction"] = {
                        "status": "🟢 Stable",
                        "recommendation": "File is stable, no immediate action needed",
                    }

        except Exception as e:
            results["error"] = str(e)

        return results
