---
name: review
namespace: dev
description: Comprehensive code review workflow
---

# Code Review Command

Triggers a comprehensive code review using specialized sub-agents.

## Usage
```
/dev:review [--scope all|staged|branch] [--depth quick|standard|deep]
```

## Review Process
1. **Code Quality**: Reviews code style, patterns, and best practices
2. **Security**: Checks for vulnerabilities and security issues
3. **Performance**: Identifies potential bottlenecks
4. **Tests**: Verifies test coverage and quality
5. **Documentation**: Ensures docs are updated

## Options
- `--scope`: What to review (default: staged)
  - `all`: Review all project files
  - `staged`: Review staged changes only
  - `branch`: Review all changes in current branch
- `--depth`: Review thoroughness (default: standard)
  - `quick`: Fast review of critical issues
  - `standard`: Normal review process
  - `deep`: Extensive analysis including edge cases

## Example
```
/dev:review --scope branch --depth deep
```