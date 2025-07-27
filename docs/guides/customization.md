# Customization Instructions

This guide shows you how to customize the Claude Code Project Template to fit your specific needs, from adding new sub-agents to creating custom commands and configuring automation hooks.

## Table of Contents

1. [Customizing CLAUDE.md](#customizing-claudemd)
2. [Creating Custom Commands](#creating-custom-commands)
3. [Adding New Sub-Agents](#adding-new-sub-agents)
4. [Configuring Hooks](#configuring-hooks)
5. [Modifying Project Structure](#modifying-project-structure)
6. [Custom Workflows](#custom-workflows)
7. [Integration Customization](#integration-customization)

## Customizing CLAUDE.md

The `CLAUDE.md` file is the central configuration for how Claude understands and works with your project. It's automatically created when you initialize a new project.

### Key Sections to Customize

#### 1. Project Overview
```markdown
## 1. Project Overview
- **Vision:** [Your specific project vision]
- **Current Phase:** [Development/Beta/Production]
- **Key Architecture:** [Monolith/Microservices/Serverless]
- **Development Strategy:** [Agile/Waterfall/Hybrid]
```

#### 2. Coding Standards
```markdown
### Coding Standards & AI Instructions
- **Language Preferences:** Python 3.12+, TypeScript
- **Framework Choices:** FastAPI, React, PostgreSQL
- **Testing Requirements:** 90% coverage minimum
- **Documentation Style:** Google docstrings
- **Naming Conventions:** snake_case for Python, camelCase for JS
```

#### 3. Custom Instructions
Add project-specific instructions:

```markdown
### Project-Specific Rules
- Always use async/await for database operations
- Implement rate limiting on all public APIs
- Use dependency injection for better testability
- Follow Domain-Driven Design principles
- Implement feature flags for new functionality
```

### Example: E-commerce Project CLAUDE.md

```markdown
# E-commerce Platform - AI Context

## 1. Project Overview
- **Vision:** Modern, scalable e-commerce platform with AI-powered recommendations
- **Current Phase:** MVP Development
- **Key Architecture:** Microservices with event-driven communication
- **Development Strategy:** Agile with 2-week sprints

## 2. Architecture Decisions
- **Payment Processing:** Stripe integration only
- **Search:** Elasticsearch for product search
- **Caching:** Redis for session and product cache
- **Message Queue:** RabbitMQ for order processing

## 3. Security Requirements
- PCI DSS compliance required
- All payment data must be tokenized
- Customer PII must be encrypted at rest
- Implement fraud detection on all transactions
```

## Creating Custom Commands

Custom commands extend Claude's capabilities for your specific workflow.

### Command Structure

Commands are defined in `commands/` directory with this structure:

```
commands/
├── dev/
│   ├── feature.md
│   ├── review.md
│   └── custom-command.md
├── project/
│   └── custom-project-command.md
└── domain/
    └── your-domain-commands.md
```

### Creating a New Command

#### 1. Basic Command Template
Create `commands/dev/migrate-database.md`:

```markdown
# /dev:migrate-database

Executes database migrations with safety checks and rollback capability.

## Usage
`/dev:migrate-database [version] [--dry-run]`

## Process
1. Check current database version
2. Validate migration files
3. Create backup (production only)
4. Execute migrations in transaction
5. Verify data integrity
6. Update migration history

## Options
- `version`: Target migration version (default: latest)
- `--dry-run`: Show what would be migrated without executing

## Safety Checks
- Automatic backup before migration
- Transaction rollback on error
- Data validation after migration
- Compatibility check with current code
```

#### 2. Domain-Specific Command
Create `commands/ecommerce/process-order.md`:

```markdown
# /ecommerce:process-order

Implements complete order processing workflow with payment, inventory, and shipping.

## Usage
`/ecommerce:process-order <order-id>`

## Workflow
1. Validate order details
2. Check inventory availability
3. Process payment through Stripe
4. Update inventory levels
5. Generate shipping label
6. Send confirmation emails
7. Update order status
8. Trigger fulfillment webhook

## Sub-Agent Coordination
- Security Auditor: Validates payment data
- Test Engineer: Creates order processing tests
- Documentation Specialist: Updates API docs
```

### Advanced Command Features

#### 1. Multi-Stage Commands
```markdown
# /dev:feature-complete

## Stages
1. **Planning Stage**
   - Trigger: Planning Architect
   - Output: Technical design document

2. **Implementation Stage**
   - Implement core functionality
   - Create unit tests
   - Add integration tests

3. **Review Stage**
   - Trigger: Code Reviewer
   - Security audit
   - Performance check

4. **Documentation Stage**
   - API documentation
   - User guide updates
   - Architecture updates
```

#### 2. Conditional Commands
```markdown
# /deploy:smart

## Conditions
- If changes in `src/api/`: Run API tests
- If changes in `src/frontend/`: Run E2E tests
- If changes in `database/`: Run migration tests
- If performance critical: Run load tests

## Deployment Strategy
- Development: Direct deployment
- Staging: Blue-green deployment
- Production: Canary deployment with 10% rollout
```

## Adding New Sub-Agents

Sub-agents are specialized AI assistants that handle specific domains of expertise.

### Sub-Agent Structure

```python
# src/agents/base_agent.py
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Base class for all sub-agents"""
    
    def __init__(self, name: str, expertise: list[str]):
        self.name = name
        self.expertise = expertise
    
    @abstractmethod
    async def analyze(self, context: dict) -> dict:
        """Analyze the given context"""
        pass
    
    @abstractmethod
    async def execute(self, task: dict) -> dict:
        """Execute the specified task"""
        pass
```

### Creating a Custom Sub-Agent

#### 1. Domain Expert Agent
Create `src/agents/database_architect.py`:

```python
from typing import Dict, List, Optional
from .base_agent import BaseAgent

class DatabaseArchitect(BaseAgent):
    """Specialized agent for database design and optimization"""
    
    def __init__(self):
        super().__init__(
            name="Database Architect",
            expertise=[
                "database_design",
                "query_optimization", 
                "data_modeling",
                "migration_planning"
            ]
        )
    
    async def analyze(self, context: Dict) -> Dict:
        """Analyze database requirements and current state"""
        return {
            "current_schema": self._analyze_schema(context),
            "performance_issues": self._identify_bottlenecks(context),
            "optimization_opportunities": self._suggest_improvements(context)
        }
    
    async def execute(self, task: Dict) -> Dict:
        """Execute database-related tasks"""
        task_type = task.get("type")
        
        if task_type == "design_schema":
            return await self._design_schema(task)
        elif task_type == "optimize_query":
            return await self._optimize_query(task)
        elif task_type == "plan_migration":
            return await self._plan_migration(task)
        
    async def _design_schema(self, requirements: Dict) -> Dict:
        """Design database schema based on requirements"""
        # Implementation for schema design
        pass
```

#### 2. Integration Specialist Agent
Create `src/agents/integration_specialist.py`:

```python
class IntegrationSpecialist(BaseAgent):
    """Handles third-party integrations and API connections"""
    
    def __init__(self):
        super().__init__(
            name="Integration Specialist",
            expertise=[
                "api_integration",
                "webhook_setup",
                "auth_configuration",
                "data_synchronization"
            ]
        )
    
    async def integrate_service(self, service: str, config: Dict) -> Dict:
        """Set up integration with external service"""
        integrations = {
            "stripe": self._integrate_stripe,
            "sendgrid": self._integrate_sendgrid,
            "aws": self._integrate_aws,
            "twilio": self._integrate_twilio
        }
        
        if service in integrations:
            return await integrations[service](config)
```

### Registering Sub-Agents

Add your custom agent to the agent registry in `src/agents/__init__.py`:

```python
from .database_architect import DatabaseArchitect
from .integration_specialist import IntegrationSpecialist

AVAILABLE_AGENTS = {
    "database_architect": DatabaseArchitect,
    "integration_specialist": IntegrationSpecialist,
    # ... existing agents
}

def get_agent(agent_type: str):
    """Factory function to create agents"""
    if agent_type in AVAILABLE_AGENTS:
        return AVAILABLE_AGENTS[agent_type]()
    raise ValueError(f"Unknown agent type: {agent_type}")
```

## Configuring Hooks

Hooks automate tasks and maintain code quality throughout development.

### Hook Types

1. **Pre-execution hooks**: Run before commands
2. **Post-execution hooks**: Run after commands
3. **File change hooks**: Triggered on file modifications
4. **Commit hooks**: Run during git operations

### Creating Custom Hooks

#### 1. Pre-Command Hook
Create `hooks/pre-feature-validation.py`:

```python
#!/usr/bin/env python3
"""Validates feature requirements before implementation"""

import sys
import json
from pathlib import Path

def validate_feature(feature_description: str) -> bool:
    """Ensure feature meets project requirements"""
    
    # Check for required keywords
    required_keywords = ["user story", "acceptance criteria", "scope"]
    
    for keyword in required_keywords:
        if keyword not in feature_description.lower():
            print(f"Error: Feature description must include {keyword}")
            return False
    
    # Check against product roadmap
    roadmap = Path("docs/roadmap.md")
    if roadmap.exists():
        # Validate feature aligns with roadmap
        pass
    
    return True

if __name__ == "__main__":
    feature = sys.argv[1] if len(sys.argv) > 1 else ""
    if not validate_feature(feature):
        sys.exit(1)
```

#### 2. Post-Command Hook
Create `hooks/post-code-quality.sh`:

```bash
#!/bin/bash
# Runs quality checks after code changes

echo "Running code quality checks..."

# Python checks
if [ -f "pyproject.toml" ]; then
    echo "→ Running Black formatter..."
    black src/ tests/
    
    echo "→ Running Ruff linter..."
    ruff check src/ tests/
    
    echo "→ Running mypy type checker..."
    mypy src/
fi

# JavaScript/TypeScript checks
if [ -f "package.json" ]; then
    echo "→ Running Prettier..."
    npm run format
    
    echo "→ Running ESLint..."
    npm run lint
fi

# Security scan
echo "→ Running security scan..."
bandit -r src/ || true

echo "✓ Quality checks complete!"
```

#### 3. Smart Hook with Sub-Agent Triggering
Create `hooks/smart-review-trigger.py`:

```python
#!/usr/bin/env python3
"""Intelligently triggers code review based on changes"""

import subprocess
import json
from pathlib import Path

def get_changed_files() -> list[str]:
    """Get list of changed files"""
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split('\n')

def should_trigger_review(files: list[str]) -> tuple[bool, str]:
    """Determine if code review is needed"""
    
    critical_patterns = {
        "security": ["auth", "crypto", "password", "token"],
        "payment": ["stripe", "payment", "billing"],
        "database": ["migration", "schema", "model"]
    }
    
    for file in files:
        for category, patterns in critical_patterns.items():
            if any(pattern in file.lower() for pattern in patterns):
                return True, f"Critical {category} changes detected"
    
    return False, ""

def trigger_review(reason: str):
    """Trigger code review with specific focus"""
    print(f"🔍 Triggering code review: {reason}")
    
    # Create review command
    review_cmd = {
        "command": "/dev:review",
        "focus": reason,
        "files": get_changed_files()
    }
    
    # Write command for Claude to execute
    with open(".claude-commands", "w") as f:
        json.dump(review_cmd, f)

if __name__ == "__main__":
    files = get_changed_files()
    should_review, reason = should_trigger_review(files)
    
    if should_review:
        trigger_review(reason)
```

### Hook Configuration

Configure hooks in `.claude/hooks.yaml`:

```yaml
hooks:
  pre_command:
    - name: "Feature Validation"
      trigger: "/dev:feature"
      script: "hooks/pre-feature-validation.py"
      
  post_command:
    - name: "Code Quality"
      trigger: ["edit", "write"]
      script: "hooks/post-code-quality.sh"
      
  file_change:
    - name: "Smart Review"
      patterns: ["*.py", "*.js", "*.ts"]
      script: "hooks/smart-review-trigger.py"
      
  commit:
    - name: "Pre-commit checks"
      script: "hooks/pre-commit.sh"
      
  custom:
    - name: "Daily standup"
      schedule: "0 9 * * *"
      script: "hooks/daily-standup.py"
```

## Modifying Project Structure

Customize the project structure to match your preferences and requirements.

### Default Structure Modification

Edit `template/project_structure.yaml`:

```yaml
project_structure:
  src:
    project_name:
      # Add custom directories
      api:
        v1:
          endpoints: {}
          schemas: {}
      services:
        business_logic: {}
      repositories:
        data_access: {}
      # Modify existing structure
      core:
        config: {}
        middleware: {}
        exceptions: {}
  
  # Add new top-level directories
  infrastructure:
    terraform: {}
    kubernetes: {}
    docker: {}
  
  scripts:
    deployment: {}
    maintenance: {}
    data: {}
```

### Framework-Specific Templates

#### 1. FastAPI Structure
```yaml
fastapi_structure:
  app:
    api:
      v1:
        endpoints:
          - users.py
          - products.py
          - orders.py
        dependencies:
          - auth.py
          - database.py
    core:
      - config.py
      - security.py
    models:
      - user.py
      - product.py
      - order.py
    schemas:
      - user.py
      - product.py
      - order.py
    services:
      - user_service.py
      - product_service.py
      - order_service.py
```

#### 2. Django Structure
```yaml
django_structure:
  project_name:
    settings:
      - base.py
      - development.py
      - production.py
      - testing.py
    apps:
      users:
        - models.py
        - views.py
        - serializers.py
        - urls.py
      products:
        - models.py
        - views.py
        - serializers.py
        - urls.py
```

## Custom Workflows

Create specialized workflows for your development process.

### Workflow Definition

Create `workflows/feature-development.yaml`:

```yaml
name: "Complete Feature Development"
description: "End-to-end feature implementation with quality gates"

stages:
  - name: "Requirements Analysis"
    agent: "planning_architect"
    outputs:
      - technical_design.md
      - api_specification.yaml
      
  - name: "Implementation"
    parallel: true
    tasks:
      - name: "Backend Development"
        commands:
          - /dev:implement backend
          - /dev:test unit
      - name: "Frontend Development"
        commands:
          - /dev:implement frontend
          - /dev:test components
          
  - name: "Integration"
    commands:
      - /dev:test integration
      - /dev:test e2e
      
  - name: "Quality Assurance"
    agent: "code_reviewer"
    gates:
      - test_coverage: ">= 90%"
      - security_scan: "pass"
      - performance_baseline: "maintained"
      
  - name: "Documentation"
    agent: "documentation_specialist"
    outputs:
      - api_docs_updated
      - user_guide_updated
      - changelog_entry
```

### Custom Workflow Implementation

```python
# src/workflows/custom_workflow.py

class FeatureDevelopmentWorkflow:
    """Orchestrates complete feature development"""
    
    def __init__(self, feature_spec: Dict):
        self.feature_spec = feature_spec
        self.stages = []
        self.current_stage = 0
        
    async def execute(self):
        """Run the complete workflow"""
        for stage in self.stages:
            print(f"Executing stage: {stage.name}")
            
            if stage.parallel:
                await self._execute_parallel(stage.tasks)
            else:
                await self._execute_sequential(stage.tasks)
                
            if not await self._validate_stage(stage):
                raise WorkflowError(f"Stage {stage.name} failed validation")
                
            self.current_stage += 1
```

## Integration Customization

Customize how the template integrates with external tools and services.

### CI/CD Integration

#### GitHub Actions
Create `.github/workflows/ai-enhanced-ci.yml`:

```yaml
name: AI-Enhanced CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Claude Code Review
        run: |
          claude-code review \
            --command "/dev:review" \
            --focus "${{ github.event.pull_request.title }}"
            
      - name: Security Audit
        run: |
          claude-code execute "/security:audit"
          
      - name: Test Generation
        if: contains(github.event.pull_request.labels.*.name, 'needs-tests')
        run: |
          claude-code execute "/dev:test"
```

### IDE Integration

#### VS Code Settings
Create `.vscode/claude-code.json`:

```json
{
  "claude-code": {
    "autoTriggers": {
      "onSave": [
        {
          "pattern": "*.py",
          "command": "format"
        },
        {
          "pattern": "src/**/*.py",
          "command": "/dev:review --quick"
        }
      ],
      "onCommit": {
        "command": "/git:commit"
      }
    },
    "shortcuts": {
      "cmd+shift+f": "/dev:feature",
      "cmd+shift+r": "/dev:review",
      "cmd+shift+t": "/dev:test"
    }
  }
}
```

### External Service Integration

```python
# src/integrations/custom_integrations.py

class CustomIntegrations:
    """Manages external service integrations"""
    
    @staticmethod
    def configure_monitoring():
        """Set up monitoring integrations"""
        return {
            "datadog": {
                "api_key": "from_env",
                "tags": ["claude-code", "ai-enhanced"],
                "custom_metrics": [
                    "ai_suggestions_accepted",
                    "code_quality_score",
                    "auto_fix_success_rate"
                ]
            },
            "sentry": {
                "dsn": "from_env",
                "traces_sample_rate": 0.1,
                "profiles_sample_rate": 0.1
            }
        }
```

## Best Practices for Customization

1. **Start Small**: Begin with simple customizations and gradually add complexity
2. **Document Everything**: Keep your customizations well-documented
3. **Test Thoroughly**: Ensure customizations don't break existing functionality
4. **Share Back**: Consider contributing useful customizations to the community
5. **Version Control**: Track all customization changes in git
6. **Regular Reviews**: Periodically review and update customizations

## Conclusion

The Claude Code Project Template is designed to be highly customizable while maintaining consistency and quality. Use these customization options to create a development environment that perfectly matches your team's needs and workflow.

Remember: The goal is to enhance productivity without adding unnecessary complexity. Choose customizations that provide real value to your development process.