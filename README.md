# Onyx Documentation Index

A comprehensive guide to all documentation in the Onyx repository.

## Setup & Configuration

| Document | Description | When to Use |
|----------|-------------|-------------|
| [CONTRIBUTING.md](./CONTRIBUTING.md) | General contribution guidelines and manual setup | Setting up development environment from scratch |
| [CONTRIBUTING_VSCODE.md](./CONTRIBUTING_VSCODE.md) | VS Code debugger configuration | Using VS Code for development and debugging |
| [CONTRIBUTING_MACOS.md](./CONTRIBUTING_MACOS.md) | macOS-specific setup instructions | Developing on macOS systems |
| [SETUP_GIT_WITH_NO_CONE.md](./SETUP_GIT_WITH_NO_CONE.md) | Git sparse-checkout to exclude enterprise folders | Configuring git to exclude EE-only code |

## Testing

| Document | Description | When to Use |
|----------|-------------|-------------|
| [backend/BACKEND_TESTING_OVERVIEW.md](./backend/BACKEND_TESTING_OVERVIEW.md) | Complete backend testing guide and architecture | Running or writing backend tests |
| [backend/tests/integration/INTEGRATION_TEST_SETUP_GUIDE.md](./backend/tests/integration/INTEGRATION_TEST_SETUP_GUIDE.md) | Detailed integration test environment setup | Setting up integration test environment |
| [backend/tests/integration/README.md](./backend/tests/integration/README.md) | Integration test design patterns and guidelines | Understanding integration test architecture |
| [backend/tests/regression/answer_quality/README.md](./backend/tests/regression/answer_quality/README.md) | Answer quality regression testing | Testing LLM answer quality |
| [backend/tests/regression/search_quality/README.md](./backend/tests/regression/search_quality/README.md) | Search quality regression testing | Testing search result quality |

## Backend Components

| Document | Description | When to Use |
|----------|-------------|-------------|
| [backend/onyx/connectors/README.md](./backend/onyx/connectors/README.md) | Creating custom data source connectors | Building new connector integrations |
| [backend/onyx/file_store/README.md](./backend/onyx/file_store/README.md) | File storage system documentation | Working with file storage |
| [backend/alembic/README.md](./backend/alembic/README.md) | Database migration management | Managing database schema changes |
| [backend/alembic_tenants/README.md](./backend/alembic_tenants/README.md) | Multi-tenant database migrations | Working with tenant-specific schemas |
| [backend/generated/README.md](./backend/generated/README.md) | Auto-generated code documentation | Understanding generated API clients |
| [backend/slackbot_images/README.md](./backend/slackbot_images/README.md) | Slack bot image assets | Customizing Slack bot appearance |

## Deployment

| Document | Description | When to Use |
|----------|-------------|-------------|
| [deployment/README.md](./deployment/README.md) | Deployment options overview | Choosing deployment strategy |
| [deployment/docker_compose/README.md](./deployment/docker_compose/README.md) | Docker Compose deployment | Deploying with Docker Compose |
| [deployment/helm/README.md](./deployment/helm/README.md) | Kubernetes Helm chart deployment | Deploying to Kubernetes |
| [deployment/aws_ecs_fargate/cloudformation/README.md](./deployment/aws_ecs_fargate/cloudformation/README.md) | AWS ECS Fargate deployment | Deploying on AWS infrastructure |

## Frontend & Other

| Document | Description | When to Use |
|----------|-------------|-------------|
| [web/README.md](./web/README.md) | Frontend development guide | Working on web interface |
| [web/src/lib/generated/README.md](./web/src/lib/generated/README.md) | Generated TypeScript client documentation | Using auto-generated API types |
| [examples/widget/README.md](./examples/widget/README.md) | Embedding Onyx widget examples | Integrating Onyx into external sites |