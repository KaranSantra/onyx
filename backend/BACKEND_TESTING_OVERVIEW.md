# Backend Testing Overview

This document provides a comprehensive guide to the Onyx backend testing infrastructure, helping developers understand what tests are available, what they test, and when to run them.

## Table of Contents
1. [Test Structure Overview](#test-structure-overview)
2. [Test Categories](#test-categories)
3. [How to Run Tests](#how-to-run-tests)
4. [Test Selection Guide](#test-selection-guide)
5. [Detailed Test Descriptions](#detailed-test-descriptions)

## Test Structure Overview

The backend tests are organized into four main categories:

```
backend/tests/
├── unit/          # Fast, isolated function tests with mocking
├── integration/   # Full API workflow tests requiring running services
├── daily/         # Connector and embedding tests (run daily in CI)
└── regression/    # Answer and search quality evaluation tests
```

### Test Architecture
- **Manager Classes**: Handle API calls for creating, deleting, and verifying entities
- **Test Classes**: Store expected state and test data
- **Fixtures**: Shared setup/teardown logic using pytest fixtures
- **Mocking**: Extensive use of mocks in unit tests to isolate functionality

## Test Categories

### 1. Unit Tests (`tests/unit/`)
**Purpose**: Test individual functions and classes in isolation  
**Speed**: Fast (milliseconds to seconds)  
**Dependencies**: None (uses mocks)  
**When to run**: After any code change to the tested modules

### 2. Integration Tests (`tests/integration/`)
**Purpose**: Test complete API workflows and feature interactions  
**Speed**: Slower (seconds to minutes)  
**Dependencies**: Requires Onyx services running (API on port 8080, Vespa, PostgreSQL)  
**When to run**: Before commits, after feature implementation

### 3. Daily Tests (`tests/daily/`)
**Purpose**: Test connector functionality and document processing  
**Speed**: Varies (some require external services)  
**Dependencies**: May require external service credentials  
**When to run**: When modifying connectors or document processing

### 4. Regression Tests (`tests/regression/`)
**Purpose**: Evaluate search and answer quality  
**Speed**: Slow (minutes to hours)  
**Dependencies**: Requires test datasets and evaluation metrics  
**When to run**: Before major releases, after search/LLM changes

## How to Run Tests

### Prerequisites

1. **Install test dependencies**:
```bash
cd backend
pip install -r requirements/dev.txt
```

2. **For integration tests**, ensure Onyx is running:
```bash
# Services must be running with:
AUTH_TYPE=basic
ENABLE_PAID_ENTERPRISE_EDITION_FEATURES=true
# API server on port 8080
```

3. **Optional**: Create `.test.env` file for test credentials:
```bash
cd backend/tests
echo "TEST_VAR=value" > .test.env
```

### Running Tests

#### Run all tests in a category:
```bash
cd backend

# Unit tests
pytest tests/unit/

# Integration tests
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

## Detailed Test Descriptions

### Chat and LLM Tests

#### Unit Tests

**`tests/unit/onyx/chat/test_answer.py`**
- Tests the Answer class for generating LLM responses
- Covers streaming, tool calling, search integration
- Tests cancellation handling and reranking configurations
- **Run when**: Modifying chat response generation or tool integration

**`tests/unit/onyx/chat/test_prune_and_merge.py`**
- Tests document pruning and merging logic for context windows
- **Run when**: Changing document selection algorithms

**`tests/unit/onyx/chat/stream_processing/test_citation_processing.py`**
- Tests citation extraction and formatting from LLM responses
- **Run when**: Modifying citation logic

**`tests/unit/onyx/llm/test_chat_llm.py`**
- Tests LLM interaction layer, especially tool calling
- Tests multiple simultaneous tool calls
- **Run when**: Changing LLM integration or tool calling logic

#### Integration Tests

**`tests/integration/tests/chat/test_chat_deletion.py`**
- Tests soft and hard deletion of chat sessions
- Verifies CASCADE deletion behavior
- Tests deletion with agent search data
- **Run when**: Modifying chat storage or deletion logic

**`tests/integration/tests/dev_apis/test_simple_chat_api.py`**
- Tests simplified chat API endpoints
- **Run when**: Modifying public API interfaces

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

#### Integration Connector Tests

**`tests/integration/tests/connector/test_connector_creation.py`**
- Tests connector CRUD operations
- Tests overlapping connectors (multiple connectors indexing same docs)
- Tests pausing connectors during indexing
- **Run when**: Modifying connector management logic

**`tests/integration/tests/connector/test_connector_deletion.py`**
- Tests connector deletion and cleanup
- **Run when**: Modifying connector lifecycle management

### Indexing and Document Processing Tests

#### Unit Tests

**`tests/unit/onyx/indexing/test_chunker.py`**
- **Purpose**: Tests document chunking for vector search
- **What it tests**:
  - Document splitting into appropriate chunk sizes
  - Metadata preservation in chunks
  - Contextual RAG configuration effects
  - Chunk overlap handling
- **Run when**: Modifying chunking algorithms or chunk sizes

**`tests/unit/onyx/indexing/test_embedder.py`**
- Tests embedding generation for documents
- **Run when**: Modifying embedding logic or models

**`tests/unit/onyx/indexing/test_indexing_pipeline.py`**
- Tests the complete indexing pipeline
- **Run when**: Modifying any part of the indexing flow

#### Integration Tests

**`tests/integration/tests/indexing/test_polling.py`**
- **Purpose**: Tests incremental polling behavior
- **What it tests**:
  - Poll time range management
  - Prevention of duplicate indexing
  - Proper time range boundaries
  - POLL_CONNECTOR_OFFSET handling
- **Run when**: Modifying polling logic or time-based indexing

**`tests/integration/tests/indexing/test_checkpointing.py`**
- Tests indexing checkpoint/resume functionality
- **Run when**: Modifying fault tolerance or resume logic

**`tests/integration/tests/indexing/test_initial_permission_sync.py`**
- Tests permission synchronization during initial indexing
- **Run when**: Modifying permission sync logic

### Authentication and Permissions Tests

#### Unit Tests

**`tests/unit/onyx/auth/test_email.py`**
- Tests email invitation system
- Currently skipped (sends real emails)
- **Run when**: Modifying email templates or invitation logic

**`tests/unit/onyx/auth/test_oauth_refresher.py`**
- Tests OAuth token refresh logic
- **Run when**: Modifying OAuth integration

#### Integration Tests

**`tests/integration/tests/permissions/test_user_role_permissions.py`**
- Tests role-based access control
- Verifies admin vs regular user permissions
- **Run when**: Modifying authorization logic

**`tests/integration/tests/permissions/test_connector_permissions.py`**
- Tests connector access permissions
- **Run when**: Modifying connector visibility rules

**`tests/integration/tests/permissions/test_doc_set_permissions.py`**
- Tests document set access control
- **Run when**: Modifying document access rules

**`tests/integration/tests/auth/test_saml_user_conversion.py`**
- Tests SAML authentication user conversion
- **Run when**: Modifying SAML integration

### User and Group Management Tests

**`tests/integration/tests/usergroup/test_usergroup_syncing.py`**
- Tests user group synchronization
- Tests group membership updates
- **Run when**: Modifying group management

**`tests/integration/tests/usergroup/test_user_group_deletion.py`**
- Tests user group deletion and cleanup
- **Run when**: Modifying group lifecycle

**`tests/integration/tests/users/test_user_pagination.py`**
- Tests user listing and pagination
- **Run when**: Modifying user management APIs

### LLM Provider Tests

**`tests/integration/tests/llm_provider/test_llm_provider.py`**
- **Purpose**: Tests LLM provider configuration
- **What it tests**:
  - Provider creation with various configurations
  - Model configuration management
  - Default model handling
  - Duplicate configuration prevention
  - Provider updates and deletion
- **Run when**: Adding new LLM providers or modifying provider logic

### Document Management Tests

**`tests/integration/tests/document_set/test_syncing.py`**
- Tests document set synchronization
- **Run when**: Modifying document set logic

**`tests/integration/tests/pruning/test_pruning.py`**
- Tests document pruning (removal of deleted docs)
- **Run when**: Modifying document lifecycle management

### Search and Retrieval Tests

**`tests/regression/search_quality/run_search_eval.py`**
- Evaluates search result quality
- Requires test query dataset
- **Run when**: Modifying search algorithms

**`tests/unit/onyx/document_index/vespa/shared_utils/test_utils.py`**
- Tests Vespa search utilities
- **Run when**: Modifying Vespa integration

### Tool Tests

**`tests/unit/onyx/tools/test_tool_utils.py`**
- Tests tool calling utility functions
- Tests provider-specific tool support detection
- **Run when**: Modifying tool integration

**`tests/integration/tests/tools/test_image_generation_tool.py`**
- Tests image generation tool integration
- **Run when**: Modifying image generation features

### Performance and Quality Tests

**`tests/integration/tests/query_history/test_query_history.py`**
- Tests query history tracking
- **Run when**: Modifying query logging

**`tests/integration/tests/query_history/test_usage_reports.py`**
- Tests usage report generation
- **Run when**: Modifying analytics or reporting

**`tests/integration/tests/personas/test_persona_categories.py`**
- Tests persona label management
- Tests admin-only access control
- **Run when**: Modifying persona features

## Testing Best Practices

1. **Always run unit tests** after code changes - they're fast and catch most issues
2. **Run integration tests** before committing features
3. **Check test output carefully** - Some tests may pass but with warnings
4. **Use -s flag** for debugging to see print statements
5. **Create .test.env** for local credentials instead of hardcoding
6. **Run related tests together** to catch interaction issues
7. **Don't skip flaky tests** - Fix them or report them

## Common Issues and Solutions

### Integration tests failing
- Ensure Onyx is running with correct environment variables
- Check if mock services are needed and running
- Verify PostgreSQL and Vespa are accessible

### Permission denied errors
- Run with proper Python virtual environment activated
- Check file permissions in test directories

### Import errors
- Install all requirements: `pip install -r requirements/dev.txt`
- Ensure PYTHONPATH includes backend directory

### Slow test execution
- Use pytest-xdist for parallel execution: `pytest -n auto`
- Run only relevant test files instead of entire suites
- Skip regression tests during development

## Contributing New Tests

When adding new tests:
1. Follow existing patterns for consistency
2. Add clear docstrings explaining what is tested
3. Use appropriate fixtures and managers
4. Consider both success and failure cases
5. Update this document if adding new test categories