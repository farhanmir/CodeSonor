"""
Team DNA - Contributor Behavioral Analysis

Analyzes coding patterns and behavioral signatures of contributors.
Detects anomalies, collaboration patterns, and individual coding styles.
"""

import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

try:
    from git import Repo

    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False


class TeamDNA:
    """Analyzes contributor patterns and team dynamics."""

    def __init__(self, repo_path: Path):
        """
        Initialize Team DNA analyzer.

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

    def analyze_contributors(self, limit: int = 500) -> Dict[str, Any]:
        """
        Analyze all contributors and their coding patterns.

        Args:
            limit: Maximum number of commits to analyze per contributor

        Returns:
            Dictionary with contributor analysis
        """
        if not self.repo:
            return {"error": "Git repository not available or GitPython not installed"}

        results = {
            "contributors": {},
            "team_metrics": {},
            "collaboration_graph": {},
            "anomalies": [],
        }

        try:
            # Get all commits
            commits = list(self.repo.iter_commits("HEAD", max_count=limit * 10))

            # Group commits by author
            author_commits = defaultdict(list)
            for commit in commits:
                author_commits[commit.author.name].append(commit)

            # Analyze each contributor
            for author, author_commits_list in author_commits.items():
                if len(author_commits_list) < 3:  # Skip contributors with very few commits
                    continue

                profile = self._analyze_contributor(author, author_commits_list[:limit])
                results["contributors"][author] = profile

            # Calculate team-wide metrics
            results["team_metrics"] = self._calculate_team_metrics(results["contributors"])

            # Build collaboration graph
            results["collaboration_graph"] = self._build_collaboration_graph(commits)

            # Detect anomalies
            results["anomalies"] = self._detect_anomalies(results["contributors"])

        except Exception as e:
            results["error"] = f"Analysis failed: {str(e)}"

        return results

    def _analyze_contributor(self, author: str, commits: List) -> Dict[str, Any]:
        """Analyze a single contributor's patterns."""
        profile = {
            "name": author,
            "total_commits": len(commits),
            "coding_style": {},
            "work_patterns": {},
            "specialization": {},
            "consistency_score": 0.0,
        }

        # Analyze coding style from diffs
        indentation_style = Counter()
        line_length_avg = []
        comment_density = []
        commit_sizes = []
        file_types = Counter()
        commit_hours = []

        for commit in commits:
            try:
                # Get commit time
                commit_time = datetime.fromtimestamp(commit.committed_date)
                commit_hours.append(commit_time.hour)

                # Analyze commit diff
                if commit.parents:
                    diff = commit.parents[0].diff(commit, create_patch=True)

                    total_lines = 0
                    code_lines = 0
                    comment_lines = 0

                    for change in diff:
                        # Track file types
                        if change.b_path:
                            ext = Path(change.b_path).suffix
                            if ext:
                                file_types[ext] += 1

                        # Analyze diff content
                        if change.diff:
                            diff_text = change.diff.decode("utf-8", errors="ignore")
                            lines = diff_text.split("\n")

                            for line in lines:
                                if line.startswith("+") and not line.startswith("+++"):
                                    total_lines += 1
                                    code_lines += 1

                                    # Detect indentation
                                    if line[1:].startswith("    "):
                                        indentation_style["4-spaces"] += 1
                                    elif line[1:].startswith("  "):
                                        indentation_style["2-spaces"] += 1
                                    elif line[1:].startswith("\t"):
                                        indentation_style["tabs"] += 1

                                    # Track line length
                                    line_length_avg.append(len(line))

                                    # Detect comments
                                    if "#" in line or "//" in line or "/*" in line:
                                        comment_lines += 1

                    if code_lines > 0:
                        comment_density.append(comment_lines / code_lines)
                    commit_sizes.append(total_lines)

            except Exception:
                continue

        # Calculate coding style metrics
        if indentation_style:
            profile["coding_style"]["indentation"] = indentation_style.most_common(1)[0][0]

            # Calculate consistency (percentage of most common style)
            total_indents = sum(indentation_style.values())
            most_common_count = indentation_style.most_common(1)[0][1]
            profile["consistency_score"] = (
                (most_common_count / total_indents * 100) if total_indents > 0 else 0
            )

        if line_length_avg:
            profile["coding_style"]["avg_line_length"] = int(
                sum(line_length_avg) / len(line_length_avg)
            )

        if comment_density:
            avg_comment_density = sum(comment_density) / len(comment_density)
            profile["coding_style"]["comment_density"] = f"{avg_comment_density * 100:.1f}%"

        # Work patterns
        if commit_sizes:
            profile["work_patterns"]["avg_commit_size"] = int(sum(commit_sizes) / len(commit_sizes))
            profile["work_patterns"]["commit_size_variance"] = (
                "High" if max(commit_sizes) > 500 else "Normal"
            )

        if commit_hours:
            avg_hour = sum(commit_hours) / len(commit_hours)
            if 9 <= avg_hour <= 17:
                profile["work_patterns"]["work_time"] = "Business hours"
            elif 18 <= avg_hour <= 23:
                profile["work_patterns"]["work_time"] = "Evening"
            else:
                profile["work_patterns"]["work_time"] = "Late night/Early morning"

        # Specialization (file types)
        if file_types:
            top_types = file_types.most_common(3)
            profile["specialization"]["primary_languages"] = [
                f"{ext} ({count} commits)" for ext, count in top_types
            ]

        return profile

    def _calculate_team_metrics(self, contributors: Dict[str, Dict]) -> Dict[str, Any]:
        """Calculate team-wide metrics."""
        if not contributors:
            return {}

        metrics = {
            "total_contributors": len(contributors),
            "style_diversity": {},
            "collaboration_level": "Unknown",
        }

        # Analyze style diversity
        indentation_styles = Counter()
        for profile in contributors.values():
            style = profile["coding_style"].get("indentation", "unknown")
            indentation_styles[style] += 1

        metrics["style_diversity"]["indentation_styles"] = dict(indentation_styles)

        # Check for style conflicts
        if len(indentation_styles) > 1:
            metrics["style_diversity"]["status"] = "⚠️ Mixed styles detected"
            metrics["style_diversity"]["recommendation"] = "Consider adopting a unified style guide"
        else:
            metrics["style_diversity"]["status"] = "✅ Consistent style across team"

        return metrics

    def _build_collaboration_graph(self, commits: List) -> Dict[str, Any]:
        """Build a graph of who works on what files."""
        file_authors = defaultdict(set)
        author_files = defaultdict(set)

        for commit in commits:
            author = commit.author.name
            try:
                for item in commit.stats.files.keys():
                    file_authors[item].add(author)
                    author_files[author].add(item)
            except Exception:
                continue

        # Find files with multiple authors (collaboration points)
        collaboration_files = {
            file: list(authors) for file, authors in file_authors.items() if len(authors) > 1
        }

        # Find author pairs that frequently collaborate
        collaboration_pairs = Counter()
        for file, authors in collaboration_files.items():
            for i, author1 in enumerate(authors):
                for author2 in authors[i + 1 :]:
                    pair = tuple(sorted([author1, author2]))
                    collaboration_pairs[pair] += 1

        return {
            "total_collaborative_files": len(collaboration_files),
            "top_collaborative_files": sorted(
                [(file, len(authors)) for file, authors in collaboration_files.items()],
                key=lambda x: x[1],
                reverse=True,
            )[:10],
            "frequent_pairs": [
                {"contributors": list(pair), "shared_files": count}
                for pair, count in collaboration_pairs.most_common(10)
            ],
        }

    def _detect_anomalies(self, contributors: Dict[str, Dict]) -> List[Dict[str, Any]]:
        """Detect unusual patterns that might indicate issues."""
        anomalies = []

        # Calculate team averages
        if not contributors:
            return anomalies

        commit_sizes = []
        consistency_scores = []

        for profile in contributors.values():
            if "avg_commit_size" in profile["work_patterns"]:
                commit_sizes.append(profile["work_patterns"]["avg_commit_size"])
            if profile["consistency_score"] > 0:
                consistency_scores.append(profile["consistency_score"])

        avg_commit_size = sum(commit_sizes) / len(commit_sizes) if commit_sizes else 0
        avg_consistency = (
            sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0
        )

        # Detect anomalies
        for name, profile in contributors.items():
            # Unusually large commits
            contributor_size = profile["work_patterns"].get("avg_commit_size", 0)
            if contributor_size > avg_commit_size * 3:
                anomalies.append(
                    {
                        "contributor": name,
                        "type": "Large commits",
                        "description": f"Average commit size ({contributor_size} lines) is 3x team average",
                        "severity": "Medium",
                    }
                )

            # Inconsistent coding style
            if profile["consistency_score"] < 50 and profile["consistency_score"] > 0:
                anomalies.append(
                    {
                        "contributor": name,
                        "type": "Inconsistent style",
                        "description": f"Coding style consistency only {profile['consistency_score']:.1f}%",
                        "severity": "Low",
                    }
                )

        return anomalies

    def get_contributor_profile(self, author_name: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get detailed profile for a specific contributor.

        Args:
            author_name: Name of the contributor
            limit: Number of commits to analyze

        Returns:
            Detailed contributor profile
        """
        if not self.repo:
            return {"error": "Git repository not available"}

        try:
            # Find commits by this author
            commits = [
                c
                for c in self.repo.iter_commits("HEAD", max_count=limit * 10)
                if c.author.name == author_name
            ][:limit]

            if not commits:
                return {"error": f"No commits found for author: {author_name}"}

            return self._analyze_contributor(author_name, commits)

        except Exception as e:
            return {"error": str(e)}
