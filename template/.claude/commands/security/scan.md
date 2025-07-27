# /security:scan

Performs quick security scans on specific components or code changes.

## Usage
`/security:scan [target] [scan-type]`

## Description
Executes targeted security scans for rapid vulnerability detection, focusing on specific files, directories, or security aspects.

## Scan Types

### 1. Vulnerability Scan
- Known CVEs
- Security misconfigurations
- Weak cryptography
- Injection points

### 2. Secret Scan
- API keys
- Passwords
- Private keys
- Access tokens

### 3. Dependency Scan
- Outdated packages
- Known vulnerabilities
- License compliance
- Supply chain risks

### 4. Code Scan
- Static analysis
- Security patterns
- Input validation
- Error handling

## Examples

### Scan Current Changes
```
/security:scan
```

### Scan Specific Directory
```
/security:scan src/api/
```

### Secret Detection
```
/security:scan . secrets
```

### Dependency Check
```
/security:scan dependencies
```

## Scan Results

### Quick Scan Report
```markdown
# Security Scan Results

**Scan Type**: Vulnerability Scan
**Target**: src/api/
**Duration**: 12.3 seconds
**Status**: 🔴 ISSUES FOUND

## Summary
- 🔴 Critical: 1
- 🟡 High: 3
- 🟠 Medium: 7
- ⚪ Low: 15

## Critical Issues

### 1. Hardcoded Database Password
**File**: `src/api/config.py:34`
**Pattern**: Password in source code
```python
DATABASE_PASSWORD = "admin123"  # CRITICAL: Hardcoded password
```
**Fix**: Use environment variables
```python
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
```

## High Priority Issues

### 1. SQL Injection Risk
**File**: `src/api/queries.py:78`
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
```
**Severity**: HIGH
**CWE**: CWE-89
**Fix**: Use parameterized queries

### 2. Insecure Random
**File**: `src/api/tokens.py:23`
```python
token = random.randint(100000, 999999)  # Predictable
```
**Fix**: Use cryptographically secure random
```python
import secrets
token = secrets.randbelow(900000) + 100000
```

### 3. Missing Input Validation
**File**: `src/api/endpoints.py:45`
```python
@app.route('/api/user/<user_id>')
def get_user(user_id):
    # No validation on user_id
    return db.get_user(user_id)
```
```

### Secret Scan Results
```markdown
# Secret Detection Report

**Files Scanned**: 156
**Secrets Found**: 4
**False Positives**: 2

## Confirmed Secrets

### 1. AWS Access Key
**File**: `config/production.env:12`
**Line**: `AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE`
**Severity**: CRITICAL
**Action**: Rotate immediately and use AWS Secrets Manager

### 2. Stripe API Key
**File**: `tests/fixtures.py:45`
**Line**: `STRIPE_KEY = "sk_test_EXAMPLE_KEY_REPLACE_WITH_REAL"`
**Severity**: HIGH
**Action**: Remove from code, use test keys from environment

### 3. JWT Secret
**File**: `src/auth/constants.py:8`
**Line**: `JWT_SECRET = "your-256-bit-secret"`
**Severity**: CRITICAL
**Action**: Generate strong secret, store in environment

### 4. Database URL with Password
**File**: `.env.example:5`
**Line**: `DATABASE_URL=postgresql://user:password@localhost/db`
**Severity**: MEDIUM
**Action**: Use placeholder values in examples

## Recommendations
1. Implement pre-commit hooks for secret scanning
2. Use git-secrets or similar tools
3. Rotate all exposed credentials
4. Audit git history for secrets
```

### Dependency Scan Results
```markdown
# Dependency Vulnerability Report

**Package Manager**: pip, npm
**Total Dependencies**: 143
**Vulnerable Packages**: 7
**License Issues**: 2

## Critical Vulnerabilities

### Python Dependencies
| Package | Installed | Vulnerability | Severity | Fixed Version |
|---------|-----------|---------------|----------|--------------|
| Django | 3.2.0 | CVE-2023-23969 | HIGH | 3.2.18 |
| requests | 2.25.0 | CVE-2023-32681 | MEDIUM | 2.31.0 |
| Pillow | 8.3.2 | CVE-2022-22815 | HIGH | 9.0.1 |

### JavaScript Dependencies
| Package | Installed | Vulnerability | Severity | Fixed Version |
|---------|-----------|---------------|----------|--------------|
| lodash | 4.17.19 | CVE-2021-23337 | HIGH | 4.17.21 |
| axios | 0.21.0 | CVE-2021-3749 | MEDIUM | 0.21.2 |

## License Compliance Issues

### GPL Licensed Dependencies
1. **package-name** (GPL-3.0) - Incompatible with MIT license
2. **other-package** (AGPL-3.0) - Requires source disclosure

## Update Commands
```bash
# Python updates
pip install --upgrade Django==3.2.18 requests==2.31.0 Pillow==9.0.1

# JavaScript updates
npm update lodash@4.17.21 axios@0.21.2

# Audit after updates
pip check
npm audit
```
```

### Code Security Patterns
```markdown
# Code Security Analysis

**Files Analyzed**: 89
**Security Patterns**: 156 checks
**Issues Found**: 23

## Security Anti-Patterns Detected

### 1. Eval Usage
**File**: `src/utils/dynamic.py:34`
```python
result = eval(user_input)  # DANGEROUS
```
**Risk**: Remote code execution
**Fix**: Use ast.literal_eval() or json.loads()

