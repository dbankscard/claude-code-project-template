# Project Structure Documentation

## Overview
This document provides a comprehensive overview of the Claude Code Project Template structure and organization.

## Technology Stack
- **Primary Language**: Python 3.12+
- **Framework**: Claude Code AI Development Framework
- **Testing**: pytest, unittest
- **Version Control**: Git with conventional commits
- **CI/CD**: GitHub Actions
- **Documentation**: Markdown with AI-context focus

## Directory Structure

```
project-root/
├── .claude/                    # Claude Code configuration
│   ├── agents/                # Sub-agent definitions
│   │   ├── master-orchestrator.md
│   │   ├── planning-architect.md
│   │   ├── code-reviewer.md
│   │   ├── test-engineer.md
│   │   ├── security-auditor.md
│   │   ├── documentation-specialist.md
│   │   └── performance-optimizer.md
│   ├── commands/             # Custom slash commands
│   │   ├── dev/             # Development commands
│   │   ├── project/         # Project management
│   │   ├── git/             # Git workflows
│   │   └── security/        # Security commands
│   ├── hooks/               # Automation scripts
│   │   ├── auto-format.sh
│   │   ├── command-approval.py
│   │   ├── intelligent-automation.py
│   │   └── security-check.py
│   └── settings.json        # Claude Code settings
├── src/                     # Source code
├── tests/                   # Test suite
├── docs/                    # Documentation
│   ├── guides/             # User guides
│   └── ai-context/         # AI assistant context
├── CLAUDE.md               # AI context and rules
├── .gitignore              # Git ignore patterns
├── pyproject.toml          # Python project config
└── README.md               # Project documentation
```

## Key Components

### Sub-Agents
Each agent in `.claude/agents/` is a specialized AI assistant with specific expertise:
- **master-orchestrator**: Coordinates multi-agent workflows
- **planning-architect**: Technical design and architecture
- **code-reviewer**: Code quality and best practices
- **test-engineer**: Test creation and coverage
- **security-auditor**: Security vulnerability scanning
- **documentation-specialist**: Documentation generation
- **performance-optimizer**: Performance analysis

### Commands
Custom slash commands organized by category:
- **dev/**: Development workflow commands
- **project/**: Project management commands
- **git/**: Version control commands
- **security/**: Security scanning commands

### Hooks
Automated scripts that run at various points:
- **auto-format.sh**: Code formatting on save
- **command-approval.py**: Command safety verification
- **intelligent-automation.py**: Smart agent triggering
- **security-check.py**: Security scanning

## File Naming Conventions
- **Python files**: `snake_case.py`
- **Markdown docs**: `kebab-case.md`
- **Config files**: `lowercase.extension`
- **Test files**: `test_*.py` or `*_test.py`

## Module Organization
- Keep files under 350 lines
- One responsibility per file
- Clear imports and exports
- Logical grouping in subdirectories