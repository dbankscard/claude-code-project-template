# /dev:review

Performs comprehensive code review with quality, security, and performance analysis.

## Usage
`/dev:review [file-or-directory]`

## Description
Triggers the Code Reviewer agent to analyze code for quality, security vulnerabilities, performance issues, and adherence to best practices.

## Review Scope

### When No Path Specified
- Reviews all changed files since last commit
- Focuses on modified code sections
- Checks related test coverage

### When Path Specified
- Reviews all files in specified path
- Performs deep analysis
- Suggests refactoring opportunities

## Review Categories

### 1. Code Quality
- **Style Compliance**: Formatting, naming conventions
- **Complexity**: Cyclomatic complexity, cognitive load
- **Duplication**: DRY principle violations
- **Maintainability**: Code clarity and organization

### 2. Security
- **Input Validation**: SQL injection, XSS prevention
- **Authentication**: Proper access controls
- **Data Protection**: Encryption, secure storage
- **Dependencies**: Known vulnerabilities

### 3. Performance
- **Algorithm Efficiency**: Time/space complexity
- **Database Queries**: N+1 problems, missing indexes
- **Memory Usage**: Leaks, excessive allocation
- **Caching**: Opportunities for optimization

### 4. Best Practices
- **SOLID Principles**: Adherence check
- **Design Patterns**: Proper implementation
- **Error Handling**: Comprehensive coverage
- **Testing**: Adequate test coverage

## Examples

### Review Current Changes
```
/dev:review
```

### Review Specific Module
```
/dev:review src/api/
```

### Review Single File
```
/dev:review src/services/payment_service.py
```

## Output Format

```markdown
# Code Review Report

## Summary
- Files Reviewed: 12
- Issues Found: 3 Critical, 7 Major, 15 Minor
- Code Quality Score: B+ (85/100)

## Critical Issues
1. SQL Injection vulnerability in user_service.py:45
2. Hardcoded API key in config.py:23
3. Missing authentication on DELETE endpoint

## Recommendations
[Detailed findings and fixes...]
```

## Options

- `--focus`: Specific aspect to focus on (security/performance/quality)
- `--strict`: Use stricter review criteria
- `--auto-fix`: Automatically fix simple issues
- `--compare`: Compare with another branch

## Integration

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
claude code "/dev:review --auto-fix"
```

### CI/CD Pipeline
```yaml
- name: Claude Code Review
  run: claude code "/dev:review --strict"
```

## Review Metrics

- **Complexity Threshold**: 10 (cyclomatic)
- **Coverage Requirement**: 80% minimum
- **Performance Budget**: <100ms response time
- **Security Level**: OWASP Top 10 compliance

## Follow-up Actions

After review completion:
1. Address critical issues immediately
2. Plan refactoring for major issues
3. Track technical debt
4. Update coding standards if needed

## Related Commands

- `/dev:refactor` - Implement review suggestions
- `/security:audit` - Deep security analysis
- `/dev:test` - Improve test coverage
- `/git:commit` - Commit reviewed changes