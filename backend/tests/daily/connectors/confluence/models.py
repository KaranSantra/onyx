from pydantic import BaseModel

# Import EE test utilities for skipping
from tests.ee_test_utils import EE_NOT_AVAILABLE

# Skip this entire module due to EE dependencies
import pytest
pytestmark = pytest.mark.skipif(
    EE_NOT_AVAILABLE,
    reason="This test module depends on Enterprise Edition functionality"
)

# Conditional EE imports
try:
    from ee.onyx.db.external_perm import ExternalUserGroup
except ImportError:
    ExternalUserGroup = None

class ExternalUserGroupSet(BaseModel):
    """A version of ExternalUserGroup that uses a set for user_emails to avoid order-dependent comparisons."""

    id: str
    user_emails: set[str]
    gives_anyone_access: bool

    @classmethod
    def from_model(
        cls, external_user_group: ExternalUserGroup
    ) -> "ExternalUserGroupSet":
        """Convert from ExternalUserGroup to ExternalUserGroupSet."""
        return cls(
            id=external_user_group.id,
            user_emails=set(external_user_group.user_emails),
            gives_anyone_access=external_user_group.gives_anyone_access,
        )
