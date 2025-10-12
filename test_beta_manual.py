"""
Manual testing script for all 12 v0.5.0-beta features.
Run this locally to test features against real GitHub repositories.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Test repositories - real, well-known projects
TEST_REPOS = {
    "small_python": {
        "url": "https://github.com/psf/requests",
        "description": "Popular HTTP library",
        "size": "small",
    },
    "medium_python": {
        "url": "https://github.com/pallets/flask",
        "description": "Web framework",
        "size": "medium",
    },
    "large_python": {
        "url": "https://github.com/django/django",
        "description": "Large web framework",
        "size": "large",
    },
    "ml_project": {
        "url": "https://github.com/scikit-learn/scikit-learn",
        "description": "Machine learning library",
        "size": "large",
    },
}


def print_header(text):
    """Print a formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def print_result(feature, status, details=""):
    """Print test result"""
    emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"{emoji} {feature:30} {status:10} {details}")


def clone_repo(url, target_dir):
    """Clone a git repository"""
    print(f"📥 Cloning {url}...")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "100", url, target_dir],
            capture_output=True,
            check=True,
            timeout=300,
        )
        return True
    except Exception as e:
        print(f"❌ Failed to clone: {e}")
        return False


def test_archaeology(repo_path):
    """Test Code Archaeology feature"""
    try:
        from codesonor.archaeology import CodeArchaeology

        archaeology = CodeArchaeology(repo_path)
        result = archaeology.analyze_evolution()

        if "error" in result:
            return "FAIL", result["error"]

        summary = result.get("summary", {})
        commits = summary.get("total_commits", 0)
        hotspots = len(result.get("hotspots", []))

        return "PASS", f"Commits: {commits}, Hotspots: {hotspots}"
    except Exception as e:
        return "FAIL", str(e)


def test_team_dna(repo_path):
    """Test Team DNA feature"""
    try:
        from codesonor.team_dna import TeamDNA

        team_dna = TeamDNA(repo_path)
        result = team_dna.analyze_contributors()

        if "error" in result:
            return "FAIL", result["error"]

        contributors = len(result.get("contributors", {}))

        return "PASS", f"Contributors: {contributors}"
    except Exception as e:
        return "FAIL", str(e)


def test_dep_risk(repo_path):
    """Test Dependency Risk Score feature"""
    try:
        from codesonor.dep_risk import DependencyRisk

        analyzer = DependencyRisk(repo_path)
        result = analyzer.analyze_dependencies()

        if "error" in result:
            return "WARN", result["error"]

        deps = len(result.get("dependencies", []))
        avg_risk = result.get("summary", {}).get("average_risk", 0)

        return "PASS", f"Dependencies: {deps}, Avg Risk: {avg_risk:.1f}"
    except Exception as e:
        return "FAIL", str(e)


def test_forecaster(repo_path):
    """Test Code Climate Prediction feature"""
    try:
        from codesonor.forecaster import CodeClimatePredictor

        forecaster = CodeClimatePredictor(repo_path)
        result = forecaster.forecast_quality()

        if "error" in result:
            return "WARN", result["error"]

        predictions = len(result.get("predictions", {}))

        return "PASS", f"Predictions made: {predictions}"
    except Exception as e:
        return "FAIL", str(e)


def test_cross_repo(repo_path):
    """Test Cross-Repo Intelligence feature"""
    try:
        from codesonor.cross_repo import CrossRepoIntelligence

        intelligence = CrossRepoIntelligence(repo_path)
        result = intelligence.compare_with_best_practices(language="Python", topic="web")

        if "error" in result:
            return "WARN", result["error"]

        similar = len(result.get("similar_projects", []))

        return "PASS", f"Similar projects: {similar}"
    except Exception as e:
        return "FAIL", str(e)


def test_onboarding(repo_path):
    """Test Onboarding Assistant feature"""
    try:
        from codesonor.onboarding import OnboardingAssistant

        assistant = OnboardingAssistant(repo_path)
        result = assistant.create_code_tour()

        if "error" in result:
            return "FAIL", result["error"]

        critical_files = len(result.get("critical_files", []))
        days = len(result.get("learning_path", []))

        return "PASS", f"Critical files: {critical_files}, Days: {days}"
    except Exception as e:
        return "FAIL", str(e)


def test_smart_smell(repo_path):
    """Test Smart Code Smell Detection feature"""
    try:
        from codesonor.smart_smell import SmartSmellDetector

        detector = SmartSmellDetector(repo_path)
        result = detector.detect_smells()

        if "error" in result:
            return "FAIL", result["error"]

        smells = len(result.get("smells", []))
        critical = sum(1 for s in result.get("smells", []) if s.get("severity") == "critical")

        return "PASS", f"Smells: {smells}, Critical: {critical}"
    except Exception as e:
        return "FAIL", str(e)


def test_license_matrix(repo_path):
    """Test License Compatibility Matrix feature"""
    try:
        from codesonor.license_matrix import LicenseMatrix

        matrix = LicenseMatrix(repo_path)
        result = matrix.analyze_licenses()

        if "error" in result:
            return "WARN", result["error"]

        conflicts = len(result.get("conflicts", []))

        return (
            "PASS",
            f"License: {result.get('project_license', 'Unknown')}, Conflicts: {conflicts}",
        )
    except Exception as e:
        return "FAIL", str(e)


