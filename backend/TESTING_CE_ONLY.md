# Testing in Community Edition (CE) Mode

This guide covers running tests in Community Edition mode without Enterprise Edition dependencies.

## Quick Start

### Running Tests
Use the CE test runner script for the best experience:

```bash
# Run all CE-compatible tests (recommended)
./run_ce_tests.sh

# Run specific test categories
./run_ce_tests.sh unit        # Unit tests only
./run_ce_tests.sh integration # Integration tests only
./run_ce_tests.sh external    # External dependency tests
./run_ce_tests.sh all         # Unit + Integration tests
```

### Expected Results
When running in CE mode:
- **✅ Passed tests**: Core functionality that works without EE
- **⏭️ Skipped tests**: EE-dependent tests (properly marked, don't affect metrics)
- **❌ Failed tests**: May indicate missing external services (normal in CE)

### Test Categories
- **~106 CE-compatible tests**: Run without issues
- **6 EE-dependent tests**: Automatically skipped with clear reasons
- **External service tests**: May fail if services not configured (expected)













































---


## Skip System Explanation

### How EE Test Skipping Works
Tests with Enterprise Edition dependencies use pytest skip markers to avoid affecting test metrics:

```python
# Module-level skip (entire file)
from tests.ee_test_utils import EE_NOT_AVAILABLE
import pytest

pytestmark = pytest.mark.skipif(
    EE_NOT_AVAILABLE,
    reason="This test module depends on Enterprise Edition functionality"
)

# Conditional imports
if not EE_NOT_AVAILABLE:
    from ee.onyx.some_module import some_function
else:
    some_function = None
```

### Test Result Interpretation
- **Skipped tests appear in pytest output**: `24 skipped` - this is correct behavior
- **Skipped ≠ Failed**: Skipped tests don't count against pass/fail metrics
- **Clear skip reasons**: Each skipped test shows why it was skipped


## Developer Guidelines

### Adding New Tests

#### For CE-Only Tests
```python
# Normal test - no special handling needed
def test_my_feature():
    # Test CE functionality
    assert True
```

#### For EE-Dependent Tests  
```python
from tests.ee_test_utils import EE_NOT_AVAILABLE
import pytest

# Module-level skip for files that are entirely EE-dependent
pytestmark = pytest.mark.skipif(
    EE_NOT_AVAILABLE,
    reason="This test module depends on Enterprise Edition functionality"
)

# Conditional EE imports
if not EE_NOT_AVAILABLE:
    from ee.onyx.some_module import SomeEEClass
else:
    SomeEEClass = None
```

#### For Mixed Files (some tests need EE, some don't)
```python
from tests.ee_test_utils import ee_only

# Individual test skip
@ee_only
def test_ee_specific_feature():
    # This test will be skipped in CE mode
    pass

def test_ce_compatible_feature():
    # This test will run in CE mode
    pass
```

### Best Practices

1. **Import Order Matters**: Always put skip markers BEFORE EE imports
2. **Use Conditional Imports**: Wrap EE imports in `if not EE_NOT_AVAILABLE:` blocks
3. **Prefer Module-Level Skips**: If entire file needs EE, use `pytestmark`
4. **Clear Skip Reasons**: Always provide descriptive skip messages
5. **Test Without EE**: Regularly run tests in CE mode to catch issues early

### External Dependencies
For tests requiring external services (PostgreSQL, Vespa, MinIO, etc.):
```python
import pytest

# Skip when service not available
@pytest.mark.skipif(
    not service_available(),
    reason="Requires external service to be running"
)
def test_with_external_service():
    pass
```

## EE Import Fixes Applied

This section documents the specific fixes applied to resolve EE import issues in Community Edition mode.

### Problem
Several test files had EE imports at the module level before skip markers, causing ImportError crashes during test collection:

```python
# BROKEN - EE import before skip marker
from ee.onyx.some_module import SomeClass  # ❌ ImportError in CE mode

from tests.ee_test_utils import EE_NOT_AVAILABLE
pytestmark = pytest.mark.skipif(EE_NOT_AVAILABLE, reason="...")  # Too late!
```

### Solution Pattern
We fixed 6 files using this minimally invasive pattern:

```python
# FIXED - Skip marker before EE imports  
import pytest

# Import EE test utilities FIRST
from tests.ee_test_utils import EE_NOT_AVAILABLE

# Skip marker BEFORE any EE imports
pytestmark = pytest.mark.skipif(
    EE_NOT_AVAILABLE,
    reason="This test module depends on Enterprise Edition functionality"
)

# Conditional EE imports - only if EE available
if not EE_NOT_AVAILABLE:
    from ee.onyx.some_module import SomeClass
else:
    SomeClass = None

# Normal CE imports continue...
from onyx.regular.module import RegularClass
```

### Files Fixed

1. **`tests/daily/connectors/confluence/test_confluence_permissions_basic.py`**
   - Fixed: `from ee.onyx.external_permissions.confluence.doc_sync import confluence_doc_sync`

2. **`tests/daily/connectors/google_drive/test_drive_perm_sync.py`** 
   - Fixed: Multiple EE imports for Google Drive sync functions

3. **`tests/external_dependency_unit/connectors/confluence/test_confluence_group_sync.py`**
   - Fixed: `from ee.onyx.external_permissions.confluence.group_sync import confluence_group_sync`

4. **`tests/integration/tests/query_history/test_usage_reports.py`**
   - Fixed: `from ee.onyx.db.usage_export import get_all_empty_chat_message_entries`

5. **`tests/regression/answer_quality/api_utils.py`**
   - Fixed: `from ee.onyx.server.query_and_chat.models import OneShotQARequest`

6. **`tests/regression/search_quality/run_search_eval.py`**
   - Fixed: Multiple EE model imports for search evaluation

