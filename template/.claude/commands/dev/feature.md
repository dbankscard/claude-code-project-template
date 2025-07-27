---
name: feature
namespace: dev
description: Create a new feature with full development workflow
---

# Feature Development Command

This command orchestrates the complete feature development workflow.

## Usage
```
/dev:feature <feature-name> [--description "Feature description"]
```

## Workflow
1. **Planning**: Invokes planning-architect to design the feature
2. **Implementation**: Guides through TDD implementation
3. **Review**: Triggers code-reviewer for quality checks
4. **Testing**: Ensures comprehensive test coverage
5. **Documentation**: Updates relevant documentation
6. **Security**: Runs security audit if needed

## Example
```
/dev:feature user-authentication --description "Add OAuth2 authentication with Google and GitHub providers"
```

## Actions
- Creates feature branch
- Sets up initial file structure
- Triggers master-orchestrator for complex features
- Runs all quality checks
- Prepares for PR creation