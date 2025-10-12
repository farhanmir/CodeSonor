#!/usr/bin/env python3
"""
Cleanup temporary files from beta development
Run this to clean up before creating the beta release
"""

import os
from pathlib import Path


def main():
    print("🧹 CodeSonor Beta Cleanup")
    print("=" * 50)
    print()

    # Files to remove
    temp_files = [
        "fix_workflow_signatures.py",
        "fix_workflow_mappings.py",
        "fix_workflow.py",
        "fix_test_signatures.py",
        "fix_tests.py",
        "fix_remaining_9_tests.py",
        "fix_manual_tests.py",
        "fix_beta_tests_comprehensive.py",
        "fix_all_test_issues.py",
        "TEST_FIXES_ROUND_3.md",
        "CLEANUP_AND_NEXT_STEPS.md",  # Replaced by BETA_RELEASE_PLAN.md
    ]

    removed = []
    not_found = []

    for file in temp_files:
        if Path(file).exists():
            print(f"  Removing: {file}")
            removed.append(file)
        else:
            not_found.append(file)

    print()
    print(f"Files to remove: {len(removed)}")
    print(f"Already gone: {len(not_found)}")
    print()

    if removed:
        print("Files marked for removal:")
        for f in removed:
            print(f"  - {f}")
        print()

        response = input("Remove these files? (yes/no): ").strip().lower()

        if response == "yes":
            for file in removed:
                try:
                    os.remove(file)
                    print(f"  ✅ Removed: {file}")
                except Exception as e:
                    print(f"  ❌ Error removing {file}: {e}")

            print()
            print("✅ Cleanup complete!")
            print()
            print("Next steps:")
            print("  1. git add -A")
            print("  2. git commit -m '🧹 Clean up temporary fix scripts'")
            print("  3. git push origin beta")
            print("  4. Create GitHub beta release (see BETA_RELEASE_PLAN.md)")
        else:
            print("❌ Cleanup cancelled")
    else:
        print("✅ Nothing to clean up!")


if __name__ == "__main__":
    main()
