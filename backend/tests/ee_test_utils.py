"""
Utility functions for handling Enterprise Edition (EE) dependencies in tests.

This module provides utilities to detect EE availability and skip tests
that require EE functionality when running in Community Edition (CE) mode.
"""

import pytest
import sys
from typing import Any


def is_ee_available() -> bool:
    """
    Check if Enterprise Edition modules are available.
    
    Returns:
        bool: True if EE modules can be imported, False otherwise.
    """
    try:
        # Test for specific EE modules that tests commonly use
        import ee.onyx.server.query_and_chat.models
        import ee.onyx.server.user_group.models
        return True
    except ImportError:
        return False


def skip_if_ee_not_available(reason: str = "Requires Enterprise Edition"):
    """
    Decorator to skip tests that require EE functionality.
    
    Args:
        reason: Custom reason for skipping the test.
        
    Returns:
        pytest.mark.skipif decorator
    """
    return pytest.mark.skipif(
        not is_ee_available(),
        reason=reason
    )


def conditional_ee_import(module_path: str, fallback=None):
    """
    Conditionally import an EE module, returning fallback if not available.
    
    Args:
        module_path: The module path to import (e.g., 'ee.onyx.server.models')
        fallback: Value to return if import fails (default: None)
        
    Returns:
        The imported module or the fallback value
    """
    try:
        parts = module_path.split('.')
        module = __import__(module_path, fromlist=[parts[-1]])
        return module
    except ImportError:
        return fallback


# Global constant for use in test modules
EE_NOT_AVAILABLE = not is_ee_available()

# Pytest marker for EE-only tests
ee_only = pytest.mark.skipif(
    EE_NOT_AVAILABLE,
    reason="Test requires Enterprise Edition functionality"
)