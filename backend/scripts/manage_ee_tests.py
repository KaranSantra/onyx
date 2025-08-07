#!/usr/bin/env python3
"""
Script to manage Enterprise Edition (EE) dependent tests.

This script can temporarily disable or re-enable EE-dependent test files
by renaming them with a .ee_disabled extension.
"""

import os
import sys
from pathlib import Path
from typing import List

# Add backend to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# List of files that are heavily dependent on EE functionality
EE_DEPENDENT_FILES = [
    "tests/regression/answer_quality/api_utils.py",
    "tests/regression/search_quality/run_search_eval.py", 
    "tests/daily/connectors/google_drive/test_drive_perm_sync.py",
    "tests/daily/connectors/confluence/test_confluence_permissions_basic.py",
    "tests/external_dependency_unit/connectors/google_drive/test_google_drive_group_sync.py",
    "tests/external_dependency_unit/connectors/confluence/test_confluence_group_sync.py",
    "tests/unit/onyx/connectors/jira/test_jira_permission_sync.py",
    "tests/integration/tests/query_history/test_usage_reports.py",
    "tests/integration/common_utils/managers/document_search.py",
    "tests/integration/common_utils/managers/query_history.py",
    "tests/daily/connectors/confluence/models.py",
]

def is_ee_available() -> bool:
    """Check if EE modules are available."""
    try:
        import ee.onyx  # type: ignore
        return True
    except ImportError:
        return False

def disable_ee_tests(base_dir: Path = None) -> None:
    """Disable EE-dependent tests by renaming them."""
    if base_dir is None:
        base_dir = backend_dir
    
    disabled_count = 0
    
    for file_path in EE_DEPENDENT_FILES:
        full_path = base_dir / file_path
        disabled_path = full_path.with_suffix(full_path.suffix + ".ee_disabled")
        
        if full_path.exists() and not disabled_path.exists():
            try:
                full_path.rename(disabled_path)
                print(f"Disabled: {file_path}")
                disabled_count += 1
            except Exception as e:
                print(f"Failed to disable {file_path}: {e}")
        elif disabled_path.exists():
            print(f"Already disabled: {file_path}")
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nDisabled {disabled_count} EE-dependent test files")

def enable_ee_tests(base_dir: Path = None) -> None:
    """Re-enable EE-dependent tests by restoring their original names."""
    if base_dir is None:
        base_dir = backend_dir
    
    enabled_count = 0
    
    for file_path in EE_DEPENDENT_FILES:
        full_path = base_dir / file_path
        disabled_path = full_path.with_suffix(full_path.suffix + ".ee_disabled")
        
        if disabled_path.exists():
            try:
                disabled_path.rename(full_path)
                print(f"Enabled: {file_path}")
                enabled_count += 1
            except Exception as e:
                print(f"Failed to enable {file_path}: {e}")
        elif full_path.exists():
            print(f"Already enabled: {file_path}")
        else:
            print(f"Disabled file not found: {file_path}")
    
    print(f"\nEnabled {enabled_count} EE-dependent test files")

def status() -> None:
    """Show status of EE-dependent test files."""
    print("Enterprise Edition Test Status")
    print("=" * 40)
    print(f"EE modules available: {is_ee_available()}")
    print()
    
    enabled_count = 0
    disabled_count = 0
    
    for file_path in EE_DEPENDENT_FILES:
        full_path = backend_dir / file_path
        disabled_path = full_path.with_suffix(full_path.suffix + ".ee_disabled")
        
        if full_path.exists():
            print(f"✓ ENABLED:  {file_path}")
            enabled_count += 1
        elif disabled_path.exists():
            print(f"✗ DISABLED: {file_path}")
            disabled_count += 1
        else:
            print(f"? MISSING:  {file_path}")
    
    print()
    print(f"Total: {enabled_count} enabled, {disabled_count} disabled")

def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("Usage: python manage_ee_tests.py [disable|enable|status]")
        print()
        print("Commands:")
        print("  disable - Disable EE-dependent tests (rename with .ee_disabled)")
        print("  enable  - Re-enable EE-dependent tests (restore original names)")
        print("  status  - Show current status of EE tests")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "disable":
        disable_ee_tests()
    elif command == "enable":
        enable_ee_tests()
    elif command == "status":
        status()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()