"""
Team Health Insights - Collaboration Analytics

Analyzes PR patterns, review bottlenecks, and team collaboration health.
Detects potential team dysfunction and communication issues.
"""

import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from git import Repo

    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False


class TeamHealthAnalyzer:
    """Analyze team collaboration and health metrics."""

    def __init__(self, repo_path: Path):
        """Initialize Team Health Analyzer."""
        self.repo_path = repo_path
        self.repo = None

        if GIT_AVAILABLE:
            try:
                self.repo = Repo(repo_path)
            except Exception:
                pass

    def analyze_team_health(self) -> Dict[str, Any]:
        """
        Analyze team collaboration health.

        Returns:
            Dictionary with team health metrics
        """
        results = {
            "commit_patterns": {},
            "collaboration_score": 0,
            "bottlenecks": [],
            "communication_issues": [],
            "recommendations": [],
        }

        if not self.repo:
            return {"error": "Git repository not available or GitPython not installed"}

        try:
            # Analyze commit patterns
            results["commit_patterns"] = self._analyze_commit_patterns()

            # Detect bottlenecks
            results["bottlenecks"] = self._detect_bottlenecks(results["commit_patterns"])

            # Check communication health
            results["communication_issues"] = self._check_communication()

            # Calculate collaboration score
            results["collaboration_score"] = self._calculate_collaboration_score(results)

            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(results)

        except Exception as e:
            results["error"] = f"Analysis failed: {str(e)}"

        return results

    def _analyze_commit_patterns(self, limit: int = 500) -> Dict[str, Any]:
        """Analyze patterns in commits."""
        patterns = {
            "contributors": {},
            "commit_frequency": defaultdict(int),
            "contribution_distribution": {},
        }

        try:
            commits = list(self.repo.iter_commits("HEAD", max_count=limit))

            # Group by author
            author_commits = defaultdict(list)
            for commit in commits:
                author_commits[commit.author.name].append(commit)

            # Analyze each contributor
            for author, author_commits_list in author_commits.items():
                commit_dates = [
                    datetime.fromtimestamp(c.committed_date) for c in author_commits_list
                ]

                # Calculate metrics
                if commit_dates:
                    date_range = (max(commit_dates) - min(commit_dates)).days
                    commits_per_week = (len(commit_dates) / max(date_range, 1)) * 7

                    # Analyze commit sizes
                    commit_sizes = []
                    for commit in author_commits_list:
                        try:
                            size = sum(commit.stats.files.values(), [])
                            if isinstance(size, list):
                                size = len(size)
                            commit_sizes.append(size)
                        except:
                            pass

                    avg_size = sum(commit_sizes) / len(commit_sizes) if commit_sizes else 0

                    patterns["contributors"][author] = {
                        "total_commits": len(author_commits_list),
                        "commits_per_week": round(commits_per_week, 2),
                        "avg_commit_size": round(avg_size, 2),
                        "date_range_days": date_range,
                    }

            # Calculate contribution distribution
            total_commits = len(commits)
            for author, stats in patterns["contributors"].items():
                percentage = (stats["total_commits"] / total_commits) * 100
                patterns["contribution_distribution"][author] = round(percentage, 1)

        except Exception:
            pass

        return patterns

    def _detect_bottlenecks(self, patterns: Dict) -> List[Dict[str, Any]]:
        """Detect collaboration bottlenecks."""
        bottlenecks = []

        contributors = patterns.get("contributors", {})
        if not contributors:
            return bottlenecks

        # Check for single-person dominance
        distribution = patterns.get("contribution_distribution", {})
        for author, percentage in distribution.items():
            if percentage > 70:
                bottlenecks.append(
                    {
                        "type": "Single Contributor Dominance",
                        "contributor": author,
                        "impact": f"{percentage}% of commits by one person",
                        "severity": "High",
                        "risk": "Bus factor of 1 - critical knowledge concentrated",
                    }
                )

        # Check for inactive contributors
        for author, stats in contributors.items():
            if stats["commits_per_week"] < 0.5 and stats["total_commits"] > 5:
                bottlenecks.append(
                    {
                        "type": "Declining Activity",
                        "contributor": author,
                        "impact": f"Only {stats['commits_per_week']:.1f} commits/week",
                        "severity": "Medium",
                        "risk": "Contributor may be disengaging",
                    }
                )

        # Check for uneven commit sizes
        commit_sizes = [stats["avg_commit_size"] for stats in contributors.values()]
        if commit_sizes:
            avg_size = sum(commit_sizes) / len(commit_sizes)
            for author, stats in contributors.items():
                if stats["avg_commit_size"] > avg_size * 3:
                    bottlenecks.append(
                        {
                            "type": "Oversized Commits",
                            "contributor": author,
                            "impact": f"Commits 3x larger than team average",
                            "severity": "Medium",
                            "risk": "Large commits are hard to review and increase bug risk",
                        }
                    )

        return bottlenecks

    def _check_communication(self) -> List[Dict[str, str]]:
        """Check for communication issues in commit messages."""
        issues = []

        try:
            commits = list(self.repo.iter_commits("HEAD", max_count=200))

            # Analyze commit messages
            short_messages = 0
            vague_messages = 0

            for commit in commits:
                message = commit.message.strip()
                first_line = message.split("\n")[0]

                # Check for too-short messages
                if len(first_line) < 10:
                    short_messages += 1

                # Check for vague messages
                vague_keywords = ["fix", "update", "change", "misc", "stuff", "things"]
                if any(keyword == first_line.lower() for keyword in vague_keywords):
                    vague_messages += 1

            # Report issues
            if short_messages > len(commits) * 0.3:
                issues.append(
                    {
                        "issue": "Poor Commit Messages",
                        "description": f"{short_messages} commits have very short messages",
                        "impact": "Makes code archaeology and debugging harder",
                        "recommendation": "Enforce commit message guidelines (e.g., Conventional Commits)",
                    }
                )

            if vague_messages > len(commits) * 0.2:
                issues.append(
                    {
                        "issue": "Vague Commit Messages",
                        "description": f"{vague_messages} commits use generic words like 'fix' or 'update'",
                        "impact": "Reduces commit history usefulness",
                        "recommendation": "Be specific: 'Fix login timeout bug' not 'fix stuff'",
                    }
                )

        except Exception:
            pass

        return issues

    def _calculate_collaboration_score(self, results: Dict) -> int:
        """Calculate overall collaboration health score (0-100)."""
        score = 100

        # Penalize for bottlenecks
        bottlenecks = results.get("bottlenecks", [])
        high_severity = [b for b in bottlenecks if b.get("severity") == "High"]
        score -= len(high_severity) * 20
        score -= len(bottlenecks) * 5

        # Penalize for communication issues
        comm_issues = results.get("communication_issues", [])
        score -= len(comm_issues) * 10

        # Reward for good contributor distribution
        patterns = results.get("commit_patterns", {})
        distribution = patterns.get("contribution_distribution", {})
        if distribution:
            # Good if no one has > 50%
            if all(pct < 50 for pct in distribution.values()):
                score += 10

        return max(0, min(100, score))

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate recommendations for improving team health."""
        recommendations = []

        score = results["collaboration_score"]

        # Overall status
        if score >= 80:
            recommendations.append("✅ Team collaboration health is excellent")
        elif score >= 60:
            recommendations.append("🟡 Team collaboration is good but could improve")
        else:
            recommendations.append("🔴 Team collaboration needs attention")

        # Specific recommendations
        bottlenecks = results.get("bottlenecks", [])
        for bottleneck in bottlenecks:
            if bottleneck["type"] == "Single Contributor Dominance":
                recommendations.append(
                    "👥 Encourage knowledge sharing and pair programming to reduce bus factor"
                )
            elif bottleneck["type"] == "Declining Activity":
                recommendations.append(
                    f"📉 Check in with {bottleneck['contributor']} - may need support or be leaving"
                )
            elif bottleneck["type"] == "Oversized Commits":
                recommendations.append(
                    "✂️ Encourage smaller, more frequent commits for better reviewability"
                )

        # Communication recommendations
        comm_issues = results.get("communication_issues", [])
        if comm_issues:
            recommendations.append(
                "💬 Implement commit message guidelines (consider pre-commit hooks)"
            )

        return recommendations

    def compare_contributors(self, contributor1: str, contributor2: str) -> Dict[str, Any]:
        """
        Compare two contributors' patterns.

        Args:
            contributor1: First contributor name
            contributor2: Second contributor name

        Returns:
            Comparison metrics
        """
        patterns = self._analyze_commit_patterns()
        contributors = patterns.get("contributors", {})

        if contributor1 not in contributors or contributor2 not in contributors:
            return {"error": "One or both contributors not found"}

        stats1 = contributors[contributor1]
        stats2 = contributors[contributor2]

        return {
            "contributor_1": contributor1,
            "contributor_2": contributor2,
            "comparison": {
                "commits": {
                    contributor1: stats1["total_commits"],
                    contributor2: stats2["total_commits"],
                    "difference": abs(stats1["total_commits"] - stats2["total_commits"]),
                },
                "activity_rate": {
                    contributor1: stats1["commits_per_week"],
                    contributor2: stats2["commits_per_week"],
                },
                "commit_size": {
                    contributor1: stats1["avg_commit_size"],
                    contributor2: stats2["avg_commit_size"],
                },
            },
            "insights": self._get_comparison_insights(stats1, stats2, contributor1, contributor2),
        }

    def _get_comparison_insights(
        self, stats1: Dict, stats2: Dict, name1: str, name2: str
    ) -> List[str]:
        """Generate insights from contributor comparison."""
        insights = []

        # Compare activity
        if stats1["commits_per_week"] > stats2["commits_per_week"] * 2:
            insights.append(f"{name1} is significantly more active than {name2}")
        elif stats2["commits_per_week"] > stats1["commits_per_week"] * 2:
            insights.append(f"{name2} is significantly more active than {name1}")
        else:
            insights.append("Both contributors have similar activity levels")

        # Compare commit sizes
        if stats1["avg_commit_size"] > stats2["avg_commit_size"] * 2:
            insights.append(f"{name1} makes larger commits - may benefit from breaking them down")
        elif stats2["avg_commit_size"] > stats1["avg_commit_size"] * 2:
            insights.append(f"{name2} makes larger commits - may benefit from breaking them down")

        return insights
