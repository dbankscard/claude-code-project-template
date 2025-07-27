---
name: audit
namespace: security
description: Comprehensive security audit of codebase
---

# Security Audit Command

Performs thorough security analysis using the security-auditor agent.

## Usage
```
/security:audit [--scope full|changes|module] [--level basic|standard|paranoid]
```

## Audit Process
1. **Dependency Scanning**: Check for vulnerable packages
2. **Code Analysis**: Static security analysis
3. **Secret Detection**: Scan for exposed credentials
4. **Configuration Review**: Validate security settings
5. **OWASP Compliance**: Check against OWASP Top 10

## Options
- `--scope`: Audit scope (default: changes)
  - `full`: Entire codebase
  - `changes`: Recent changes only
  - `module`: Specific module/directory
- `--level`: Security paranoia level (default: standard)

## Example
```
/security:audit --scope full --level paranoid
```

## Report Includes
- Vulnerability summary
- Risk assessment
- Remediation steps
- Security best practices
- Compliance status