# /project:status

Provides comprehensive project status including progress, metrics, and health indicators.

## Usage
`/project:status [component]`

## Description
Generates a detailed status report of the project, including development progress, code quality metrics, test coverage, and system health.

## Status Categories

### 1. Development Progress
- Feature completion
- Sprint progress
- Milestone tracking
- Blocker identification

### 2. Code Quality
- Test coverage
- Code complexity
- Technical debt
- Security issues

### 3. System Health
- Performance metrics
- Error rates
- Uptime statistics
- Resource usage

### 4. Team Metrics
- Velocity trends
- PR statistics
- Issue resolution
- Documentation coverage

## Examples

### Overall Project Status
```
/project:status
```

### Specific Component Status
```
/project:status authentication
```

### Sprint Status
```
/project:status sprint
```

### Production Health
```
/project:status production
```

## Status Report Format

### Executive Summary
```markdown
# Project Status Report

**Date**: 2024-01-15
**Sprint**: 14 (Week 2 of 2)
**Release Target**: v2.1.0 (2024-01-31)

## 🎯 Summary

- **Overall Health**: 🟢 Good
- **Sprint Progress**: 78% complete (11/14 stories)
- **Release Readiness**: 🟡 On Track with Risks
- **Critical Issues**: 2 blockers identified

## 📊 Key Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Feature Completion | 85% | 100% | 🟡 |
| Test Coverage | 91.2% | 90% | 🟢 |
| Performance (p95) | 145ms | <200ms | 🟢 |
| Tech Debt | 12.3% | <15% | 🟢 |
| Open Bugs | 23 | <30 | 🟢 |
```

### Development Progress
```markdown
## 🚀 Development Progress

### Current Sprint (Sprint 14)

#### Completed (11/14)
- ✅ FEAT-401: User profile management
- ✅ FEAT-402: OAuth2 integration
- ✅ FEAT-403: Password reset flow
- ✅ BUG-201: Fix cart calculation
- ✅ TECH-101: Database optimization
- ✅ FEAT-404: Email notifications
- ✅ TEST-301: Integration test suite
- ✅ DOC-201: API documentation
- ✅ FEAT-405: Admin dashboard
- ✅ SEC-101: Security audit fixes
- ✅ PERF-201: Query optimization

#### In Progress (2/14)
- 🔄 FEAT-406: Payment webhook handling (80% - @john)
- 🔄 FEAT-407: Mobile push notifications (60% - @sarah)

#### Blocked (1/14)
- 🔴 FEAT-408: Third-party API integration
  - **Blocker**: Waiting for API credentials
  - **Impact**: 2-day delay expected
  - **Mitigation**: Working with vendor

### Velocity Trend
```
Sprint 11: ████████████████████ 20 points
Sprint 12: ██████████████████ 18 points  
Sprint 13: █████████████████████ 21 points
Sprint 14: ████████████████ 16 points (projected)
```

### Burndown Chart
```
Story Points
25 |█
   |██
20 |███
   |████
15 |█████
   |██████
10 |███████████
   |█████████████
5  |███████████████████
   |█████████████████████████
0  |_________________________
   Mon  Tue  Wed  Thu  Fri
   
   ━━━ Ideal
   ███ Actual
```
```

### Code Quality Report
```markdown
## 📈 Code Quality Metrics

### Test Coverage
```
Overall Coverage: 91.2% ✅

├── services/
│   ├── auth/        94.3% ✅
│   ├── product/     92.1% ✅
│   ├── order/       89.7% 🟡
│   └── payment/     90.5% ✅
├── shared/          93.8% ✅
└── utils/           87.2% 🟡
```

### Code Complexity
```
Cyclomatic Complexity Analysis:
- Low (1-5):      72% ████████████████
- Medium (6-10):  23% █████
- High (11-15):    4% █
- Very High (>15): 1% ▌

Files needing refactoring:
1. order_service.py - complexity: 18
2. payment_processor.py - complexity: 16
3. report_generator.py - complexity: 15
```

### Technical Debt
```
Technical Debt Ratio: 12.3%

By Category:
- Code Smells:      45 issues
- Vulnerabilities:   2 issues  🔴
- Security Hotspots: 8 issues  🟡
- Duplications:     3.2%

Debt Timeline:
- Added this sprint:   2.1 hours
- Removed this sprint: 5.3 hours
- Net improvement:     3.2 hours ✅
```

### Security Status
```
Security Scan Results:

Critical:  0 ✅
High:      2 🔴 (addressing)
Medium:    5 🟡
Low:       12 ℹ️

Recent Actions:
- Fixed SQL injection vulnerability
- Updated dependencies (3 critical)
- Implemented CSRF protection
- Added rate limiting

Pending:
- Implement CSP headers
- Update JWT library
```
```

### System Health Dashboard
```markdown
## 🏥 System Health

### Production Metrics (Last 24h)

#### Availability
```
Uptime: 99.98% (1m 44s downtime)

Service Availability:
- API Gateway:    99.99% ✅
- Auth Service:   99.98% ✅
- Product Service: 99.97% ✅
- Order Service:  99.99% ✅
- Payment Service: 100%   ✅
```

#### Performance
```
Response Times (p50/p95/p99):
- GET /products:     42ms / 145ms / 289ms ✅
- POST /orders:      89ms / 234ms / 456ms ✅
- GET /users/me:     23ms / 67ms / 125ms  ✅
- POST /auth/login:  156ms / 312ms / 498ms 🟡