def test_perf_predictor(repo_path):
    """Test Performance Prediction feature"""
    try:
        from codesonor.perf_predictor import PerformancePredictor

        predictor = PerformancePredictor(repo_path)
        result = predictor.analyze_performance()

        if "error" in result:
            return "FAIL", result["error"]

        bottlenecks = len(result.get("bottlenecks", []))
        critical = sum(1 for b in result.get("bottlenecks", []) if b.get("severity") == "high")

        return "PASS", f"Bottlenecks: {bottlenecks}, Critical: {critical}"
    except Exception as e:
        return "FAIL", str(e)


def test_review_tutor(repo_path):
    """Test AI Code Review Tutor feature"""
    try:
        from codesonor.review_tutor import ReviewTutor

        tutor = ReviewTutor(repo_path)
        result = tutor.conduct_review(str(repo_path / "src"))

        if "error" in result:
            return "FAIL", result["error"]

        reviews = len(result.get("reviews", []))

        return "PASS", f"Reviews: {reviews}"
    except Exception as e:
        return "FAIL", str(e)


def test_portability(repo_path):
    """Test Code Portability Score feature"""
    try:
        from codesonor.portability import PortabilityAnalyzer

        analyzer = PortabilityAnalyzer(repo_path)
        result = analyzer.analyze_portability()

        if "error" in result:
            return "FAIL", result["error"]

        score = result.get("portability_score", 0)
        frameworks = len(result.get("frameworks", []))

        return "PASS", f"Score: {score}, Frameworks: {frameworks}"
    except Exception as e:
        return "FAIL", str(e)


def test_team_health(repo_path):
    """Test Team Health Insights feature"""
    try:
        from codesonor.team_health import TeamHealthAnalyzer

        analyzer = TeamHealthAnalyzer(repo_path)
        result = analyzer.analyze_team_health()

        if "error" in result:
            return "FAIL", result["error"]

        health_score = result.get("health_score", 0)
        bottlenecks = len(result.get("bottlenecks", []))

        return "PASS", f"Health Score: {health_score}, Bottlenecks: {bottlenecks}"
    except Exception as e:
        return "FAIL", str(e)


def run_all_tests(repo_path, repo_name):
    """Run all 12 feature tests on a repository"""
    print_header(f"Testing on: {repo_name}")

    tests = [
        ("🏛️  Code Archaeology", test_archaeology),
        ("🧬 Team DNA", test_team_dna),
        ("⚠️  Dependency Risk Score", test_dep_risk),
        ("🔮 Code Climate Prediction", test_forecaster),
        ("🌐 Cross-Repo Intelligence", test_cross_repo),
        ("🎓 Onboarding Assistant", test_onboarding),
        ("👃 Smart Code Smell Detection", test_smart_smell),
        ("⚖️  License Compatibility Matrix", test_license_matrix),
        ("⚡ Performance Prediction", test_perf_predictor),
        ("🎯 AI Code Review Tutor", test_review_tutor),
        ("🔄 Code Portability Score", test_portability),
        ("👥 Team Health Insights", test_team_health),
    ]

    results = {}
    for name, test_func in tests:
        status, details = test_func(repo_path)
        print_result(name, status, details)
        results[name] = {"status": status, "details": details}

    return results


def main():
    """Main testing function"""
    print_header("CodeSonor v0.5.0-beta Feature Testing")

    # Ask user which repo to test
    print("Available test repositories:")
    for i, (key, info) in enumerate(TEST_REPOS.items(), 1):
        print(f"{i}. {key:20} - {info['description']:30} ({info['size']})")
    print(f"{len(TEST_REPOS) + 1}. All repositories (comprehensive)")
    print(f"{len(TEST_REPOS) + 2}. Test on current directory")

    choice = input("\nSelect option (1-{}): ".format(len(TEST_REPOS) + 2))

    all_results = {}

    try:
        choice_num = int(choice)

        if choice_num == len(TEST_REPOS) + 2:
            # Test on current directory
            print_header("Testing on Current Directory")
            results = run_all_tests(Path.cwd(), "Current Directory")
            all_results["current_directory"] = results

        elif choice_num == len(TEST_REPOS) + 1:
            # Test all repositories
            with tempfile.TemporaryDirectory() as tmpdir:
                for repo_key, repo_info in TEST_REPOS.items():
                    repo_dir = Path(tmpdir) / repo_key

                    if clone_repo(repo_info["url"], str(repo_dir)):
                        results = run_all_tests(repo_dir, repo_key)
                        all_results[repo_key] = results
        else:
            # Test single repository
            repo_key = list(TEST_REPOS.keys())[choice_num - 1]
            repo_info = TEST_REPOS[repo_key]

            with tempfile.TemporaryDirectory() as tmpdir:
                repo_dir = Path(tmpdir) / repo_key

                if clone_repo(repo_info["url"], str(repo_dir)):
                    results = run_all_tests(repo_dir, repo_key)
                    all_results[repo_key] = results

    except ValueError:
        print("❌ Invalid choice")
        return 1
    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")
        return 1

    # Generate summary
    print_header("Test Summary")

    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    warned_tests = 0

    for repo_name, results in all_results.items():
        for feature, result in results.items():
            total_tests += 1
            if result["status"] == "PASS":
                passed_tests += 1
            elif result["status"] == "FAIL":
                failed_tests += 1
            else:
                warned_tests += 1

    print(f"Total Tests Run:    {total_tests}")
    print(f"✅ Passed:         {passed_tests}")
    print(f"❌ Failed:         {failed_tests}")
    print(f"⚠️  Warnings:       {warned_tests}")
    print(f"\nSuccess Rate:      {passed_tests/total_tests*100:.1f}%")

    # Save results to JSON
    results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n📄 Results saved to: {results_file}")

    return 0 if failed_tests == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
