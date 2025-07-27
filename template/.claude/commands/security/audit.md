# /security:audit

Performs comprehensive security audits to identify vulnerabilities and ensure compliance.

## Usage
`/security:audit [scope] [standard]`

## Description
Triggers the Security Auditor agent to perform in-depth security analysis, checking for vulnerabilities, compliance issues, and security best practices.

## Audit Scope

### 1. Code Security
- Static analysis (SAST)
- Dependency scanning
- Secret detection
- Injection vulnerabilities

### 2. Infrastructure Security
- Configuration review
- Access controls
- Network security
- Encryption status

### 3. Compliance
- OWASP Top 10
- PCI DSS
- GDPR
- SOC 2
- HIPAA

### 4. Authentication & Authorization
- Password policies
- Token security
- Session management
- Access control

## Examples

### Full Security Audit
```
/security:audit
```

### OWASP Compliance Check
```
/security:audit owasp
```

### API Security Audit
```
/security:audit api
```

### Compliance Audit
```
/security:audit compliance gdpr
```

## Audit Report Format

```markdown
# Security Audit Report

**Date**: 2024-01-15
**Scope**: Full Application Audit
**Standards**: OWASP Top 10, PCI DSS
**Risk Level**: 🟡 MEDIUM

## Executive Summary

The security audit identified 2 critical, 5 high, 12 medium, and 23 low-priority issues. Critical issues require immediate attention before the next deployment.

### Risk Distribution
```
Critical ██ 2
High     █████ 5  
Medium   ████████████ 12
Low      ███████████████████████ 23
```

## Critical Vulnerabilities

### 1. SQL Injection in User Search
**Severity**: CRITICAL
**CVSS Score**: 9.8
**Location**: `src/api/search.py:45-52`

**Vulnerable Code**:
```python
def search_users(query):
    sql = f"SELECT * FROM users WHERE name LIKE '%{query}%'"
    return db.execute(sql)
```

**Remediation**:
```python
def search_users(query):
    sql = "SELECT * FROM users WHERE name LIKE %s"
    return db.execute(sql, (f'%{query}%',))
```

**Impact**: Attackers could extract entire database contents, modify data, or execute arbitrary SQL commands.

### 2. Hardcoded API Keys
**Severity**: CRITICAL
**CVSS Score**: 8.9
**Location**: `src/config/settings.py:23`

**Issue**:
```python
STRIPE_API_KEY = "sk_live_abcd1234..."  # Hardcoded secret
```

**Remediation**:
```python
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')
if not STRIPE_API_KEY:
    raise ValueError("STRIPE_API_KEY environment variable not set")
```

## High Priority Issues

### 1. Weak Password Policy
**Severity**: HIGH
**Location**: User registration

**Current Policy**:
- Minimum length: 6 characters
- No complexity requirements
- No password history

**Recommended Policy**:
```python
PASSWORD_POLICY = {
    'min_length': 12,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_numbers': True,
    'require_special': True,
    'password_history': 5,
    'max_age_days': 90,
    'min_age_minutes': 60,
    'complexity_score': 3
}
```

### 2. Missing Rate Limiting
**Severity**: HIGH
**Affected Endpoints**: Authentication, API

**Recommendation**:
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: get_remote_address(),
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
```

## Authentication & Authorization

### Findings
| Check | Status | Notes |
|-------|--------|-------|
| Password Hashing | ✅ | Using bcrypt with cost 12 |
| JWT Implementation | ⚠️ | Missing expiration validation |
| Session Management | ⚠️ | Sessions don't expire on logout |
| MFA Support | ❌ | Not implemented |
| OAuth Security | ✅ | Properly implemented |

### JWT Security Issues
```python
# Current (Vulnerable)
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except:
        return None

# Recommended
def verify_token(token):
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=['HS256'],
            options={
                "verify_exp": True,
                "verify_iat": True,
                "verify_nbf": True,
                "require": ["exp", "iat", "sub"]
            }
        )
        # Additional validation
        if payload['exp'] < time.time():
            raise TokenExpiredError()
        return payload
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {e}")
        return None
```

## OWASP Top 10 Compliance

### A01:2021 – Broken Access Control
**Status**: ⚠️ PARTIAL
- [x] Role-based access implemented
- [ ] Missing function-level authorization
- [ ] No horizontal privilege checks
- [x] CORS properly configured

