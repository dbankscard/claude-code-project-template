# /git:hotfix

Creates and manages hotfix branches for critical production issues.

## Usage
`/git:hotfix <issue-description> [target-version]`

## Description
Streamlines the hotfix process by creating branches, implementing fixes, and preparing for rapid deployment to production.

## Hotfix Process

### 1. Branch Creation
- Create from latest release tag
- Follow naming convention
- Set up tracking

### 2. Fix Implementation
- Minimal changes only
- Focus on the issue
- Maintain stability

### 3. Testing
- Verify fix works
- Run regression tests
- Test in staging

### 4. Release
- Merge to main
- Merge to develop
- Tag new version
- Deploy

## Examples

### Create Hotfix for Critical Bug
```
/git:hotfix "Fix payment processing error"
```

### Hotfix with Version
```
/git:hotfix "Security vulnerability patch" v2.1.1
```

### Emergency Hotfix
```
/git:hotfix "Critical data loss prevention" --emergency
```

## Hotfix Workflow

```mermaid
gitGraph
    commit id: "v2.1.0"
    branch hotfix/v2.1.1
    checkout hotfix/v2.1.1
    commit id: "Fix critical bug"
    commit id: "Add tests"
    checkout main
    merge hotfix/v2.1.1 tag: "v2.1.1"
    checkout develop
    merge hotfix/v2.1.1
```

## Hotfix Template

### Branch Naming
```
hotfix/v{version}-{brief-description}

Examples:
hotfix/v2.1.1-payment-fix
hotfix/v2.1.2-security-patch
hotfix/v2.1.3-data-corruption
```

### Commit Messages
```
hotfix: Fix critical payment processing error

This hotfix addresses a critical issue where payment processing
fails for amounts over $1000 due to decimal precision errors.

The fix:
- Uses Decimal type for all calculations
- Rounds only at final step
- Adds validation for edge cases

This issue affected approximately 5% of transactions and has
been verified in staging environment.

Fixes #critical-123
```

### Pull Request
```markdown
# 🚨 Hotfix: Payment Processing Error

## Critical Issue
Payment processing fails for orders over $1000, causing customer transactions to be declined despite valid payment methods.

## Root Cause
Floating-point precision errors in tax calculation causing total to exceed authorized amount.

## Fix Applied
```python
# Before (broken)
total = subtotal * (1 + tax_rate)  # Float arithmetic

# After (fixed)
from decimal import Decimal, ROUND_HALF_UP
total = (Decimal(str(subtotal)) * (Decimal('1') + Decimal(str(tax_rate)))).quantize(
    Decimal('0.01'), rounding=ROUND_HALF_UP
)
```

## Testing
- ✅ Unit tests added for edge cases
- ✅ Tested with production data samples
- ✅ Verified in staging environment
- ✅ Performance impact: negligible

## Rollout Plan
1. Deploy to production immediately
2. Monitor payment success rate
3. Verify no new errors introduced

## Rollback Plan
```bash
# If issues arise
kubectl rollout undo deployment/api
# or
git revert v2.1.1
```
```

## Emergency Procedures

### Critical Security Patch
```bash
#!/bin/bash
# emergency-hotfix.sh

echo "🚨 EMERGENCY HOTFIX PROCEDURE 🚨"

# 1. Create hotfix branch
git checkout -b hotfix/security-critical main

# 2. Apply security patch
patch -p1 < security-fix.patch

# 3. Commit with GPG signature
git commit -S -m "security: Critical vulnerability patch

SEVERITY: CRITICAL
CVE: CVE-2024-12345
IMPACT: Remote code execution possible

This patch must be applied immediately to all production systems."

# 4. Fast-track testing
npm run test:security
npm run test:smoke

# 5. Tag and push
git tag -s v2.1.1-security -m "Emergency security release"
git push origin hotfix/security-critical --tags

# 6. Trigger emergency deployment
kubectl set image deployment/api api=myapp:v2.1.1-security --record
```

### Data Corruption Fix
```python
# hotfix_data_corruption.py
"""
Emergency script to fix data corruption issue
"""

import logging
from database import db
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_corrupted_records():
    """Fix corrupted order records"""
    
    # Identify affected records
    corrupted = db.query("""
        SELECT id, total, calculated_total
        FROM orders
        WHERE total != calculated_total
        AND created_at > '2024-01-14'
    """)
    
    logger.info(f"Found {len(corrupted)} corrupted records")
    
    # Fix each record
    fixed = 0
    for record in corrupted:
        try:
            # Recalculate correct total
            correct_total = calculate_order_total(record.id)
            
            # Update record
            db.execute("""
                UPDATE orders 
                SET total = %s,
                    fixed_at = %s,
                    fix_reason = 'HOTFIX-2.1.1'
                WHERE id = %s
            """, (correct_total, datetime.now(), record.id))
            
            fixed += 1
            logger.info(f"Fixed order {record.id}")
            
        except Exception as e:
            logger.error(f"Failed to fix order {record.id}: {e}")
    
    logger.info(f"Fixed {fixed}/{len(corrupted)} records")
    
    # Verify fix
    remaining = db.query("""
        SELECT COUNT(*) FROM orders
        WHERE total != calculated_total
    """)
    
    if remaining[0][0] > 0:
        logger.error(f"Still {remaining[0][0]} corrupted records!")
        return False
    
    return True

if __name__ == "__main__":
    if fix_corrupted_records():
        logger.info("✅ Data corruption fixed successfully")
    else:
        logger.error("❌ Data corruption fix failed!")
```

