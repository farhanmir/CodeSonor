"""
Onboarding Assistant - New Developer Guidance

Generates personalized learning paths for new contributors.
Creates interactive guides and identifies critical code paths.
"""

import ast
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class OnboardingAssistant:
    """Generate learning paths for new developers."""

    def __init__(self, repo_path: Path):
        """
        Initialize Onboarding Assistant.

        Args:
            repo_path: Path to the repository
        """
        self.repo_path = repo_path

    def generate_learning_path(
        self, role: str = "backend", experience: str = "intermediate"
    ) -> Dict[str, Any]:
        """
        Generate personalized onboarding path.

        Args:
            role: Developer role (backend, frontend, fullstack, devops)
            experience: Experience level (junior, intermediate, senior)

        Returns:
            Dictionary with learning path and recommendations
        """
        results = {
            "learning_path": [],
            "key_files": [],
            "critical_concepts": [],
            "estimated_time": "Unknown",
        }

        try:
            # Analyze repository structure
            structure = self._analyze_structure()

            # Generate day-by-day learning path
            results["learning_path"] = self._create_learning_path(structure, role, experience)

            # Identify key files to understand
            results["key_files"] = self._identify_key_files(structure, role)

            # Extract critical concepts
            results["critical_concepts"] = self._extract_concepts(structure)

            # Estimate onboarding time
            results["estimated_time"] = self._estimate_time(structure, experience)

        except Exception as e:
            results["error"] = f"Generation failed: {str(e)}"

        return results

    def _analyze_structure(self) -> Dict[str, Any]:
        """Analyze repository structure."""
        structure = {
            "entry_points": [],
            "config_files": [],
            "core_modules": [],
            "test_files": [],
            "total_files": 0,
        }

        # Find entry points
        entry_patterns = ["main.py", "app.py", "server.py", "index.js", "main.js"]
        for pattern in entry_patterns:
            matches = list(self.repo_path.rglob(pattern))
            structure["entry_points"].extend([str(m.relative_to(self.repo_path)) for m in matches])

        # Find config files
        config_patterns = ["*.config.js", "*.config.py", "config.py", "settings.py", ".env*"]
        for pattern in config_patterns:
            matches = list(self.repo_path.rglob(pattern))
            structure["config_files"].extend(
                [str(m.relative_to(self.repo_path)) for m in matches[:5]]
            )

        # Find test files
        test_dirs = ["tests", "test", "__tests__"]
        for test_dir in test_dirs:
            test_path = self.repo_path / test_dir
            if test_path.is_dir():
                test_files = list(test_path.rglob("*.py")) + list(test_path.rglob("*.js"))
                structure["test_files"].extend(
                    [str(f.relative_to(self.repo_path)) for f in test_files[:10]]
                )

        # Count total code files
        code_files = list(self.repo_path.rglob("*.py")) + list(self.repo_path.rglob("*.js"))
        structure["total_files"] = len(
            [f for f in code_files if "node_modules" not in str(f) and "venv" not in str(f)]
        )

        return structure

    def _create_learning_path(
        self, structure: Dict, role: str, experience: str
    ) -> List[Dict[str, Any]]:
        """Create day-by-day learning path."""
        path = []

        # Day 1: Setup and overview
        path.append(
            {
                "day": 1,
                "title": "🚀 Setup & Repository Overview",
                "tasks": [
                    "Clone repository and set up development environment",
                    "Read README.md and CONTRIBUTING.md thoroughly",
                    "Run the application locally",
                    "Explore project structure and folder organization",
                ],
                "files_to_read": ["README.md"] + structure["config_files"][:2],
            }
        )

        # Day 2: Entry points and core flow
        path.append(
            {
                "day": 2,
                "title": "🎯 Understanding Core Flow",
                "tasks": [
                    "Study entry point files to understand how app starts",
                    "Trace a simple request/operation through the codebase",
                    "Identify main modules and their responsibilities",
                    "Create a mental map of code flow",
                ],
                "files_to_read": structure["entry_points"] + ["Core modules"],
            }
        )

        # Day 3: Testing
        path.append(
            {
                "day": 3,
                "title": "🧪 Testing & Code Quality",
                "tasks": [
                    "Run existing test suite",
                    "Understand testing framework and patterns used",
                    "Write a simple test for a utility function",
                    "Learn the deployment process",
                ],
                "files_to_read": structure["test_files"][:3],
            }
        )

        # Day 4-5: Deep dive based on role
        if role == "backend":
            path.append(
                {
                    "day": 4,
                    "title": "🔧 Backend Deep Dive",
                    "tasks": [
                        "Study database models and schema",
                        "Understand API endpoints and routing",
                        "Learn authentication/authorization flow",
                        "Review error handling patterns",
                    ],
                }
            )
        elif role == "frontend":
            path.append(
                {
                    "day": 4,
                    "title": "🎨 Frontend Deep Dive",
                    "tasks": [
                        "Study component structure",
                        "Understand state management approach",
                        "Learn routing and navigation",
                        "Review styling methodology",
                    ],
                }
            )

        # Day 5: First contribution
        path.append(
            {
                "day": 5,
                "title": "✨ First Contribution",
                "tasks": [
                    "Pick a 'good first issue' or small bug",
                    "Make your first code change",
                    "Write tests for your change",
                    "Submit a pull request",
                ],
            }
        )

        return path

    def _identify_key_files(self, structure: Dict, role: str) -> List[Dict[str, str]]:
        """Identify must-read files for the role."""
        key_files = []

        # Universal key files
        if structure["entry_points"]:
            key_files.append(
                {
                    "file": structure["entry_points"][0],
                    "importance": "Critical",
                    "reason": "Entry point - shows how application starts",
                }
            )

        # Add config files
        if structure["config_files"]:
            key_files.append(
                {
                    "file": structure["config_files"][0],
                    "importance": "High",
                    "reason": "Configuration - understand app settings",
                }
            )

        # Role-specific files
        if role == "backend":
            # Look for models, database, API files
            backend_patterns = ["models.py", "database.py", "api.py", "routes.py"]
            for pattern in backend_patterns:
                matches = list(self.repo_path.rglob(pattern))
                if matches:
                    key_files.append(
                        {
                            "file": str(matches[0].relative_to(self.repo_path)),
                            "importance": "High",
                            "reason": f"Core backend logic - {pattern}",
                        }
                    )

        return key_files[:10]

    def _extract_concepts(self, structure: Dict) -> List[str]:
        """Extract critical concepts from codebase."""
        concepts = []

        # Detect frameworks/technologies from file patterns
        if any("package.json" in str(f) for f in self.repo_path.rglob("package.json")):
            concepts.append("📦 Node.js/JavaScript ecosystem")

        if any("requirements.txt" in str(f) for f in self.repo_path.rglob("requirements.txt")):
            concepts.append("🐍 Python ecosystem")

        if any("docker" in str(f).lower() for f in self.repo_path.rglob("*")):
            concepts.append("🐳 Docker containerization")

        if (self.repo_path / ".github" / "workflows").is_dir():
            concepts.append("⚙️ GitHub Actions CI/CD")

        # Add generic concepts
        concepts.extend(
            [
                "🔒 Authentication & Authorization",
                "📊 Error Handling & Logging",
                "🧪 Testing Strategies",
                "📁 Project Architecture Patterns",
            ]
        )

        return concepts[:8]

    def _estimate_time(self, structure: Dict, experience: str) -> str:
        """Estimate onboarding time based on complexity."""
        base_days = 5

        # Adjust for codebase size
        if structure["total_files"] > 100:
            base_days += 3
        elif structure["total_files"] > 50:
            base_days += 2

        # Adjust for experience
        if experience == "junior":
            base_days = int(base_days * 1.5)
        elif experience == "senior":
            base_days = int(base_days * 0.7)

        return f"{base_days} days for basic proficiency, {base_days * 2} days for full productivity"

    def create_code_tour(self) -> Dict[str, Any]:
        """Create an interactive tour of the codebase."""
        tour = {
            "stops": [],
            "total_duration": "30-45 minutes",
        }

        # Find interesting files to tour
        interesting_files = []

        # Entry point
        for pattern in ["main.py", "app.py", "index.js"]:
            matches = list(self.repo_path.rglob(pattern))
            if matches:
                interesting_files.append((matches[0], "Entry point - where it all begins"))
                break

        # Core logic
        for pattern in ["core.py", "engine.py", "controller.py"]:
            matches = list(self.repo_path.rglob(pattern))
            if matches:
                interesting_files.append((matches[0], "Core logic - the heart of the application"))
                break

        # Create tour stops
        for i, (file_path, description) in enumerate(interesting_files, 1):
            tour["stops"].append(
                {
                    "stop": i,
                    "file": str(file_path.relative_to(self.repo_path)),
                    "description": description,
                    "estimated_time": "5-10 minutes",
                }
            )

        return tour