### A02:2021 – Cryptographic Failures
**Status**: ✅ PASS
- [x] TLS 1.3 enforced
- [x] Strong cipher suites
- [x] Sensitive data encrypted
- [x] No weak algorithms

### A03:2021 – Injection
**Status**: ❌ FAIL
- [ ] SQL injection vulnerability found
- [x] NoSQL injection protected
- [x] Command injection protected
- [x] XSS protection enabled

### A04:2021 – Insecure Design
**Status**: ⚠️ PARTIAL
- [x] Threat modeling performed
- [ ] Missing security requirements
- [x] Secure design patterns used
- [ ] No security user stories

### A05:2021 – Security Misconfiguration
**Status**: ⚠️ PARTIAL
- [ ] Default passwords in use
- [x] Security headers configured
- [ ] Directory listing enabled
- [x] Error handling secure

### A06:2021 – Vulnerable Components
**Status**: ❌ FAIL
- [ ] 3 critical vulnerabilities in dependencies
- [ ] 7 high severity issues
- [x] Dependency scanning enabled
- [ ] Automatic updates disabled

### A07:2021 – Authentication Failures
**Status**: ⚠️ PARTIAL
- [ ] Weak password policy
- [ ] No account lockout
- [x] Secure session management
- [ ] Missing MFA

### A08:2021 – Software and Data Integrity
**Status**: ✅ PASS
- [x] Code signing implemented
- [x] Dependency verification
- [x] CI/CD security
- [x] Update mechanism secure

### A09:2021 – Security Logging
**Status**: ⚠️ PARTIAL
- [x] Authentication logged
- [ ] Missing security events
- [x] Log injection protected
- [ ] Insufficient monitoring

### A10:2021 – SSRF
**Status**: ✅ PASS
- [x] URL validation implemented
- [x] Network segmentation
- [x] Allowlist approach
- [x] Response validation

## Dependency Vulnerabilities

### Critical Dependencies
| Package | Current | Vulnerability | Severity | Fixed In |
|---------|---------|---------------|----------|----------|
| requests | 2.25.0 | CVE-2023-32681 | HIGH | 2.31.0 |
| pyjwt | 1.7.1 | CVE-2022-29217 | CRITICAL | 2.4.0 |
| pillow | 8.3.2 | CVE-2022-22815 | HIGH | 9.0.1 |

### Remediation Script
```bash
#!/bin/bash
# security-update.sh

echo "🔒 Updating vulnerable dependencies..."

# Python dependencies
pip install --upgrade \
    requests>=2.31.0 \
    pyjwt>=2.4.0 \
    pillow>=9.0.1

# Node dependencies
npm audit fix --force

# Verify updates
pip list --outdated
npm audit
```

## Security Headers Analysis

### Current Headers
```
X-Content-Type-Options: nosniff ✅
X-Frame-Options: MISSING ❌
Strict-Transport-Security: max-age=31536000 ✅
Content-Security-Policy: MISSING ❌
X-XSS-Protection: DEPRECATED ⚠️
Referrer-Policy: MISSING ❌
Permissions-Policy: MISSING ❌
```

### Recommended Headers
```python
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.trusted.com; style-src 'self' 'unsafe-inline';"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response
```

## Infrastructure Security

### Network Security
- ✅ Firewall rules properly configured
- ⚠️ Some unnecessary ports open (8080, 9000)
- ✅ VPN access required for admin
- ❌ Missing network segmentation

### Access Control
- ⚠️ Too many users with admin access
- ❌ No principle of least privilege
- ✅ MFA for infrastructure access
- ⚠️ Service accounts with excessive permissions

### Encryption
- ✅ Data encrypted at rest (AES-256)
- ✅ TLS 1.3 for data in transit
- ❌ Some backup data unencrypted
- ⚠️ Encryption keys in same location as data

## Compliance Status

### PCI DSS Requirements
| Requirement | Status | Notes |
|-------------|--------|-------|
| Build secure networks | ⚠️ | Missing network segmentation |
| Protect cardholder data | ✅ | Properly encrypted and tokenized |
| Vulnerability management | ❌ | Outdated dependencies |
| Access control | ⚠️ | Needs improvement |
| Monitor networks | ⚠️ | Insufficient logging |
| Security policies | ✅ | Documented and enforced |