## Hotfix Checklist

```markdown
# Hotfix Checklist

## Pre-Hotfix
- [ ] Issue confirmed in production
- [ ] Root cause identified
- [ ] Fix developed and tested locally
- [ ] Impact assessment completed
- [ ] Rollback plan prepared

## Hotfix Implementation
- [ ] Create hotfix branch from production tag
- [ ] Implement minimal fix (no extra changes!)
- [ ] Add tests for the specific issue
- [ ] Update version number (patch increment)
- [ ] Create clear commit message

## Testing
- [ ] All existing tests pass
- [ ] New tests for the fix pass
- [ ] Manual testing completed
- [ ] Tested in staging environment
- [ ] Performance impact verified

## Deployment
- [ ] PR created and reviewed (emergency review process)
- [ ] Merged to main branch
- [ ] Tagged with new version
- [ ] Deployed to production
- [ ] Merge back to develop branch

## Post-Deployment
- [ ] Production verification completed
- [ ] Monitoring alerts configured
- [ ] Customer communication sent
- [ ] Incident report created
- [ ] Team retrospective scheduled
```

## Communication Template

### Status Page Update
```markdown
**Investigating** - We are investigating reports of payment processing failures for some customers.
*Posted at 14:30 UTC*

**Identified** - We have identified an issue with decimal precision in our payment calculations affecting orders over $1000.
*Updated at 14:45 UTC*

**Fixing** - A fix has been developed and is being tested. We expect to deploy within 30 minutes.
*Updated at 15:00 UTC*

**Fixed** - The issue has been resolved. All payment processing is now functioning normally. We apologize for any inconvenience.
*Resolved at 15:30 UTC*
```

### Customer Email
```markdown
Subject: Resolved: Payment Processing Issue

Dear Customer,

We recently experienced a technical issue that may have affected your ability to complete purchases over $1000. This issue has now been resolved.

**What happened:**
A calculation error in our payment system caused some high-value transactions to be incorrectly declined.

**What we've done:**
- Identified and fixed the root cause
- Tested thoroughly to ensure no further issues
- Implemented additional monitoring

**What you need to do:**
If you experienced a failed payment in the last 2 hours, please try your purchase again. All systems are now operating normally.

We sincerely apologize for any inconvenience this may have caused.

Best regards,
The Support Team
```

## Monitoring

### Hotfix Verification
```python
# verify_hotfix.py
import requests
import time
from datetime import datetime

def verify_hotfix():
    """Verify hotfix is working in production"""
    
    test_cases = [
        {"amount": 999.99, "expected": "success"},
        {"amount": 1000.00, "expected": "success"},
        {"amount": 1000.01, "expected": "success"},
        {"amount": 9999.99, "expected": "success"},
    ]
    
    results = []
    for test in test_cases:
        response = requests.post(
            "https://api.production.com/test-payment",
            json={"amount": test["amount"]},
            headers={"X-Test-Mode": "true"}
        )
        
        success = response.json()["status"] == test["expected"]
        results.append({
            "amount": test["amount"],
            "success": success,
            "response": response.json()
        })
        
        if not success:
            alert_team(f"Hotfix verification failed for amount {test['amount']}")
    
    return all(r["success"] for r in results)
```

### Metrics Dashboard
```yaml
# hotfix-dashboard.yaml
dashboard:
  title: "Hotfix v2.1.1 Monitoring"
  
  panels:
    - title: "Payment Success Rate"
      query: |
        rate(payments_total{status="success"}[5m]) /
        rate(payments_total[5m]) * 100
      alert: < 95
      
    - title: "High Value Transactions"
      query: |
        rate(payments_total{amount=">1000"}[5m])
      alert: "sudden drop"
      
    - title: "Error Rate"
      query: |
        rate(errors_total{type="payment"}[5m])
      alert: > 0.1
      
    - title: "Response Time"
      query: |
        histogram_quantile(0.95, payment_duration_seconds)
      alert: > 500ms
```

## Options

- `--emergency`: Skip some checks for critical fixes
- `--target`: Specific version to patch
- `--no-tests`: Skip test requirements (dangerous!)
- `--auto-deploy`: Deploy immediately after merge

## Best Practices

### 1. Minimal Changes
- Fix only the reported issue
- No refactoring
- No new features
- No dependency updates

### 2. Thorough Testing
- Test the exact scenario
- Verify no regressions
- Test edge cases
- Performance check

### 3. Clear Communication
- Update status page
- Notify affected users
- Document in incident report
- Schedule retrospective

### 4. Learn and Improve
- Root cause analysis
- Update monitoring
- Add regression tests
- Improve processes

## Related Commands

- `/git:commit` - Commit hotfix changes
- `/git:release` - Create hotfix release
- `/project:deploy` - Deploy hotfix
- `/project:status` - Monitor hotfix impact