"""
AI Code Review Tutor - Educational Code Reviews

Provides teaching-focused code reviews with explanations and interactive quizzes.
Helps developers learn WHY issues matter, not just WHAT to fix.
"""

import ast
import random
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class ReviewTutor:
    """Educational code review system."""

    def __init__(self, repo_path: Path):
        """Initialize Review Tutor."""
        self.repo_path = repo_path

    def conduct_review(self, file_path: str, teach_mode: bool = True) -> Dict[str, Any]:
        """
        Conduct educational code review.

        Args:
            file_path: Path to file relative to repo root
            teach_mode: If True, include explanations and quizzes

        Returns:
            Dictionary with review findings and lessons
        """
        results = {
            "findings": [],
            "lessons": [],
            "quiz": [],
            "learning_resources": [],
        }

        try:
            full_path = self.repo_path / file_path
            if not full_path.exists():
                return {"error": f"File not found: {file_path}"}

            content = full_path.read_text(encoding="utf-8", errors="ignore")

            # Analyze code
            findings = self._analyze_code(content, full_path)
            results["findings"] = findings

            # Generate lessons if teach mode
            if teach_mode:
                results["lessons"] = self._generate_lessons(findings)
                results["quiz"] = self._generate_quiz(findings)
                results["learning_resources"] = self._get_resources(findings)

        except Exception as e:
            results["error"] = f"Review failed: {str(e)}"

        return results

    def _analyze_code(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze code and return findings with educational context."""
        findings = []

        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                # Check for mutable default arguments
                if isinstance(node, ast.FunctionDef):
                    for default in node.args.defaults:
                        if isinstance(default, (ast.List, ast.Dict)):
                            findings.append(
                                {
                                    "issue": "Mutable Default Argument",
                                    "line": node.lineno,
                                    "function": node.name,
                                    "severity": "Medium",
                                    "explanation": (
                                        "Using mutable objects (list, dict) as default arguments is dangerous "
                                        "because Python evaluates defaults ONCE when the function is defined, "
                                        "not each time it's called. This means all calls share the same object!"
                                    ),
                                    "example_bug": (
                                        "def add_item(item, items=[]):\\n"
                                        "    items.append(item)\\n"
                                        "    return items\\n\\n"
                                        "add_item(1)  # [1]\\n"
                                        "add_item(2)  # [1, 2] <- Oops! Expected [2]"
                                    ),
                                    "fix": "Use None as default, then create new list: if items is None: items = []",
                                }
                            )

                # Check for bare except
                if isinstance(node, ast.ExceptHandler):
                    if node.type is None:  # bare except:
                        findings.append(
                            {
                                "issue": "Bare Except Clause",
                                "line": node.lineno,
                                "severity": "Medium",
                                "explanation": (
                                    "Bare 'except:' catches ALL exceptions, including SystemExit and KeyboardInterrupt. "
                                    "This can make your program impossible to stop and hide real bugs!"
                                ),
                                "why_it_matters": (
                                    "You might catch exceptions you didn't intend to, making debugging extremely difficult. "
                                    "Always specify which exceptions you're handling."
                                ),
                                "fix": "Use 'except Exception:' or specific exceptions like 'except ValueError:'",
                            }
                        )

                # Check for string concatenation in loops
                if isinstance(node, (ast.For, ast.While)):
                    for child in ast.walk(node):
                        if isinstance(child, ast.AugAssign) and isinstance(child.op, ast.Add):
                            if isinstance(child.target, ast.Name):
                                findings.append(
                                    {
                                        "issue": "String Concatenation in Loop",
                                        "line": node.lineno if hasattr(node, "lineno") else 0,
                                        "severity": "Low",
                                        "explanation": (
                                            "Strings are immutable in Python. Each += creates a NEW string and copies "
                                            "all the old data. In a loop, this is O(n²) complexity!"
                                        ),
                                        "performance_impact": (
                                            "For 1000 iterations, you're copying ~500,000 characters total instead of 1000. "
                                            "Use list.append() then ''.join(list) for O(n) complexity."
                                        ),
                                        "fix": "items = []; items.append(x); result = ''.join(items)",
                                    }
                                )

        except SyntaxError:
            pass

        return findings

    def _generate_lessons(self, findings: List[Dict]) -> List[Dict[str, str]]:
        """Generate educational lessons from findings."""
        lessons = []

        for finding in findings:
            lesson = {
                "topic": finding["issue"],
                "key_concept": finding.get("explanation", ""),
                "why_it_matters": finding.get(
                    "why_it_matters", finding.get("performance_impact", "")
                ),
                "best_practice": finding.get("fix", ""),
            }
            lessons.append(lesson)

        return lessons

    def _generate_quiz(self, findings: List[Dict]) -> List[Dict[str, Any]]:
        """Generate interactive quiz questions."""
        quiz = []

        # Quiz templates based on common issues
        quiz_templates = {
            "Mutable Default Argument": {
                "question": "What will this code output?\\n\\ndef add(x, lst=[]):\\n    lst.append(x)\\n    return lst\\n\\nprint(add(1))\\nprint(add(2))",
                "options": [
                    "A) [1]\\n[2]",
                    "B) [1]\\n[1, 2]",
                    "C) [2]\\n[2]",
                    "D) Error",
                ],
                "correct": "B",
                "explanation": "The list [] is created ONCE when the function is defined. Both calls share the same list object.",
            },
            "Bare Except Clause": {
                "question": "Why is 'except:' dangerous?",
                "options": [
                    "A) It's slower than specific exceptions",
                    "B) It catches KeyboardInterrupt and SystemExit",
                    "C) It doesn't catch any exceptions",
                    "D) It only works in Python 2",
                ],
                "correct": "B",
                "explanation": "Bare except catches ALL exceptions, including system exceptions that should propagate.",
            },
            "String Concatenation in Loop": {
                "question": "What's the time complexity of string concatenation in a loop of n iterations?",
                "options": [
                    "A) O(n)",
                    "B) O(n log n)",
                    "C) O(n²)",
                    "D) O(1)",
                ],
                "correct": "C",
                "explanation": "Each concatenation copies the entire string. Total: 1+2+3+...+n = O(n²) operations.",
            },
        }

        # Create quiz from findings
        for finding in findings[:3]:  # Limit to 3 questions
            issue_type = finding["issue"]
            if issue_type in quiz_templates:
                quiz.append(quiz_templates[issue_type])

        return quiz

    def _get_resources(self, findings: List[Dict]) -> List[Dict[str, str]]:
        """Get learning resources for issues found."""
        resources = []

        resource_map = {
            "Mutable Default Argument": {
                "title": "Python Common Gotchas - Default Arguments",
                "url": "https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments",
                "type": "Article",
            },
            "Bare Except Clause": {
                "title": "PEP 8 - Exception Handling",
                "url": "https://pep8.org/#programming-recommendations",
                "type": "Official Guide",
            },
            "String Concatenation in Loop": {
                "title": "Python Performance Tips",
                "url": "https://wiki.python.org/moin/PythonSpeed/PerformanceTips",
                "type": "Wiki",
            },
        }

        seen_issues = set()
        for finding in findings:
            issue_type = finding["issue"]
            if issue_type in resource_map and issue_type not in seen_issues:
                resources.append(resource_map[issue_type])
                seen_issues.add(issue_type)

        return resources

    def explain_concept(self, concept: str) -> Dict[str, str]:
        """
        Provide detailed explanation of a coding concept.

        Args:
            concept: Concept to explain (e.g., 'mutable-defaults', 'complexity', 'race-condition')

        Returns:
            Dictionary with explanation and examples
        """
        explanations = {
            "mutable-defaults": {
                "title": "Mutable Default Arguments",
                "simple": "Don't use [] or {} as default argument values",
                "detailed": (
                    "When Python sees 'def func(x=[]):', it creates the list ONCE when "
                    "defining the function. Every call to func() shares the same list object. "
                    "This means changes persist across calls, causing confusing bugs."
                ),
                "analogy": (
                    "It's like having one shared shopping cart for all customers. "
                    "Each customer adds items, but they're all going to the same cart!"
                ),
                "correct_way": (
                    "def func(x=None):\\n"
                    "    if x is None:\\n"
                    "        x = []\\n"
                    "    # Now each call gets its own list"
                ),
            },
            "complexity": {
                "title": "Time Complexity",
                "simple": "How runtime grows as data size increases",
                "detailed": (
                    "O(n) = linear: double the data, double the time\\n"
                    "O(n²) = quadratic: double the data, 4x the time\\n"
                    "O(log n) = logarithmic: double the data, slightly more time"
                ),
                "example": (
                    "Searching a sorted list: O(log n) with binary search\\n"
                    "Nested loops over list: O(n²)\\n"
                    "Simple loop: O(n)"
                ),
            },
            "race-condition": {
                "title": "Race Conditions",
                "simple": "When multiple threads access shared data without coordination",
                "detailed": (
                    "Thread A reads value (100), adds 1 (101)\\n"
                    "Thread B reads value (100), adds 1 (101)\\n"
                    "Thread A writes 101\\n"
                    "Thread B writes 101\\n"
                    "Result: 101 instead of 102! One increment lost."
                ),
                "fix": "Use locks, atomic operations, or queue-based communication",
            },
        }

        return explanations.get(
            concept,
            {
                "title": "Concept not found",
                "simple": "Try: mutable-defaults, complexity, race-condition",
            },
        )
