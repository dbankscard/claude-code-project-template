---
name: commit
namespace: git
description: Smart commit with conventional commit messages
---

# Git Commit Command

Creates well-formatted commits following conventional commit standards.

## Usage
```
/git:commit [--type feat|fix|docs|style|refactor|test|chore] [--scope component] [--breaking]
```

## Commit Process
1. **Change Analysis**: Reviews staged changes
2. **Message Generation**: Creates conventional commit message
3. **Validation**: Ensures commit standards
4. **Hook Execution**: Runs pre-commit hooks

## Options
- `--type`: Commit type (auto-detected if not specified)
- `--scope`: Component scope of changes
- `--breaking`: Mark as breaking change

## Conventional Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build/tool changes

## Example
```
/git:commit --type feat --scope auth
```