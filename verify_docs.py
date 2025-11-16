#!/usr/bin/env python3
"""
Verify RoboEval documentation structure and completeness.

Run this script to check if all documentation files are properly created
and linked.
"""

import os
from pathlib import Path
from typing import List, Tuple

def check_file_exists(filepath: Path) -> Tuple[bool, str]:
    """Check if a file exists and return status."""
    exists = filepath.exists()
    status = "✓" if exists else "✗"
    return exists, f"{status} {filepath}"

def main():
    """Main verification function."""
    docs_root = Path(__file__).parent
    
    print("=" * 80)
    print("RoboEval Documentation Structure Verification")
    print("=" * 80)
    
    all_files = []
    
    # Core files
    print("\n📄 Core Files:")
    core_files = [
        "index.rst",
        "conf.py",
        "Makefile",
        "make.bat",
        "README.md",
        ".gitignore",
    ]
    for f in core_files:
        exists, msg = check_file_exists(docs_root / f)
        all_files.append(exists)
        print(f"  {msg}")
    
    # Getting Started
    print("\n📚 Getting Started:")
    getting_started_files = [
        "getting-started/installation.rst",
        "getting-started/quickstart.rst",
        "getting-started/examples.rst",
    ]
    for f in getting_started_files:
        exists, msg = check_file_exists(docs_root / f)
        all_files.append(exists)
        print(f"  {msg}")
    
    # User Guide
    print("\n📖 User Guide:")
    user_guide_files = [
        "user-guide/environments.rst",
        "user-guide/action-modes.rst",
        "user-guide/observations.rst",
        "user-guide/data-collection.rst",
        "user-guide/demonstrations.rst",
    ]
    for f in user_guide_files:
        exists, msg = check_file_exists(docs_root / f)
        all_files.append(exists)
        print(f"  {msg}")
    
    # Tasks
    print("\n🎯 Tasks:")
    task_files = [
        "tasks/index.rst",
        "tasks/lift-pot.rst",
        "tasks/stack-books.rst",
        "tasks/manipulation.rst",
        "tasks/rotate-valve.rst",
        "tasks/pack-box.rst",
        "tasks/lift-tray.rst",
    ]
    for f in task_files:
        exists, msg = check_file_exists(docs_root / f)
        all_files.append(exists)
        print(f"  {msg}")
    
    # Advanced
    print("\n🚀 Advanced Topics:")
    advanced_files = [
        "advanced/custom-tasks.rst",
        "advanced/custom-props.rst",
        "advanced/custom-robots.rst",
        "advanced/metrics.rst",
        "advanced/integrations.rst",
    ]
    for f in advanced_files:
        exists, msg = check_file_exists(docs_root / f)
        all_files.append(exists)
        print(f"  {msg}")
    
    # API Reference
    print("\n🔧 API Reference:")
    api_files = [
        "api/core.rst",
        "api/environments.rst",
        "api/robots.rst",
        "api/demonstrations.rst",
        "api/utils.rst",
    ]
    for f in api_files:
        exists, msg = check_file_exists(docs_root / f)
        all_files.append(exists)
        print(f"  {msg}")
    
    # Development
    print("\n💻 Development:")
    dev_files = [
        "development/contributing.rst",
        "development/testing.rst",
    ]
    for f in dev_files:
        exists, msg = check_file_exists(docs_root / f)
        all_files.append(exists)
        print(f"  {msg}")
    
    # Static files
    print("\n🎨 Static Files:")
    static_files = [
        "_static/css/custom.css",
        "_static/imgs/roboeval_overview.png",
        "_static/imgs/lift_pot.png",
    ]
    for f in static_files:
        exists, msg = check_file_exists(docs_root / f)
        all_files.append(exists)
        print(f"  {msg}")
    
    # GitHub Actions
    print("\n⚙️  GitHub Actions:")
    gh_files = [
        ".github/workflows/deploy-docs.yml",
    ]
    for f in gh_files:
        exists, msg = check_file_exists(docs_root / f)
        all_files.append(exists)
        print(f"  {msg}")
    
    # Summary
    print("\n" + "=" * 80)
    total = len(all_files)
    present = sum(all_files)
    missing = total - present
    
    print(f"Total files: {total}")
    print(f"Present: {present} ✓")
    print(f"Missing: {missing} ✗")
    
    if missing == 0:
        print("\n✅ All documentation files are present!")
        print("\nNext steps:")
        print("  1. Replace placeholder images in _static/imgs/")
        print("  2. Build the documentation: make html")
        print("  3. View locally: open _build/html/index.html")
        print("  4. Commit and push to deploy to GitHub Pages")
    else:
        print("\n⚠️  Some files are missing. Please check the output above.")
    
    print("=" * 80)
    
    return 0 if missing == 0 else 1

if __name__ == "__main__":
    exit(main())
