# /git:release

Creates comprehensive releases with changelogs, version bumping, and deployment preparation.

## Usage
`/git:release <version> [type]`

## Description
Manages the complete release process including version updates, changelog generation, tagging, and release notes creation.

## Release Types

### Semantic Versioning
- **Major** (1.0.0 → 2.0.0): Breaking changes
- **Minor** (1.0.0 → 1.1.0): New features
- **Patch** (1.0.0 → 1.0.1): Bug fixes
- **Pre-release** (1.0.0 → 1.1.0-beta.1): Beta/RC versions

## Examples

### Create Patch Release
```
/git:release patch
```

### Create Minor Release
```
/git:release minor
```

### Create Specific Version
```
/git:release v2.1.0
```

### Create Pre-release
```
/git:release v2.0.0-beta.1
```

## Release Process

### 1. Version Determination
```bash
# Analyze commits since last release
- Count features → minor bump
- Count fixes → patch bump  
- Breaking changes → major bump
```

### 2. Changelog Generation
```bash
# Generate changelog from commits
- Group by type
- Extract breaking changes
- Include contributor list
```

### 3. Version Updates
```bash
# Update version in files
- package.json
- pyproject.toml
- version.py
- README.md
```

### 4. Release Creation
```bash
# Create release
- Create git tag
- Generate release notes
- Create GitHub release
- Trigger deployment
```

## Changelog Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2024-01-15

### 🎉 Release Highlights
- OAuth2 authentication support
- Performance improvements reducing response time by 40%
- New admin dashboard with analytics
- Enhanced security with rate limiting

