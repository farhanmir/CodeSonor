"""
Auto-fix script for test_beta_manual.py
Corrects all class names and method calls.
"""

# Read the manual test file
with open("test_beta_manual.py", "r", encoding="utf-8") as f:
    content = f.read()

# Define replacements
replacements = [
    # Fix imports
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
    # Fix method calls
    (
        "archaeology = CodeArchaeology(repo_path)\n        result = archaeology.analyze()",
        "archaeology = CodeArchaeology(repo_path)\n        result = archaeology.analyze_evolution()",
    ),
    (
        "team_dna = TeamDNA(repo_path)\n        result = team_dna.analyze()",
        "team_dna = TeamDNA(repo_path)\n        result = team_dna.analyze_contributors()",
    ),
    (
        "analyzer = DependencyRisk(repo_path)\n        result = analyzer.analyze()",
        "analyzer = DependencyRisk(repo_path)\n        result = analyzer.analyze_dependencies()",
    ),
    (
        "forecaster = CodeClimatePredictor(repo_path)\n        result = forecaster.predict()",
        "forecaster = CodeClimatePredictor(repo_path)\n        result = forecaster.forecast_quality()",
    ),
    ("result = intelligence.analyze(", "result = intelligence.compare_with_best_practices("),
    (
        "assistant = OnboardingAssistant(repo_path)\n        result = assistant.generate_plan()",
        "assistant = OnboardingAssistant(repo_path)\n        result = assistant.create_code_tour()",
    ),
    (
        "detector = SmartSmellDetector(repo_path)\n        result = detector.analyze()",
        "detector = SmartSmellDetector(repo_path)\n        result = detector.detect_smells()",
    ),
    (
        "matrix = LicenseMatrix(repo_path)\n        result = matrix.analyze()",
        "matrix = LicenseMatrix(repo_path)\n        result = matrix.analyze_licenses()",
    ),
    (
        "predictor = PerformancePredictor(repo_path)\n        result = predictor.analyze()",
        "predictor = PerformancePredictor(repo_path)\n        result = predictor.analyze_performance()",
    ),
    (
        "tutor = ReviewTutor(repo_path)\n        result = tutor.review()",
        'tutor = ReviewTutor(repo_path)\n        result = tutor.conduct_review(str(repo_path / "src"))',
    ),
    (
        "analyzer = PortabilityAnalyzer(repo_path)\n        result = analyzer.analyze()",
        "analyzer = PortabilityAnalyzer(repo_path)\n        result = analyzer.analyze_portability()",
    ),
    (
        "analyzer = TeamHealthAnalyzer(repo_path)\n        result = analyzer.analyze()",
        "analyzer = TeamHealthAnalyzer(repo_path)\n        result = analyzer.analyze_team_health()",
    ),
]

# Apply replacements
for old, new in replacements:
    content = content.replace(old, new)

# Write back
with open("test_beta_manual.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Fixed test_beta_manual.py")
print("\nKey changes:")
print("  - Fixed class names: DependencyRiskAnalyzer → DependencyRisk")
print("  - Fixed class names: CodeForecaster → CodeClimatePredictor")
print("  - Fixed all method calls to use correct names")
