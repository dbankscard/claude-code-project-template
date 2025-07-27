# /git:pr

Creates comprehensive pull requests with detailed descriptions, checklists, and context.

## Usage
`/git:pr [title] [base-branch]`

## Description
Generates pull requests with rich descriptions including change summaries, testing instructions, screenshots, and review checklists.

## PR Components

### 1. Title
- Clear and descriptive
- Includes ticket/issue reference
- Follows naming convention

### 2. Description
- Summary of changes
- Motivation and context
- Technical approach
- Testing performed

### 3. Checklists
- Code quality checks
- Testing coverage
- Documentation updates
- Review guidelines

## Examples

### Create PR from Current Branch
```
/git:pr
```

### Custom Title
```
/git:pr "Add user authentication system"
```

### Specific Base Branch
```
/git:pr "Feature: Payment integration" develop
```

### Hotfix PR
```
/git:pr "Hotfix: Critical security patch" main --hotfix
```

## PR Template

```markdown
# [FEAT-123] Add User Authentication System

## 🎯 Summary

This PR implements a complete user authentication system with JWT tokens, OAuth2 support, and comprehensive security features.

### What does this PR do?
- ✅ Implements JWT-based authentication
- ✅ Adds OAuth2 integration (Google, GitHub)
- ✅ Creates user registration and login endpoints
- ✅ Implements password reset functionality
- ✅ Adds rate limiting and security headers

### Why is this needed?
Currently, the application lacks user authentication, which is required for:
- Personalizing user experience
- Securing API endpoints
- Managing user permissions
- Tracking user activity

## 🔄 Changes

### New Features
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Token refresh
- `POST /api/auth/reset-password` - Password reset
- `GET /api/auth/oauth/{provider}` - OAuth initiation
- `GET /api/auth/oauth/{provider}/callback` - OAuth callback

### Modified Files
```diff
+ src/auth/
+   ├── __init__.py
+   ├── models.py (User model)
+   ├── schemas.py (Pydantic schemas)
+   ├── service.py (Auth business logic)
+   ├── router.py (FastAPI routes)
+   ├── dependencies.py (Auth dependencies)
+   └── utils.py (JWT, hashing utilities)
  
~ src/main.py (Added auth router)
~ src/config.py (Added auth configuration)
~ requirements.txt (Added auth dependencies)
+ tests/auth/ (Complete test suite)
```

### Database Changes
```sql
-- New tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE oauth_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,
    provider_user_id VARCHAR(255) NOT NULL,
    UNIQUE(provider, provider_user_id)
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_oauth_provider ON oauth_accounts(provider, provider_user_id);
```

## 🧪 Testing

### Test Coverage
- Unit tests: 95% coverage
- Integration tests: All endpoints tested
- Security tests: OWASP Top 10 validated

### How to Test
1. **Manual Testing**
   ```bash
   # Start the server
   docker-compose up
   
   # Register a new user
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "SecurePass123!"}'
   
   # Login
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "SecurePass123!"}'
   ```

2. **Automated Tests**
   ```bash
   # Run all tests
   pytest tests/auth/
   
   # Run with coverage
   pytest tests/auth/ --cov=src/auth
   ```

3. **OAuth Testing**
   - Visit http://localhost:8000/api/auth/oauth/google
   - Complete OAuth flow
   - Verify user creation and login

### Test Results
```
============================= test session starts ==============================
collected 47 items

tests/auth/test_models.py::test_user_creation PASSED                    [  2%]
tests/auth/test_models.py::test_password_hashing PASSED                 [  4%]
tests/auth/test_service.py::test_register_user PASSED                   [  6%]
tests/auth/test_service.py::test_login_user PASSED                      [  8%]
tests/auth/test_service.py::test_invalid_credentials PASSED             [ 10%]
tests/auth/test_router.py::test_register_endpoint PASSED                [ 12%]
... (all tests passing)

============================== 47 passed in 3.21s ==============================