### ✨ Added
- **Authentication**: OAuth2 integration with Google and GitHub (#234)
- **Admin**: New admin dashboard with user management (#245)
- **API**: Batch operations endpoint for bulk updates (#256)
- **Security**: Rate limiting on all API endpoints (#267)
- **Monitoring**: Prometheus metrics integration (#278)

### 🐛 Fixed
- **Payment**: Decimal precision errors in order calculations (#301)
- **Cart**: Items disappearing on session timeout (#302)
- **Search**: Special characters causing search failures (#303)
- **UI**: Mobile navigation menu overlap issue (#304)

### ♻️ Changed
- **Performance**: Optimized database queries, 40% faster response times (#289)
- **API**: Standardized error response format across all endpoints (#290)
- **Dependencies**: Updated all dependencies to latest secure versions (#291)

### ⚠️ Deprecated
- **API**: `/api/v1/auth/*` endpoints - use `/api/v2/auth/*` instead
- **Config**: `OLD_SETTING` configuration - use `NEW_SETTING` instead

### 🔥 Removed
- **Feature**: Legacy XML export format (use JSON instead)
- **API**: Deprecated `/api/v1/legacy/*` endpoints

### 🔒 Security
- Fixed potential XSS vulnerability in user input fields (CVE-2024-1234)
- Updated JWT library to patch authentication bypass (CVE-2024-5678)
- Implemented CSRF protection on all state-changing endpoints

### 🚀 Performance
- Database query optimization reducing load time by 40%
- Implemented Redis caching for frequently accessed data
- Added CDN integration for static assets

### 📦 Dependencies
- Updated FastAPI from 0.104.0 to 0.109.0
- Updated PostgreSQL driver to support connection pooling
- Added Redis client for caching layer

### 👥 Contributors
Thanks to all contributors who made this release possible:
- @johndoe - OAuth implementation
- @janesmith - Performance optimization
- @bobwilson - Security fixes
- @alicebrown - Admin dashboard

### 📝 Migration Guide

#### Breaking Changes
None in this release.

#### Database Migrations
```bash
# Run migrations
alembic upgrade head
```

#### Configuration Changes
Add the following to your `.env`:
```bash
# OAuth settings
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# Rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### 📊 Release Statistics
- **Commits**: 89 commits since v2.0.0
- **Changed Files**: 156 files (+4,521 -2,103 lines)
- **Contributors**: 12 contributors
- **Issues Closed**: 34 issues resolved
- **Pull Requests**: 28 PRs merged

---

**Full Changelog**: https://github.com/company/project/compare/v2.0.0...v2.1.0
```

## Release Notes Template

```markdown
# Release v2.1.0

We're excited to announce the release of v2.1.0! This release includes OAuth2 authentication, significant performance improvements, and enhanced security features.

## 🎯 Key Features

### OAuth2 Authentication
Users can now sign in using their Google or GitHub accounts, making registration and login faster and more secure.

### Performance Boost
We've optimized our database queries and implemented intelligent caching, resulting in 40% faster response times across the platform.

### Enhanced Security
- Rate limiting prevents abuse and ensures fair usage
- Updated security headers protect against common attacks
- All dependencies updated to latest secure versions

## 🐛 Important Fixes
- Fixed calculation errors affecting order totals
- Resolved session timeout issues in shopping cart
- Corrected search functionality for special characters

## 📋 Upgrade Instructions

### For Docker Users
```bash
docker pull company/app:2.1.0
docker-compose up -d
```

### For Direct Installation
```bash
git fetch --tags
git checkout v2.1.0
pip install -r requirements.txt
alembic upgrade head
```

### Configuration Updates
Add OAuth configuration to your environment:
```bash
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
```

## ⚠️ Known Issues
- OAuth login may be slow on first attempt while caches warm up
- Some users may need to clear browser cache after upgrade

## 🙏 Acknowledgments
Special thanks to our contributors and the community for their valuable feedback and contributions.

## 📖 Documentation
- [Migration Guide](docs/migration/v2.1.0.md)
- [OAuth Setup Guide](docs/oauth-setup.md)
- [API Documentation](https://api-docs.company.com)

## 💬 Feedback
We'd love to hear your feedback! Please report issues or share suggestions on our [GitHub repository](https://github.com/company/project).

---

**Docker Image**: `company/app:2.1.0`
**PyPI Package**: `company-app==2.1.0`
```

## Version Files Update

### package.json
```json
{
  "name": "myapp",
  "version": "2.1.0",
  "description": "Application description",
  ...
}
```

### pyproject.toml
```toml
[tool.poetry]
name = "myapp"
version = "2.1.0"
description = "Application description"
```

### version.py
```python
"""Version information for myapp"""

__version__ = "2.1.0"
__version_info__ = (2, 1, 0)
__release_date__ = "2024-01-15"
```

## Release Checklist

```markdown
# Release Checklist for v2.1.0

## Pre-release
- [ ] All tests passing on main branch
- [ ] Security scan completed
- [ ] Performance benchmarks acceptable
- [ ] Documentation updated
- [ ] Migration guide written
- [ ] Changelog reviewed
- [ ] Version numbers updated

## Release Process
- [ ] Create release branch
- [ ] Generate changelog
- [ ] Update version files
- [ ] Create git tag
- [ ] Build release artifacts
- [ ] Create GitHub release
- [ ] Publish Docker images
- [ ] Deploy to staging

## Post-release
- [ ] Deploy to production
- [ ] Verify deployment
- [ ] Update status page
- [ ] Send release announcement
- [ ] Monitor error rates
- [ ] Update roadmap
- [ ] Archive release branch
```

## Automation Scripts

### Release Script
```bash
#!/bin/bash
# release.sh

VERSION=$1
TYPE=${2:-minor}

echo "🚀 Creating release $VERSION ($TYPE)"

# Update changelog
echo "📝 Generating changelog..."
conventional-changelog -p angular -i CHANGELOG.md -s

# Update version files
echo "📦 Updating version files..."
npm version $VERSION --no-git-tag-version
sed -i "s/version = .*/version = \"$VERSION\"/" pyproject.toml
sed -i "s/__version__ = .*/__version__ = \"$VERSION\"/" src/version.py

# Commit changes
echo "💾 Committing changes..."
git add .
git commit -m "chore(release): $VERSION"

# Create tag
echo "🏷️ Creating tag..."
git tag -a "v$VERSION" -m "Release v$VERSION"

# Push changes
echo "⬆️ Pushing to remote..."
git push origin main
git push origin "v$VERSION"

# Create GitHub release
echo "📦 Creating GitHub release..."
gh release create "v$VERSION" \
  --title "Release v$VERSION" \
  --notes-file RELEASE_NOTES.md \
  --draft

echo "✅ Release draft created! Please review and publish."
```

### Version Bump Config
```yaml
# .versionrc.json
{
  "types": [
    {"type": "feat", "section": "✨ Features"},
    {"type": "fix", "section": "🐛 Bug Fixes"},
    {"type": "perf", "section": "🚀 Performance"},
    {"type": "docs", "section": "📝 Documentation"},
    {"type": "chore", "hidden": true}
  ],
  "releaseCommitMessageFormat": "chore(release): {{currentTag}}",
  "bumpFiles": [
    {
      "filename": "package.json",
      "type": "json"
    },
    {
      "filename": "pyproject.toml",
      "updater": "scripts/toml-updater.js"
    },
    {
      "filename": "src/version.py",
      "updater": "scripts/python-updater.js"
    }
  ]
}
```

## Deployment Integration

### GitHub Actions
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build artifacts
        run: |
          npm run build
          docker build -t myapp:${{ github.ref_name }} .
      
      - name: Run tests
        run: |
          npm test
          docker run myapp:${{ github.ref_name }} test
      
      - name: Publish to registry
        run: |
          docker push myapp:${{ github.ref_name }}
          npm publish
      
      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp myapp=myapp:${{ github.ref_name }}
```

## Options

- `--draft`: Create draft release
- `--prerelease`: Mark as pre-release
- `--branch`: Release from specific branch
- `--no-changelog`: Skip changelog generation
- `--dry-run`: Preview without creating

## Best Practices

### 1. Release Planning
- Schedule releases regularly
- Communicate release dates
- Feature freeze before release
- Test in staging first

### 2. Version Management
- Follow semantic versioning
- Keep changelog updated
- Tag all releases
- Document breaking changes

### 3. Quality Gates
- All tests must pass
- Security scan clean
- Performance benchmarks met
- Documentation complete

## Related Commands

- `/git:commit` - Create release commits
- `/project:status` - Check release readiness
- `/project:deploy` - Deploy release
- `/git:hotfix` - Create hotfix from release