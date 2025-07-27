import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture
def temp_project_dir():
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def mock_project_structure(temp_project_dir):
    dirs = [
        ".claude/agents",
        ".claude/commands/dev",
        ".claude/commands/project",
        ".claude/commands/git",
        ".claude/commands/security",
        ".claude/hooks",
        "src",
        "tests",
        "docs/guides",
        "docs/ai-context"
    ]
    
    for dir_path in dirs:
        (temp_project_dir / dir_path).mkdir(parents=True, exist_ok=True)
        
    return temp_project_dir

@pytest.fixture
def sample_agent_content():
    return """# test-agent

## Role
Test agent for unit testing.

## Expertise
- Testing
- Validation

## Activation Triggers
- Test scenarios
- Unit testing needs

## Workflow
1. Analyze test requirements
2. Execute tests
3. Report results
"""

@pytest.fixture
def sample_command_content():
    return """# /test:command

## Usage
/test:command <argument>

## Description
Test command for unit testing.

## Examples
/test:command example

## Process
1. Parse arguments
2. Execute command
3. Return results
"""