---
name: test
namespace: dev
description: Testing workflow with test-engineer agent
---

# Test Command

Manages testing workflows and ensures comprehensive test coverage.

## Usage
```
/dev:test [--type unit|integration|e2e|all] [--coverage] [--fix]
```

## Test Workflow
1. **Analysis**: Identifies what needs testing
2. **Generation**: Creates missing tests
3. **Execution**: Runs test suite
4. **Coverage**: Analyzes test coverage
5. **Fixes**: Repairs failing tests if requested

## Options
- `--type`: Type of tests to run (default: all)
- `--coverage`: Generate coverage report
- `--fix`: Attempt to fix failing tests

## Examples
```
/dev:test --type unit --coverage
/dev:test --fix  # Fix failing tests
```

## Features
- Automatic test discovery
- Parallel test execution
- Coverage gap identification
- Test generation for uncovered code
- Failing test diagnosis and fixes