### GDPR Compliance
- ✅ Privacy policy updated
- ✅ Consent mechanisms implemented
- ⚠️ Data retention policy not enforced
- ✅ Right to deletion implemented
- ❌ Missing data processing records
- ✅ Breach notification process

## Security Testing Code

### SQL Injection Test
```python
import pytest
from security_tests import test_sql_injection

@pytest.mark.security
def test_user_search_sql_injection():
    """Test for SQL injection in user search"""
    
    malicious_inputs = [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "' UNION SELECT * FROM passwords --",
        "admin'--",
        "' OR 1=1--"
    ]
    
    for payload in malicious_inputs:
        response = client.get(f'/api/users/search?q={payload}')
        
        # Should return 400 or sanitized results, never 500
        assert response.status_code in [200, 400]
        
        # Check that no SQL error is exposed
        assert 'SQL' not in response.text
        assert 'syntax error' not in response.text.lower()
```

### Authentication Security Test
```python
@pytest.mark.security
def test_authentication_security():
    """Test authentication security measures"""
    
    # Test rate limiting
    for i in range(10):
        response = client.post('/api/login', json={
            'username': 'test',
            'password': 'wrong'
        })
    
    # Should be rate limited after 5 attempts
    assert response.status_code == 429
    
    # Test timing attack resistance
    import time
    times = []
    
    for username in ['admin', 'nonexistent', 'test', 'invalid']:
        start = time.time()
        client.post('/api/login', json={
            'username': username,
            'password': 'password'
        })
        times.append(time.time() - start)
    
    # Response times should be consistent
    assert max(times) - min(times) < 0.1
```

## Remediation Plan

### Immediate (Critical)
1. **Fix SQL injection** - 2 hours
2. **Remove hardcoded secrets** - 1 hour
3. **Update critical dependencies** - 1 hour

### Short-term (This Sprint)
1. **Implement rate limiting** - 4 hours
2. **Add security headers** - 2 hours
3. **Fix JWT validation** - 3 hours
4. **Enable account lockout** - 3 hours

### Medium-term (Next Release)
1. **Implement MFA** - 2 days
2. **Network segmentation** - 3 days
3. **Enhanced logging** - 2 days
4. **Security training** - 1 day

### Long-term (Next Quarter)
1. **Zero-trust architecture** - 2 weeks
2. **Advanced threat detection** - 1 week
3. **Security automation** - 2 weeks
4. **Compliance automation** - 1 week

## Security Metrics

### Current State
- **Security Score**: 62/100
- **Critical Issues**: 2
- **Days Since Last Incident**: 45
- **MTTR**: 4.5 hours

### Target State (90 days)
- **Security Score**: 85/100
- **Critical Issues**: 0
- **Automated Scans**: Daily
- **MTTR**: < 2 hours

## Recommendations

1. **Establish Security Champions** - Designate security-focused developers in each team
2. **Security Training** - Mandatory OWASP Top 10 training for all developers
3. **Shift-Left Security** - Integrate security scanning in CI/CD pipeline
4. **Bug Bounty Program** - Consider launching for additional coverage
5. **Regular Audits** - Schedule quarterly security audits
6. **Incident Response Plan** - Update and practice regularly

## Next Steps

1. **Review this report with the team**
2. **Prioritize critical fixes**
3. **Create security tickets**
4. **Schedule security sprint**
5. **Update security policies**
```

## Options

- `--standard`: Compliance standard (owasp/pci/gdpr/sox/hipaa)
- `--scope`: Audit scope (full/api/frontend/infrastructure)
- `--output`: Output format (markdown/json/html/pdf)
- `--severity`: Minimum severity to report

## Integration

### CI/CD Pipeline
```yaml
security-audit:
  stage: security
  script:
    - claude code "/security:audit --severity=medium"
    - if [ $? -ne 0 ]; then exit 1; fi
  artifacts:
    paths:
      - security-audit-report.md
```

### Scheduled Audits
```python
# Schedule weekly security audits
@celery.task
def weekly_security_audit():
    result = run_command("/security:audit")
    
    if result.critical_issues > 0:
        notify_security_team(result)
        create_incident(result)
    
    store_audit_results(result)
    update_security_dashboard(result)
```

## Related Commands

- `/security:scan` - Quick security scan
- `/security:compliance` - Compliance checking
- `/dev:review` - Code security review
- `/project:status` - Security metrics