"""
Auto-fix script for beta-tests.yml workflow file.
Corrects all class names and method calls.
"""

import re

# Read the workflow file
with open(".github/workflows/beta-tests.yml", "r", encoding="utf-8") as f:
    content = f.read()

# Define replacements
replacements = [
    # Fix class imports
    (
        "from codesonor.dep_risk import DependencyRiskAnalyzer",
        "from codesonor.dep_risk import DependencyRisk",
    ),
    (
        "from codesonor.forecaster import CodeForecaster",
        "from codesonor.forecaster import CodeClimatePredictor",
    ),
    # Fix class instantiations
    ("DependencyRiskAnalyzer(", "DependencyRisk("),
    ("CodeForecaster(", "CodeClimatePredictor("),
    # Fix method calls - be specific with context
    ("archaeology.analyze()", "archaeology.analyze_evolution()"),
    ("team_dna.analyze()", "team_dna.analyze_contributors()"),
    ("analyzer.analyze()", "analyzer.analyze_dependencies()"),
    ("forecaster.predict()", "forecaster.forecast_quality()"),
    ("intelligence.analyze(", "intelligence.compare_with_best_practices("),
    ("assistant.generate_plan()", "assistant.create_code_tour()"),
    ("detector.analyze()", "detector.detect_smells()"),
    ("matrix.analyze()", "matrix.analyze_licenses()"),
    ("predictor.analyze()", "predictor.analyze_performance()"),
    ("tutor.review()", "tutor.conduct_review()"),
    (
        "PortabilityAnalyzer(repo_path).analyze()",
        "PortabilityAnalyzer(repo_path).analyze_portability()",
    ),
    (
        "TeamHealthAnalyzer(repo_path).analyze()",
        "TeamHealthAnalyzer(repo_path).analyze_team_health()",
    ),
    ("CodeArchaeology(repo_path).analyze()", "CodeArchaeology(repo_path).analyze_evolution()"),
    ("TeamDNA(repo_path).analyze()", "TeamDNA(repo_path).analyze_contributors()"),
    ("SmartSmellDetector(repo_path).analyze()", "SmartSmellDetector(repo_path).detect_smells()"),
    (
        "PerformancePredictor(repo_path).analyze()",
        "PerformancePredictor(repo_path).analyze_performance()",
    ),
    # Fix in tuples
    ("('dep_risk', 'DependencyRiskAnalyzer')", "('dep_risk', 'DependencyRisk')"),
    ("('forecaster', 'CodeForecaster')", "('forecaster', 'CodeClimatePredictor')"),
    # Fix generic analyze calls in integration test
    (
        "if hasattr(instance, 'analyze'):\n                    result = instance.analyze()",
        """if hasattr(instance, 'analyze_evolution'):
                    result = instance.analyze_evolution()
                elif hasattr(instance, 'analyze_contributors'):
                    result = instance.analyze_contributors()
                elif hasattr(instance, 'analyze_dependencies'):
                    result = instance.analyze_dependencies()
                elif hasattr(instance, 'analyze_licenses'):
                    result = instance.analyze_licenses()
                elif hasattr(instance, 'analyze_performance'):
                    result = instance.analyze_performance()
                elif hasattr(instance, 'analyze_portability'):
                    result = instance.analyze_portability()
                elif hasattr(instance, 'analyze_team_health'):
                    result = instance.analyze_team_health()""",
    ),
]

# Apply replacements
for old, new in replacements:
    content = content.replace(old, new)

# Write back
with open(".github/workflows/beta-tests.yml", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Fixed .github/workflows/beta-tests.yml")
print("\nChanges made:")
for old, new in replacements:
    count = content.count(new)
    if count > 0:
        print(f"  - {old[:50]}... → {new[:50]}... ({count} occurrences)")
