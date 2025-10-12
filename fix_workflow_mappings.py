"""
Script to generate corrected workflow file with proper class names and methods.
This fixes all the GitHub Actions failures.
"""

# Correct mappings
CORRECT_IMPORTS = {
    "CodeArchaeology": ("codesonor.archaeology", "CodeArchaeology", "analyze_evolution"),
    "TeamDNA": ("codesonor.team_dna", "TeamDNA", "analyze_contributors"),
    "DependencyRisk": ("codesonor.dep_risk", "DependencyRisk", "analyze_dependencies"),
    "CodeClimatePredictor": ("codesonor.forecaster", "CodeClimatePredictor", "forecast_quality"),
    "CrossRepoIntelligence": (
        "codesonor.cross_repo",
        "CrossRepoIntelligence",
        "compare_with_best_practices",
    ),
    "OnboardingAssistant": ("codesonor.onboarding", "OnboardingAssistant", "create_code_tour"),
    "SmartSmellDetector": ("codesonor.smart_smell", "SmartSmellDetector", "detect_smells"),
    "LicenseMatrix": ("codesonor.license_matrix", "LicenseMatrix", "analyze_licenses"),
    "PerformancePredictor": (
        "codesonor.perf_predictor",
        "PerformancePredictor",
        "analyze_performance",
    ),
    "ReviewTutor": ("codesonor.review_tutor", "ReviewTutor", "conduct_review"),
    "PortabilityAnalyzer": ("codesonor.portability", "PortabilityAnalyzer", "analyze_portability"),
    "TeamHealthAnalyzer": ("codesonor.team_health", "TeamHealthAnalyzer", "analyze_team_health"),
}

print("Correct class and method names for v0.5.0-beta:")
print("=" * 70)
for name, (module, cls, method) in CORRECT_IMPORTS.items():
    print(f"{cls:25} → {method}()")
print("=" * 70)
