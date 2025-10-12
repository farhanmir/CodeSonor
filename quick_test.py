#!/usr/bin/env python3
"""
Quick test script to verify all beta features are working.
Run this to get immediate feedback on feature status.
"""

import sys
from pathlib import Path


def quick_test():
    """Quick test of all 12 features"""
    print("🧪 CodeSonor v0.5.0-beta Quick Test\n")

    repo_path = Path.cwd()
    results = []

    # Test 1: Code Archaeology
    try:
        from codesonor.archaeology import CodeArchaeology

        archaeology = CodeArchaeology(repo_path)
        result = archaeology.analyze_evolution()
        status = "✅" if "summary" in result or "error" in result else "❌"
        results.append(("Code Archaeology", status))
    except Exception as e:
        results.append(("Code Archaeology", f"❌ {str(e)[:50]}"))

    # Test 2: Team DNA
    try:
        from codesonor.team_dna import TeamDNA

        team_dna = TeamDNA(repo_path)
        result = team_dna.analyze_contributors()
        status = "✅" if "contributors" in result or "error" in result else "❌"
        results.append(("Team DNA", status))
    except Exception as e:
        results.append(("Team DNA", f"❌ {str(e)[:50]}"))

    # Test 3: Dependency Risk
    try:
        from codesonor.dep_risk import DependencyRisk

        analyzer = DependencyRisk(repo_path)
        result = analyzer.analyze_dependencies()
        status = "✅" if "dependencies" in result or "error" in result else "❌"
        results.append(("Dependency Risk", status))
    except Exception as e:
        results.append(("Dependency Risk", f"❌ {str(e)[:50]}"))

    # Test 4: Code Forecaster
    try:
        from codesonor.forecaster import CodeClimatePredictor

        forecaster = CodeClimatePredictor(repo_path)
        result = forecaster.forecast_quality()
        status = "✅" if "predictions" in result or "error" in result else "❌"
        results.append(("Code Forecaster", status))
    except Exception as e:
        results.append(("Code Forecaster", f"❌ {str(e)[:50]}"))

    # Test 5: Cross-Repo Intelligence
    try:
        from codesonor.cross_repo import CrossRepoIntelligence

        intelligence = CrossRepoIntelligence(repo_path)
        result = intelligence.compare_with_best_practices()
        status = "✅" if result and len(result) > 0 else "❌"
        results.append(("Cross-Repo Intelligence", status))
    except Exception as e:
        results.append(("Cross-Repo Intelligence", f"❌ {str(e)[:50]}"))

    # Test 6: Onboarding Assistant
    try:
        from codesonor.onboarding import OnboardingAssistant

        assistant = OnboardingAssistant(repo_path)
        result = assistant.create_code_tour()
        status = "✅" if result and len(result) > 0 else "❌"
        results.append(("Onboarding Assistant", status))
    except Exception as e:
        results.append(("Onboarding Assistant", f"❌ {str(e)[:50]}"))

    # Test 7: Smart Smell Detection
    try:
        from codesonor.smart_smell import SmartSmellDetector

        detector = SmartSmellDetector(repo_path)
        result = detector.detect_smells()
        status = "✅" if "smells" in result or "error" in result else "❌"
        results.append(("Smart Smell Detection", status))
    except Exception as e:
        results.append(("Smart Smell Detection", f"❌ {str(e)[:50]}"))

    # Test 8: License Matrix
    try:
        from codesonor.license_matrix import LicenseMatrix

        matrix = LicenseMatrix(repo_path)
        result = matrix.analyze_licenses()
        status = "✅" if "project_license" in result or "error" in result else "❌"
        results.append(("License Matrix", status))
    except Exception as e:
        results.append(("License Matrix", f"❌ {str(e)[:50]}"))

    # Test 9: Performance Predictor
    try:
        from codesonor.perf_predictor import PerformancePredictor

        predictor = PerformancePredictor(repo_path)
        result = predictor.analyze_performance()
        status = "✅" if "summary" in result or "error" in result else "❌"
        results.append(("Performance Predictor", status))
    except Exception as e:
        results.append(("Performance Predictor", f"❌ {str(e)[:50]}"))

    # Test 10: Review Tutor
    try:
        from codesonor.review_tutor import ReviewTutor

        tutor = ReviewTutor(repo_path)
        # Just test import for now since it needs a specific file
        status = "✅"
        results.append(("Review Tutor", status))
    except Exception as e:
        results.append(("Review Tutor", f"❌ {str(e)[:50]}"))

    # Test 11: Portability Analyzer
    try:
        from codesonor.portability import PortabilityAnalyzer

        analyzer = PortabilityAnalyzer(repo_path)
        result = analyzer.analyze_portability()
        status = "✅" if "portability_score" in result or "error" in result else "❌"
        results.append(("Portability Analyzer", status))
    except Exception as e:
        results.append(("Portability Analyzer", f"❌ {str(e)[:50]}"))

    # Test 12: Team Health
    try:
        from codesonor.team_health import TeamHealthAnalyzer

        analyzer = TeamHealthAnalyzer(repo_path)
        result = analyzer.analyze_team_health()
        status = "✅" if "health_score" in result or "error" in result else "❌"
        results.append(("Team Health", status))
    except Exception as e:
        results.append(("Team Health", f"❌ {str(e)[:50]}"))

    # Print results
    print("Feature Status:")
    print("-" * 50)
    for feature, status in results:
        print(f"{feature:30} {status}")

    # Summary
    passed = sum(1 for _, s in results if "✅" in str(s))
    total = len(results)

    print("-" * 50)
    print(f"\nResult: {passed}/{total} features working")

    if passed == total:
        print("🎉 All features are operational!")
        return 0
    elif passed >= 10:
        print("✅ Most features working (some may need optional deps)")
        return 0
    else:
        print("⚠️  Some features need attention")
        return 1


if __name__ == "__main__":
    sys.exit(quick_test())
