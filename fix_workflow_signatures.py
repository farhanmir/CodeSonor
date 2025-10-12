"""
Fix workflow file to use correct method signatures.
"""

with open(".github/workflows/beta-tests.yml", "r", encoding="utf-8") as f:
    content = f.read()

# Fix CrossRepoIntelligence in workflow
# The workflow calls intelligence.analyze(language='Python', topic='web')
# Should be: intelligence.find_similar_projects(language='Python', topic='web')

content = content.replace(
    "result = intelligence.compare_with_best_practices(language='Python', topic='web')",
    "result = intelligence.find_similar_projects(language='Python', topic='web')",
)

content = content.replace(
    "result = intelligence.compare_with_best_practices(language='Python')",
    "result = intelligence.compare_with_best_practices()",
)

# Fix ReviewTutor - conduct_review needs a file_path
# Find Python files in repo and pass the first one
old_tutor = """        from codesonor.review_tutor import ReviewTutor
        from pathlib import Path
        tutor = ReviewTutor(Path('../test-repo'))
        result = tutor.conduct_review()"""

new_tutor = """        from codesonor.review_tutor import ReviewTutor
        from pathlib import Path
        tutor = ReviewTutor(Path('../test-repo'))
        # Find a Python file to review
        py_files = list(Path('../test-repo').rglob('*.py'))
        if py_files:
            result = tutor.conduct_review(str(py_files[0]))
        else:
            result = {'error': 'No Python files found'}"""

content = content.replace(old_tutor, new_tutor)

# Write back
with open(".github/workflows/beta-tests.yml", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Fixed .github/workflows/beta-tests.yml")
print("\nFixes applied:")
print("  1. Fixed CrossRepoIntelligence method calls")
print("  2. Fixed ReviewTutor.conduct_review() - added file_path parameter")
