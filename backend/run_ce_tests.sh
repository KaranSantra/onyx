#!/bin/bash
# Script to run tests in Community Edition (CE) mode
# This script handles EE-dependent tests automatically

set -e  # Exit on any error

BACKEND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BACKEND_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Onyx Community Edition Test Runner${NC}"
echo "========================================="

# Check if EE modules are available (using sophisticated detection)
if python -c "from tests.ee_test_utils import is_ee_available; exit(0 if is_ee_available() else 1)" 2>/dev/null; then
    echo -e "${YELLOW}Warning: EE modules detected. Some tests may behave differently.${NC}"
    EE_AVAILABLE=true
else
    echo -e "${GREEN}Running in Community Edition mode.${NC}"
    EE_AVAILABLE=false
fi

# Function to run unit tests
run_unit_tests() {
    echo -e "\n${GREEN}Running Unit Tests...${NC}"
    echo -e "${YELLOW}Note: EE-dependent tests will be automatically skipped${NC}"
    
    # All EE-dependent tests now have proper skip markers
    pytest tests/unit/ -v
}

# Function to run integration tests
run_integration_tests() {
    echo -e "\n${GREEN}Running Integration Tests...${NC}"
    echo -e "${YELLOW}Note: EE-dependent tests will be automatically skipped${NC}"
    
    # All EE-dependent tests now have proper skip markers
    pytest tests/integration/tests/ -v
}

# Function to run external dependency tests
run_external_tests() {
    echo -e "\n${GREEN}Running External Dependency Tests...${NC}"
    echo -e "${YELLOW}Note: Tests requiring EE modules or external services will be skipped${NC}"
    echo -e "${YELLOW}This is expected behavior in CE mode.${NC}"
    echo ""
    
    # All EE-dependent tests now have proper skip markers
    # Tests will automatically skip if external services are not configured
    pytest tests/external_dependency_unit/ -v
    
    test_exit_code=$?
    
    # Exit code 5 means "no tests collected" which is expected if no external services are configured
    if [ $test_exit_code -eq 5 ]; then
        echo -e "\n${YELLOW}No tests were collected (external services not configured)${NC}"
        return 0
    else
        return $test_exit_code
    fi
}

# Function to run all safe tests
run_all_safe_tests() {
    echo -e "\n${GREEN}Running All CE-Safe Tests...${NC}"
    run_unit_tests
    run_integration_tests
}

# Main script logic
case "${1:-all}" in
    unit)
        run_unit_tests
        ;;
    integration)
        run_integration_tests
        ;;
    external)
        run_external_tests
        ;;
    all)
        run_all_safe_tests
        ;;
    help|--help|-h)
        echo "Usage: $0 [unit|integration|external|all|help]"
        echo ""
        echo "Commands:"
        echo "  unit        - Run unit tests (skipping EE-dependent ones)"
        echo "  integration - Run integration tests (skipping EE-dependent ones)"
        echo "  external    - Run external dependency tests (skipping EE-dependent ones)"
        echo "  all         - Run unit and integration tests (default)"
        echo "  help        - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0              # Run all safe tests"
        echo "  $0 unit         # Run only unit tests"
        echo "  $0 integration  # Run only integration tests"
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo "Run '$0 help' for usage information"
        exit 1
        ;;
esac

echo -e "\n${GREEN}Test run completed!${NC}"