# /git:commit

Creates intelligent, conventional commits with detailed messages based on changes.

## Usage
`/git:commit [message]`

## Description
Analyzes code changes and creates well-structured commit messages following conventional commit standards, including change summaries and context.

## Commit Types

### Conventional Commit Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Test additions/modifications
- **build**: Build system changes
- **ci**: CI configuration changes
- **chore**: Maintenance tasks

## Examples

### Auto-generated Commit
```
/git:commit
```
Analyzes changes and creates appropriate commit message

### Custom Message
```
/git:commit "Add user authentication with OAuth2 support"
```

### Breaking Change
```
/git:commit "Refactor API endpoints" --breaking
```

## Commit Analysis Process

### 1. Change Detection
```bash
# Analyze what changed
- Modified files
- Added/deleted files  
- Line changes
- Function/class changes
```

### 2. Context Understanding
```bash
# Understand the context
- Related issue/ticket
- Previous commits
- Code purpose
- Impact analysis
```

### 3. Message Generation
```bash
# Create structured message
- Determine commit type
- Identify scope
- Write clear subject
- Add detailed body
```

## Commit Message Examples

### Feature Commit
```
feat(auth): Add OAuth2 authentication support

- Implement Google OAuth2 integration
- Add Facebook login support  
- Create OAuth callback handlers
- Update user model for social auth
- Add configuration for OAuth providers

Closes #234
```

### Bug Fix Commit
```
fix(payment): Resolve decimal precision in order calculations

The order total calculation was losing precision when dealing
with multiple items and tax calculations. This fix:

- Uses Decimal type for all monetary values
- Rounds at the final step only
- Adds unit tests for edge cases

The issue was causing penny differences in some orders,
particularly those with many items or complex tax rules.

Fixes #456
```

### Breaking Change Commit
```
refactor(api)!: Restructure authentication endpoints

BREAKING CHANGE: Authentication endpoints have been reorganized
for better consistency and security.

Migration required:
- POST /auth/login -> POST /api/v2/auth/login
- POST /auth/logout -> POST /api/v2/auth/logout  
- GET /auth/verify -> GET /api/v2/auth/verify
- Token format changed from JWT to Paseto

Before:
```http
POST /auth/login
{
  "username": "user",
  "password": "pass"
}
```

After:
```http
POST /api/v2/auth/login
{
  "email": "user@example.com",
  "password": "pass",
  "device_id": "optional"
}
```

This change improves security and allows for better
session management across devices.
```

### Multi-scope Commit
```
feat(ui,api): Implement real-time notifications

Frontend changes:
- Add WebSocket connection manager
- Create notification component
- Implement notification preferences UI
- Add notification sound settings

Backend changes:
- Set up WebSocket server
- Create notification service
- Add notification queue with Redis
- Implement notification delivery logic

This enables real-time updates for:
- Order status changes
- New messages
- System announcements
- Price alerts

Part of #789
```

## Commit Best Practices

### Subject Line Rules
1. **Limit to 50 characters**
2. **Start with lowercase**
3. **No period at end**
4. **Use imperative mood**
5. **Be specific and clear**

### Body Guidelines
1. **Wrap at 72 characters**
2. **Explain what and why**
3. **Reference issues/tickets**
4. **Include migration steps**
5. **List breaking changes**

### Good vs Bad Examples

❌ **Bad**:
```
Fixed stuff
Update code
Changes
Work on feature
```

✅ **Good**:
```
fix(cart): Prevent negative quantities in cart items
feat(search): Add fuzzy search with Elasticsearch
refactor(auth): Extract token validation to middleware
docs(api): Update endpoint documentation for v2
```

## Automated Checks

### Pre-commit Validation
```python
def validate_commit_message(message):
    """Validate commit message format"""
    
    # Check conventional format
    pattern = r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore)(\(.+\))?: .{1,50}'
    if not re.match(pattern, message.split('\n')[0]):
        return False, "Invalid format. Use: type(scope): subject"
    
    # Check subject length
    subject = message.split('\n')[0]
    if len(subject) > 72:
        return False, "Subject line too long (max 72 chars)"
    
    # Check imperative mood
    if subject.split(': ')[1][0].isupper():
        return False, "Use lowercase start in subject"
    
    return True, "Valid commit message"
```

### Commit Hooks Integration
```bash
#!/bin/bash
# .git/hooks/prepare-commit-msg

# Run Claude commit message generator
if [ -z "$2" ]; then
    claude code "/git:commit" > .git/COMMIT_EDITMSG
fi
```

## Smart Features

### Issue Linking
Automatically detects and links related issues:
- GitHub: `Fixes #123`, `Closes #456`
- Jira: `PROJ-123`, `Resolves PROJ-456`
- GitLab: `Closes #123`, `Related to #456`

### Co-author Detection
```
Co-authored-by: Jane Doe <jane@example.com>
Co-authored-by: John Smith <john@example.com>
```

### Semantic Versioning
Suggests version bumps based on commits:
- `feat`: Minor version bump (1.0.0 → 1.1.0)
- `fix`: Patch version bump (1.0.0 → 1.0.1)
- `feat!` or `BREAKING`: Major version bump (1.0.0 → 2.0.0)

## Configuration

### Project Rules (.gitmessage)
```
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>
#
# Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore
# Scope: component or file affected
# Subject: imperative, lowercase, no period, <50 chars
# Body: explain what and why, wrap at 72 chars
# Footer: references, breaking changes
```

### Custom Types
```yaml
# .claude/commit-types.yaml
types:
  - name: security
    description: Security fixes and improvements
    emoji: 🔒
  - name: ux
    description: User experience improvements
    emoji: 🎨
  - name: a11y
    description: Accessibility improvements
    emoji: ♿
```

## Options

- `--type`: Force specific commit type
- `--scope`: Set commit scope
- `--breaking`: Mark as breaking change
- `--no-verify`: Skip pre-commit hooks
- `--amend`: Amend previous commit

## Integration

### CI/CD Pipeline
```yaml
# Validate commit messages in CI
- name: Validate Commits
  run: |
    npx commitlint --from=origin/main --to=HEAD
```

### Release Notes
Automatically generate release notes from commits:
```markdown
## [2.1.0] - 2024-01-15

### Features
- auth: Add OAuth2 authentication support (#234)
- search: Implement fuzzy search with Elasticsearch (#245)

### Bug Fixes
- payment: Resolve decimal precision in calculations (#456)
- cart: Prevent negative quantities (#467)

### Breaking Changes
- api: Restructure authentication endpoints
```

## Related Commands

- `/git:pr` - Create pull request
- `/git:release` - Create release
- `/dev:review` - Review before commit
- `/project:status` - Check commit status