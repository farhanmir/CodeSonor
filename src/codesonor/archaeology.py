"""
Code Archaeology - Historical Evolution Analysis

Analyzes how code quality and complexity have evolved over time.
Tracks technical debt accumulation and identifies when issues were introduced.
"""

import re
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from git import Git, Repo

    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False


class CodeArchaeology:
    """Analyzes repository evolution and historical patterns."""

    def __init__(self, repo_path: Path):
        """
        Initialize Code Archaeology analyzer.

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

    def analyze_evolution(self, since: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        Analyze how code has evolved over time.

        Args:
            since: Start date (ISO format: YYYY-MM-DD) or None for all history
            limit: Maximum number of commits to analyze

        Returns:
            Dictionary with evolution metrics
        """
        if not self.repo:
            return {"error": "Git repository not available or GitPython not installed"}

        results = {
            "summary": {},
            "quality_trend": [],
            "complexity_trend": [],
            "debt_timeline": [],
            "impact_commits": [],
            "file_churn": {},
        }

        try:
            # Get commits
            commits = list(self.repo.iter_commits("HEAD", max_count=limit))
            if since:
                since_date = datetime.fromisoformat(since)
                commits = [
                    c for c in commits if datetime.fromtimestamp(c.committed_date) >= since_date
                ]

            if not commits:
                return {"error": "No commits found in specified range"}

            results["summary"] = {
                "total_commits": len(commits),
                "date_range": {
                    "start": datetime.fromtimestamp(commits[-1].committed_date).isoformat(),
                    "end": datetime.fromtimestamp(commits[0].committed_date).isoformat(),
                },
                "unique_authors": len(set(c.author.name for c in commits)),
            }

            # Analyze each commit for quality indicators
            for commit in commits:
                commit_date = datetime.fromtimestamp(commit.committed_date)

                # Calculate commit metrics
                stats = self._analyze_commit(commit)

                # Track quality trend
                results["quality_trend"].append(
                    {
                        "date": commit_date.isoformat(),
                        "commit": commit.hexsha[:8],
                        "files_changed": stats["files_changed"],
                        "insertions": stats["insertions"],
                        "deletions": stats["deletions"],
                        "quality_score": stats["quality_score"],
                    }
                )

                # Identify technical debt signals
                if stats["debt_signals"]:
                    results["debt_timeline"].append(
                        {
                            "date": commit_date.isoformat(),
                            "commit": commit.hexsha[:8],
                            "message": commit.message.split("\n")[0][:100],
                            "author": commit.author.name,
                            "debt_signals": stats["debt_signals"],
                        }
                    )

                # Track file churn
                for file in stats["files"]:
                    if file not in results["file_churn"]:
                        results["file_churn"][file] = 0
                    results["file_churn"][file] += 1

            # Identify high-impact commits
            results["impact_commits"] = self._identify_impact_commits(results["quality_trend"])

            # Calculate trends
            results["trends"] = self._calculate_trends(results["quality_trend"])

            # Get most churned files
            results["high_churn_files"] = sorted(
                results["file_churn"].items(), key=lambda x: x[1], reverse=True
            )[:10]

        except Exception as e:
            results["error"] = f"Analysis failed: {str(e)}"

        return results

    def _analyze_commit(self, commit) -> Dict[str, Any]:
        """Analyze a single commit for quality metrics."""
        stats = {
            "files_changed": 0,
            "insertions": 0,
            "deletions": 0,
            "quality_score": 50.0,  # Base score
            "debt_signals": [],
            "files": [],
        }

        try:
            # Get commit stats
            commit_stats = commit.stats.files
            stats["files_changed"] = len(commit_stats)

            for file_path, file_stats in commit_stats.items():
                stats["files"].append(file_path)
                stats["insertions"] += file_stats.get("insertions", 0)
                stats["deletions"] += file_stats.get("deletions", 0)

            # Analyze commit message for debt signals
            message = commit.message.lower()
            debt_keywords = {
                "TODO": "todo|fixme|hack|workaround",
                "Quick fix": "quick fix|temp|temporary",
                "Refactor needed": "needs? refactor|technical debt",
                "Bug fix": "bug|fix|hotfix",
            }

            for signal_type, pattern in debt_keywords.items():
                if re.search(pattern, message):
                    stats["debt_signals"].append(signal_type)

            # Calculate quality score based on commit characteristics
            # Smaller, focused commits = higher quality
            if stats["files_changed"] > 20:
                stats["quality_score"] -= 20
            elif stats["files_changed"] > 10:
                stats["quality_score"] -= 10
            elif stats["files_changed"] <= 3:
                stats["quality_score"] += 10

            # Large line changes = potential issues
            total_changes = stats["insertions"] + stats["deletions"]
            if total_changes > 1000:
                stats["quality_score"] -= 15
            elif total_changes > 500:
                stats["quality_score"] -= 5

            # Commit message quality
            if len(commit.message.split("\n")[0]) > 50:
                stats["quality_score"] += 5  # Good descriptive message

            # Debt signals penalty
            stats["quality_score"] -= len(stats["debt_signals"]) * 5

            # Ensure score stays in range
            stats["quality_score"] = max(0, min(100, stats["quality_score"]))

        except Exception:
            pass

        return stats

    def _identify_impact_commits(self, quality_trend: List[Dict]) -> List[Dict]:
        """Identify commits with significant quality impact."""
        if len(quality_trend) < 2:
            return []

        impact_commits = []

        for i in range(1, len(quality_trend)):
            current = quality_trend[i]
            previous = quality_trend[i - 1]

            quality_change = current["quality_score"] - previous["quality_score"]

            # Significant quality drop
            if quality_change < -15:
                impact_commits.append(
                    {
                        "commit": current["commit"],
                        "date": current["date"],
                        "impact": "Negative",
                        "quality_change": quality_change,
                        "files_changed": current["files_changed"],
                    }
                )

            # Significant quality improvement
            elif quality_change > 15:
                impact_commits.append(
                    {
                        "commit": current["commit"],
                        "date": current["date"],
                        "impact": "Positive",
                        "quality_change": quality_change,
                        "files_changed": current["files_changed"],
                    }
                )

        return sorted(impact_commits, key=lambda x: abs(x["quality_change"]), reverse=True)[:10]

    def _calculate_trends(self, quality_trend: List[Dict]) -> Dict[str, Any]:
        """Calculate overall trends from quality data."""
        if not quality_trend:
            return {}

        # Calculate average quality over time
        avg_quality = sum(q["quality_score"] for q in quality_trend) / len(quality_trend)

        # Calculate trend direction (simple linear approximation)
        if len(quality_trend) >= 2:
            first_half = quality_trend[len(quality_trend) // 2 :]
            second_half = quality_trend[: len(quality_trend) // 2]

            avg_first = sum(q["quality_score"] for q in first_half) / len(first_half)
            avg_second = sum(q["quality_score"] for q in second_half) / len(second_half)

            trend_direction = "Improving" if avg_second > avg_first else "Declining"
            trend_magnitude = abs(avg_second - avg_first)
        else:
            trend_direction = "Stable"
            trend_magnitude = 0

        return {
            "average_quality": round(avg_quality, 2),
            "direction": trend_direction,
            "magnitude": round(trend_magnitude, 2),
            "status": self._get_trend_status(trend_direction, trend_magnitude),
        }

    def _get_trend_status(self, direction: str, magnitude: float) -> str:
        """Get human-readable status from trend data."""
        if direction == "Stable":
            return "✅ Code quality is stable"
        elif direction == "Improving":
            if magnitude > 10:
                return "🚀 Code quality improving significantly"
            else:
                return "📈 Code quality gradually improving"
        else:  # Declining
            if magnitude > 10:
                return "⚠️ Code quality declining - intervention needed"
            else:
                return "📉 Code quality gradually declining"

    def find_debt_sources(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Find the origin of technical debt in a file or repository.

        Args:
            file_path: Specific file to analyze, or None for all files

        Returns:
            Dictionary with debt source information
        """
        if not self.repo:
            return {"error": "Git repository not available"}

        debt_sources = {
            "files": [],
            "total_debt_lines": 0,
            "oldest_debt": None,
        }

        try:
            # Search for debt indicators in code
            debt_patterns = [
                (r"#\s*(TODO|FIXME|HACK|XXX)", "TODO/FIXME"),
                (r"//\s*(TODO|FIXME|HACK|XXX)", "TODO/FIXME"),
                (r"(workaround|temporary|quick.?fix)", "Temporary code"),
            ]

            files_to_check = []
            if file_path:
                files_to_check = [Path(file_path)]
            else:
                # Get all code files
                for ext in [".py", ".js", ".java", ".go", ".rb", ".php"]:
                    files_to_check.extend(self.repo_path.rglob(f"*{ext}"))

            for file in files_to_check:
                if not file.is_file():
                    continue

                try:
                    content = file.read_text(encoding="utf-8", errors="ignore")
                    lines = content.split("\n")

                    file_debt = []
                    for line_num, line in enumerate(lines, 1):
                        for pattern, debt_type in debt_patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                # Try to find when this was introduced
                                blame_info = self._get_line_blame(file, line_num)
                                file_debt.append(
                                    {
                                        "line": line_num,
                                        "type": debt_type,
                                        "content": line.strip()[:100],
                                        "introduced": blame_info,
                                    }
                                )
                                debt_sources["total_debt_lines"] += 1

                    if file_debt:
                        debt_sources["files"].append(
                            {
                                "path": str(file.relative_to(self.repo_path)),
                                "debt_count": len(file_debt),
                                "debt_items": file_debt[:5],  # Limit to first 5
                            }
                        )

                except Exception:
                    continue

            # Sort files by debt count
            debt_sources["files"].sort(key=lambda x: x["debt_count"], reverse=True)
            debt_sources["files"] = debt_sources["files"][:20]  # Top 20 files

        except Exception as e:
            debt_sources["error"] = str(e)

        return debt_sources

    def _get_line_blame(self, file_path: Path, line_num: int) -> Optional[Dict[str, str]]:
        """Get blame information for a specific line."""
        if not self.repo:
            return None

        try:
            relative_path = file_path.relative_to(self.repo_path)
            blame = self.repo.blame("HEAD", str(relative_path))

            current_line = 0
            for commit, lines in blame:
                current_line += len(lines)
                if current_line >= line_num:
                    return {
                        "commit": commit.hexsha[:8],
                        "author": commit.author.name,
                        "date": datetime.fromtimestamp(commit.committed_date).isoformat(),
                    }
        except Exception:
            pass

        return None
