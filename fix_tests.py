"""
Auto-fix script for test_beta_features.py
Corrects all class names, method calls, and fixtures.
"""

import re

# Read the test file
with open("tests/test_beta_features.py", "r", encoding="utf-8") as f:
    content = f.read()

# Define replacements
replacements = [
    # Fix imports - wrong class names
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
    # Fix method calls - CodeArchaeology
    ("archaeology.analyze()", "archaeology.analyze_evolution()"),
    # Fix method calls - TeamDNA
    ("team_dna.analyze()", "team_dna.analyze_contributors()"),
    # Fix method calls - DependencyRisk
    ("analyzer.analyze()", "analyzer.analyze_dependencies()"),
    # Fix method calls - CodeClimatePredictor
    ("forecaster.predict()", "forecaster.forecast_quality()"),
    # Fix method calls - CrossRepoIntelligence
    ("intelligence.analyze(", "intelligence.compare_with_best_practices("),
    # Fix method calls - OnboardingAssistant
    ("assistant.generate_plan()", "assistant.create_code_tour()"),
    # Fix method calls - SmartSmellDetector
    ("detector.analyze()", "detector.detect_smells()"),
    # Fix method calls - LicenseMatrix
    ("matrix.analyze()", "matrix.analyze_licenses()"),
    # Fix method calls - PerformancePredictor
    ("predictor.analyze()", "predictor.analyze_performance()"),
    # Fix method calls - ReviewTutor
    ("tutor.review()", "tutor.conduct_review("),
    # Fix method calls - PortabilityAnalyzer
    (
        "PortabilityAnalyzer(repo_path)\n        result = analyzer.analyze()",
        "PortabilityAnalyzer(repo_path)\n        result = analyzer.analyze_portability()",
    ),
    # Fix method calls - TeamHealthAnalyzer
    (
        "TeamHealthAnalyzer(repo_path)\n        result = analyzer.analyze()",
        "TeamHealthAnalyzer(repo_path)\n        result = analyzer.analyze_team_health()",
    ),
]

# Apply replacements
for old, new in replacements:
    content = content.replace(old, new)

# Fix the temp_python_file fixture for Windows compatibility
old_fixture = """@pytest.fixture
def temp_python_file():
    \"\"\"Create a temporary Python file for testing\"\"\"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(
            \"\"\"
def example_function():
    \"\"\"Example function for testing\"\"\"
    x = 1
    y = 2
    z = x + y
    return z

class ExampleClass:
    def __init__(self):
        self.value = 42
    
    def method(self):
        return self.value * 2
\"\"\"
        )
        f.flush()

        yield Path(f.name)

        os.unlink(f.name)"""

new_fixture = """@pytest.fixture
def temp_python_file():
    \"\"\"Create a temporary Python file for testing\"\"\"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(
            \"\"\"
def example_function():
    '''Example function for testing'''
    x = 1
    y = 2
    z = x + y
    return z

class ExampleClass:
    def __init__(self):
        self.value = 42
    
    def method(self):
        return self.value * 2
\"\"\"
        )
        f.flush()
        f.close()  # Explicitly close before yielding

    file_path = Path(f.name)
    yield file_path

    try:
        os.unlink(file_path)
    except PermissionError:
        pass  # File might still be in use on Windows"""

content = content.replace(old_fixture, new_fixture)

# Write back
with open("tests/test_beta_features.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Fixed tests/test_beta_features.py")
print("\nKey changes:")
print("  - Fixed class names: DependencyRiskAnalyzer → DependencyRisk")
print("  - Fixed class names: CodeForecaster → CodeClimatePredictor")
print("  - Fixed all method calls to use correct names")
print("  - Fixed temp_python_file fixture for Windows compatibility")
print("  - Added proper file closing before deletion")