### 2. Shell Command Injection
**File**: `src/tools/backup.py:67`
```python
os.system(f"tar -czf {filename} {directory}")
```
**Risk**: Command injection
**Fix**: Use subprocess with array arguments
```python
subprocess.run(['tar', '-czf', filename, directory], check=True)
```

### 3. Path Traversal
**File**: `src/files/handler.py:23`
```python
file_path = os.path.join(BASE_DIR, user_filename)
# No validation on user_filename
```
**Fix**: Validate and sanitize paths
```python
safe_filename = os.path.basename(user_filename)
if '..' in safe_filename:
    raise ValueError("Invalid filename")
```

### 4. Weak Cryptography
**File**: `src/crypto/hasher.py:12`
```python
import md5  # Deprecated and insecure
password_hash = md5.new(password).hexdigest()
```
**Fix**: Use bcrypt or argon2
```python
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```
```

## Quick Fixes

### Auto-fix Script
```python
#!/usr/bin/env python3
"""Auto-fix common security issues"""

import os
import re
import fileinput

def fix_sql_injection(file_path):
    """Fix SQL injection vulnerabilities"""
    with fileinput.input(file_path, inplace=True) as f:
        for line in f:
            # Fix string formatting in SQL
            if 'SELECT' in line and '%' in line:
                line = re.sub(
                    r'"\s*%\s*([^"]+)"',
                    r'%s", (\1,)',
                    line
                )
            print(line, end='')

def fix_hardcoded_secrets(file_path):
    """Replace hardcoded secrets with env vars"""
    patterns = [
        (r'API_KEY\s*=\s*["\']([^"\']+)["\']', 'API_KEY = os.getenv("API_KEY")'),
        (r'SECRET\s*=\s*["\']([^"\']+)["\']', 'SECRET = os.getenv("SECRET")'),
        (r'PASSWORD\s*=\s*["\']([^"\']+)["\']', 'PASSWORD = os.getenv("PASSWORD")')
    ]
    
    with fileinput.input(file_path, inplace=True) as f:
        for line in f:
            for pattern, replacement in patterns:
                line = re.sub(pattern, replacement, line)
            print(line, end='')

def add_input_validation(file_path):
    """Add basic input validation"""
    # Implementation for adding validation
    pass

# Run fixes
if __name__ == "__main__":
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                fix_sql_injection(file_path)
                fix_hardcoded_secrets(file_path)
```

## Security Scan Configuration

### .security-scan.yml
```yaml
security-scan:
  vulnerability:
    enabled: true
    severity: medium
    ignore:
      - CVE-2021-12345  # False positive
    
  secrets:
    enabled: true
    patterns:
      - '[a-zA-Z0-9]{40}'  # API keys
      - 'sk_[a-zA-Z0-9]{32}'  # Stripe keys
      - 'AKIA[0-9A-Z]{16}'  # AWS keys
    exclude:
      - '*.test.js'
      - 'tests/*'
    
  dependencies:
    enabled: true
    auto-update: false
    fail-on: critical
    
  code-analysis:
    enabled: true
    rules:
      - no-eval
      - no-exec
      - sql-injection
      - path-traversal
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running security scan..."

# Run secret detection
if git diff --cached --name-only | xargs grep -E "(api_key|password|secret)" | grep -v ".example"; then
    echo "❌ Potential secrets detected!"
    exit 1
fi

# Run security scan on staged files
staged_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|js|ts)$')
if [ -n "$staged_files" ]; then
    claude code "/security:scan $staged_files" || exit 1
fi

echo "✅ Security scan passed"
```

## Scan Performance

### Optimization Tips
```python
# Parallel scanning for large codebases
import concurrent.futures
import multiprocessing

def scan_file(file_path):
    """Scan individual file"""
    results = {
        'vulnerabilities': scan_vulnerabilities(file_path),
        'secrets': scan_secrets(file_path),
        'patterns': scan_patterns(file_path)
    }
    return file_path, results

def parallel_scan(directory):
    """Scan directory in parallel"""
    files = get_python_files(directory)
    
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=multiprocessing.cpu_count()
    ) as executor:
        results = dict(executor.map(scan_file, files))
    
    return aggregate_results(results)
```

## Integration Examples

### GitHub Actions
```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security scan
        run: |
          claude code "/security:scan --output=json" > scan-results.json
          
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: security-scan
          path: scan-results.json
          
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const results = require('./scan-results.json');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              body: `Security scan found ${results.total_issues} issues`
            });
```

### Git Pre-push Hook
```bash
#!/bin/bash
# .git/hooks/pre-push

# Run full security scan before push
echo "Running comprehensive security scan..."
claude code "/security:scan" || {
    echo "❌ Security scan failed. Push aborted."
    echo "Run '/security:scan' for details"
    exit 1
}
```

## Options

- `--type`: Scan type (vulnerability/secrets/dependencies/code)
- `--severity`: Minimum severity (critical/high/medium/low)
- `--fix`: Attempt automatic fixes
- `--output`: Output format (text/json/sarif)

## Best Practices

### 1. Regular Scanning
- Pre-commit hooks
- CI/CD integration
- Scheduled scans
- Post-deployment verification

### 2. Scan Scope
- Focus on changed files
- Prioritize critical paths
- Scan dependencies regularly
- Include configuration files

### 3. Response Plan
- Fix critical immediately
- Track security debt
- Regular review cycles
- Security training

## Related Commands

- `/security:audit` - Comprehensive audit
- `/security:compliance` - Compliance check
- `/dev:review` - Code review
- `/git:commit` - Secure commits