Throughput:
- Requests/sec: 2,847 (avg)
- Peak: 4,231 req/s
- Success rate: 99.7%
```

#### Error Rates
```
Error Summary (Last 24h):
- 5xx errors: 0.08% (23 total) ✅
- 4xx errors: 2.1% (612 total) ✅
- Timeout errors: 0.02% (6 total) ✅

Top Errors:
1. 404 Not Found - 387 occurrences
2. 401 Unauthorized - 156 occurrences  
3. 400 Bad Request - 69 occurrences
```

#### Resource Usage
```
Infrastructure Metrics:

CPU Usage:
- API pods:     45% average, 78% peak ✅
- Database:     38% average, 62% peak ✅
- Cache:        12% average, 23% peak ✅

Memory Usage:
- API pods:     2.3GB / 4GB (57%) ✅
- Database:     18GB / 32GB (56%) ✅
- Cache:        4.8GB / 8GB (60%) ✅

Disk I/O:
- Database: 124 MB/s read, 89 MB/s write
- Logs: 12 MB/s write
```
```

### Deployment History
```markdown
## 🚢 Recent Deployments

### Production Deployments (Last 30 days)

| Date | Version | Type | Duration | Status | Rollbacks |
|------|---------|------|----------|--------|-----------|
| 2024-01-14 | v2.0.8 | Hotfix | 4m 23s | ✅ Success | 0 |
| 2024-01-12 | v2.0.7 | Feature | 8m 12s | ✅ Success | 0 |
| 2024-01-08 | v2.0.6 | Feature | 7m 45s | ✅ Success | 0 |
| 2024-01-05 | v2.0.5 | Bugfix | 5m 11s | 🔴 Failed | 1 |
| 2024-01-05 | v2.0.5 | Bugfix | 6m 32s | ✅ Success | 0 |

Deployment Success Rate: 94.7% (18/19)
Average Deployment Time: 6m 47s
```

### Team Activity
```markdown
## 👥 Team Metrics

### Pull Request Statistics (Last 7 days)
- Opened: 23
- Merged: 19
- Closed without merge: 2
- Average time to merge: 4.2 hours
- Average reviews per PR: 2.3

### Code Review Metrics
- Average first response: 45 minutes
- Review coverage: 98%
- Post-merge issues: 1

### Contributor Activity
```
John     ████████████████████ 89 commits
Sarah    ███████████████      67 commits
Mike     ████████████         52 commits
Lisa     ██████████           43 commits
Ahmed    ████████             34 commits
```

### Issue Resolution
- Created this week: 34
- Resolved this week: 41
- Average resolution time: 2.3 days
- Backlog size: 78 issues
```

### Recommendations
```markdown
## 📋 Recommendations & Actions

### Immediate Actions Required
1. **🔴 Resolve API Integration Blocker**
   - Contact vendor for credentials
   - Implement mock for testing
   - Target: EOD today

2. **🟡 Address High Security Issues**
   - Update JWT library (CVE-2024-1234)
   - Implement CSP headers
   - Target: Before release

### Performance Optimization
1. **Login Endpoint Optimization**
   - Current: 312ms (p95)
   - Target: <200ms
   - Action: Implement connection pooling

2. **Database Query Optimization**
   - Identified 3 slow queries
   - Add missing indexes
   - Estimated improvement: 40%

### Technical Debt
1. **Refactor Complex Methods**
   - order_service.py: Split calculate_total()
   - payment_processor.py: Extract validation logic
   - Target: Next sprint

### Process Improvements
1. **Deployment Automation**
   - Implement automated rollback
   - Add smoke tests
   - Reduce deployment time to <5 minutes

## 📅 Upcoming Milestones

| Milestone | Date | Status | Confidence |
|-----------|------|--------|------------|
| Feature Freeze | 2024-01-20 | On Track | 85% |
| Code Freeze | 2024-01-25 | On Track | 80% |
| Release v2.1.0 | 2024-01-31 | At Risk | 70% |
```

## Status Indicators

### Health Indicators
- 🟢 **Good**: Meeting or exceeding targets
- 🟡 **Warning**: Close to thresholds, needs attention
- 🔴 **Critical**: Immediate action required
- ℹ️ **Info**: For awareness only

### Progress Tracking
- ✅ Complete
- 🔄 In Progress
- 🔴 Blocked
- ⏸️ On Hold
- 📅 Scheduled

## Options

- `--format`: Output format (markdown/json/html)
- `--period`: Time period (today/week/sprint/month)
- `--detail`: Level of detail (summary/normal/detailed)
- `--component`: Specific component to analyze

## Integration

### Slack Notifications
```python
# Daily status update
@scheduled(cron="0 9 * * *")
def daily_status_update():
    status = generate_project_status()
    slack.post_message(
        channel="#project-status",
        text=f"Daily Status: {status.summary}",
        attachments=[status.details]
    )
```

### Dashboard Export
```bash
# Export to monitoring dashboard
/project:status --format=json | \
  curl -X POST https://metrics.internal/api/import \
  -H "Content-Type: application/json" \
  -d @-
```

## Related Commands

- `/project:plan` - View project plans
- `/dev:review` - Code quality details
- `/security:audit` - Security status
- `/git:release` - Release readiness