Coverage Report:
Name                     Stmts   Miss  Cover
--------------------------------------------
src/auth/__init__.py         3      0   100%
src/auth/models.py          45      2    96%
src/auth/schemas.py         38      0   100%
src/auth/service.py         92      4    96%
src/auth/router.py          67      3    96%
src/auth/dependencies.py    28      1    96%
src/auth/utils.py           41      2    95%
--------------------------------------------
TOTAL                      314     12    96%
```

## 📸 Screenshots

### Login Page
![Login Page](https://user-images.githubusercontent.com/login-page.png)

### OAuth Flow
![OAuth Flow](https://user-images.githubusercontent.com/oauth-flow.png)

### Password Reset
![Password Reset](https://user-images.githubusercontent.com/password-reset.png)

## 🔒 Security Considerations

### Implemented Security Measures
- ✅ Password hashing with bcrypt (cost factor: 12)
- ✅ JWT tokens with short expiry (15 minutes)
- ✅ Refresh tokens with rotation
- ✅ Rate limiting (5 attempts per minute)
- ✅ CSRF protection
- ✅ Secure headers (HSTS, CSP, etc.)
- ✅ Input validation and sanitization

### Security Checklist
- [x] No hardcoded secrets
- [x] Environment variables for configuration
- [x] SQL injection prevention
- [x] XSS protection
- [x] Secure password requirements enforced
- [x] Account lockout after failed attempts
- [x] Audit logging for auth events

## 📋 PR Checklist

### Code Quality
- [x] Code follows project style guidelines
- [x] No linting errors (`flake8`, `mypy`)
- [x] Functions have docstrings
- [x] Complex logic is commented
- [x] No code duplication

### Testing
- [x] All new code has tests
- [x] All tests pass locally
- [x] Test coverage > 90%
- [x] Integration tests included
- [x] Edge cases covered

### Documentation
- [x] API documentation updated
- [x] README updated with setup instructions
- [x] Environment variables documented
- [x] Migration guide provided
- [x] Swagger/OpenAPI specs updated

### Performance
- [x] No N+1 queries
- [x] Database queries optimized
- [x] Caching implemented where appropriate
- [x] Load tested with expected traffic

### Deployment
- [x] Database migrations included
- [x] Backward compatible (or breaking changes documented)
- [x] Feature flags for gradual rollout
- [x] Rollback plan documented

## 🚀 Deployment Notes

### Environment Variables Required
```bash
# JWT Configuration
JWT_SECRET_KEY=<generate-secure-key>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

# OAuth Providers
GOOGLE_CLIENT_ID=<from-google-console>
GOOGLE_CLIENT_SECRET=<from-google-console>
GITHUB_CLIENT_ID=<from-github-settings>
GITHUB_CLIENT_SECRET=<from-github-settings>

# Security
BCRYPT_ROUNDS=12
RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW=60
```

### Migration Commands
```bash
# Run migrations
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Feature Flags
```json
{
  "oauth_enabled": true,
  "registration_enabled": true,
  "password_reset_enabled": true
}
```

## 🔗 Related Issues

- Closes #123: Implement user authentication
- Closes #124: Add OAuth2 support
- Closes #125: Password reset functionality
- Addresses #126: Security hardening

## 👥 Reviewers

@security-team - Please review security implementation
@backend-team - Please review API design
@frontend-team - Please review integration points

## 📝 Additional Notes

- This PR is part of the Q1 authentication milestone
- Follow-up PR will add 2FA support
- Frontend integration PR: #456
- Mobile app integration tracked in #457

---

**Ready for review!** 🎉
```

## PR Types

### Feature PR
```markdown
## 🎯 Summary
This PR implements [feature description] to enable [business value].

### User Story
As a [user type], I want to [action] so that [benefit].

### Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Criteria 3
```

### Bug Fix PR
```markdown
## 🐛 Bug Description
[What was broken]

### Root Cause
[Why it was broken]

### Solution
[How it was fixed]

### Testing
[How to verify the fix]
```

### Refactoring PR
```markdown
## 🔧 Refactoring Summary
This PR refactors [component] to improve [metric].

### Before
[Problems with current implementation]

### After
[Improvements made]

### Performance Impact
[Benchmark results]
```

## PR Best Practices

### Title Format
```
[TYPE-ID] Brief description

Examples:
[FEAT-123] Add user authentication
[BUG-456] Fix cart calculation error
[REFACTOR] Improve database query performance
[DOCS] Update API documentation
```

### Description Guidelines
1. **Start with summary**
2. **Explain the why**
3. **List all changes**
4. **Include testing steps**
5. **Add screenshots**
6. **Reference issues**

### Review Guidelines
```markdown
## 🔍 Review Focus Areas

### For Reviewers
Please pay special attention to:
1. Security implementation in `auth/service.py`
2. Database migration compatibility
3. Error handling in OAuth flow
4. Performance of user lookup queries

### Questions for Reviewers
1. Should we add rate limiting to OAuth endpoints?
2. Is 15 minutes appropriate for token expiry?
3. Should we log failed login attempts?
```

## Automation

### PR Template
Save as `.github/pull_request_template.md`:
```markdown
## Summary
<!-- Brief description of changes -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

### Auto-labeling
```yaml
# .github/labeler.yml
frontend:
  - src/frontend/**/*
  
backend:
  - src/backend/**/*
  
documentation:
  - docs/**/*
  - '**/*.md'
  
tests:
  - tests/**/*
  - '**/*.test.js'
  - '**/*.spec.py'
```

## Options

- `--draft`: Create draft PR
- `--reviewers`: Specify reviewers
- `--labels`: Add labels
- `--milestone`: Assign milestone
- `--base`: Target branch

## Related Commands

- `/git:commit` - Create commits
- `/dev:review` - Pre-PR review
- `/git:release` - Create release
- `/project:status` - Check PR status