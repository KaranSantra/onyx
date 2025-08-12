# Backend Testing Overview

This document provides a comprehensive guide to the Onyx backend testing infrastructure, helping developers understand what tests are available, what they test, and when to run them.

### Test Architecture
- **Manager Classes**: Handle API calls for creating, deleting, and verifying entities
- **Test Classes**: Store expected state and test data
- **Fixtures**: Shared setup/teardown logic using pytest fixtures
- **Mocking**: Extensive use of mocks in unit tests to isolate functionality


## Manage EE-dependent tests (rename on/off)
```bash
cd backend
# Show current status and EE availability
python scripts/manage_ee_tests.py status
# Temporarily disable known EE-dependent tests (.ee_disabled suffix)
python scripts/manage_ee_tests.py disable
# Re-enable them
python scripts/manage_ee_tests.py enable
```


### Running Tests
#### For integration test - checkout the `backend/tests/integration/INTEGRATION_TEST_SETUP_GUIDE.md`:
```bash
cd backend

# Unit tests
pytest tests/unit/

# Integration tests - Checkout the `backend/tests/integration/INTEGRATION_TEST_SETUP_GUIDE.md` 
pytest tests/integration/tests/

# Daily tests
pytest tests/daily/

# With verbose output
pytest -s tests/unit/
```

#### Run specific test file:
```bash
pytest tests/unit/onyx/chat/test_answer.py
```

#### Run specific test function:
```bash
pytest tests/unit/onyx/chat/test_answer.py::test_answer_stream_simple
```

#### Run tests matching a pattern:
```bash
pytest -k "chat" tests/unit/
```

#### Run with parallel execution:
```bash
pytest -n auto tests/unit/
```

#### For integration tests with mock services:
```bash
cd backend/tests/integration/mock_services
docker compose -f docker-compose.mock-it-services.yml up -d
cd ../../..
pytest tests/integration/tests/
```

## Test Selection Guide

### Quick Reference: What to Test Based on Your Changes

| If you modified... | Run these tests |
|-------------------|-----------------|
| Chat/LLM logic | `tests/unit/onyx/chat/`, `tests/integration/tests/chat/` |
| Connectors | `tests/daily/connectors/<connector_name>/`, `tests/integration/tests/connector/` |
| File connector specifically | `tests/daily/connectors/file/test_file_connector.py` |
| Authentication/Users | `tests/unit/onyx/auth/`, `tests/integration/tests/auth/`, `tests/integration/tests/permissions/` |
| Document indexing | `tests/unit/onyx/indexing/`, `tests/integration/tests/indexing/` |
| Search functionality | `tests/unit/onyx/document_index/`, `tests/regression/search_quality/` |
| Permissions/Access control | `tests/integration/tests/permissions/`, `tests/integration/tests/usergroup/` |
| API endpoints | `tests/integration/tests/` (relevant feature folder) |
| Database models | `tests/integration/tests/migrations/` |
| Document processing | `tests/unit/onyx/indexing/test_chunker.py`, `tests/daily/embedding/` |
| LLM providers | `tests/integration/tests/llm_provider/`, `tests/unit/onyx/llm/` |

### Core Tests to Run Before Any Commit
```bash
# Minimum test suite
pytest tests/unit/
pytest tests/integration/tests/connector/test_connector_creation.py
pytest tests/integration/tests/indexing/test_polling.py
```




### Connector Tests

#### File Connector Test (As Requested)

**`tests/daily/connectors/file/test_file_connector.py`**
- **Purpose**: Tests local file connector functionality
- **What it tests**:
  - Text extraction from various file formats
  - Metadata extraction from file headers (#ONYX_METADATA)
  - File display name handling
  - Owner information extraction
  - Document timestamp handling
  - Tag processing
  - Link preservation
- **Key test cases**:
  - Single text file with metadata
  - Files without metadata
  - Various file formats (PDF, DOCX, etc.)
  - Zip file processing
- **Run when**: Modifying file upload, text extraction, or metadata processing

