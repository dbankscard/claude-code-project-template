# /security:compliance

Checks compliance with security standards and regulatory requirements.

## Usage
`/security:compliance <standard> [report-type]`

## Description
Evaluates the application against specific compliance standards, generating detailed reports and remediation guidance.

## Compliance Standards

### 1. OWASP Top 10
- Web application security
- API security
- Mobile security

### 2. PCI DSS
- Payment card security
- Data protection
- Network security

### 3. GDPR
- Data privacy
- User rights
- Data processing

### 4. HIPAA
- Healthcare data
- PHI protection
- Access controls

### 5. SOC 2
- Security controls
- Availability
- Confidentiality

## Examples

### OWASP Compliance Check
```
/security:compliance owasp
```

### PCI DSS Assessment
```
/security:compliance pci-dss
```

### GDPR Readiness
```
/security:compliance gdpr
```

### Multiple Standards
```
/security:compliance "owasp,pci-dss,gdpr"
```

## Compliance Reports

### OWASP Top 10 Report
```markdown
# OWASP Top 10 Compliance Report

**Date**: 2024-01-15
**Version**: OWASP Top 10 2021
**Overall Compliance**: 78%
**Risk Level**: 🟡 MEDIUM

## Compliance Summary

| Category | Status | Score | Critical Issues |
|----------|--------|-------|-----------------|
| A01: Broken Access Control | 🟡 | 75% | 2 |
| A02: Cryptographic Failures | ✅ | 95% | 0 |
| A03: Injection | 🔴 | 40% | 3 |
| A04: Insecure Design | 🟡 | 70% | 1 |
| A05: Security Misconfiguration | 🟡 | 80% | 1 |
| A06: Vulnerable Components | 🔴 | 55% | 5 |
| A07: Authentication Failures | 🟡 | 65% | 2 |
| A08: Software Integrity | ✅ | 90% | 0 |
| A09: Security Logging | 🟡 | 70% | 1 |
| A10: SSRF | ✅ | 100% | 0 |

## Detailed Findings

### A01: Broken Access Control (75%)

#### ✅ Implemented Controls
- Role-based access control (RBAC)
- JWT token validation
- API authentication required
- CORS properly configured

#### ❌ Missing Controls
- **Horizontal authorization checks**
  ```python
  # Current (Vulnerable)
  @app.route('/api/users/<user_id>')
  @require_auth
  def get_user(user_id):
      return User.query.get(user_id)  # No check if user can access this profile
  
  # Required
  @app.route('/api/users/<user_id>')
  @require_auth
  def get_user(user_id):
      if current_user.id != user_id and not current_user.is_admin:
          abort(403)
      return User.query.get(user_id)
  ```

- **Function-level authorization**
  ```python
  # Add decorator for function-level auth
  @require_permission('users.delete')
  def delete_user(user_id):
      # Implementation
  ```

### A03: Injection (40%)

#### ❌ Critical Issues
1. **SQL Injection in search**
   ```python
   # Vulnerable
   query = f"SELECT * FROM products WHERE name LIKE '%{search}%'"
   
   # Compliant
   query = "SELECT * FROM products WHERE name LIKE %s"
   db.execute(query, (f'%{search}%',))
   ```

2. **Command Injection in file processing**
   ```python
   # Vulnerable
   os.system(f"convert {input_file} {output_file}")
   
   # Compliant
   subprocess.run(['convert', input_file, output_file], check=True)
   ```

3. **LDAP Injection in authentication**
   ```python
   # Implement proper LDAP query escaping
   from ldap3.utils.conv import escape_filter_chars
   safe_username = escape_filter_chars(username)
   ```

### A06: Vulnerable Components (55%)

#### Dependency Analysis
```
Total Dependencies: 156
Vulnerable: 24 (15.4%)
Critical: 5
High: 8
Medium: 11

Top Vulnerable Packages:
1. requests 2.25.0 → 2.31.0 (HIGH)
2. django 3.2.0 → 3.2.18 (CRITICAL)
3. pyjwt 1.7.1 → 2.4.0 (CRITICAL)
4. pillow 8.3.2 → 9.0.1 (HIGH)
5. urllib3 1.26.0 → 1.26.18 (MEDIUM)
```

## Remediation Plan

### Immediate Actions (Critical)
1. **Fix SQL Injection** (A03)
   - Update all dynamic queries
   - Use parameterized statements
   - Estimated effort: 8 hours

2. **Update Critical Dependencies** (A06)
   - Update Django to 3.2.18
   - Update PyJWT to 2.4.0
   - Estimated effort: 4 hours

3. **Implement Horizontal Authorization** (A01)
   - Add ownership checks
   - Implement permission system
   - Estimated effort: 16 hours

### Short-term (This Sprint)
1. **Security Headers** (A05)
2. **Input Validation** (A03)
3. **Dependency Updates** (A06)
4. **Enhanced Logging** (A09)

### Medium-term (Next Release)
1. **Security Design Review** (A04)
2. **MFA Implementation** (A07)
3. **Automated Security Testing** (A08)
```

### PCI DSS Compliance Report
```markdown
# PCI DSS Compliance Report

**Date**: 2024-01-15
**Version**: PCI DSS 4.0
**Merchant Level**: Level 2
**Overall Compliance**: 72%
**Audit Status**: 🟡 NEEDS IMPROVEMENT

## Requirements Summary

| Requirement | Description | Status | Score |
|-------------|-------------|--------|-------|
| 1 | Network Security | 🟡 | 70% |
| 2 | Default Passwords | ✅ | 100% |
| 3 | Cardholder Data | 🟡 | 85% |
| 4 | Encrypted Transmission | ✅ | 95% |
| 5 | Malware Protection | 🟡 | 60% |
| 6 | Secure Systems | 🟡 | 75% |
| 7 | Access Control | 🔴 | 55% |
| 8 | User Authentication | 🟡 | 70% |
| 9 | Physical Access | N/A | N/A |
| 10 | Network Monitoring | 🟡 | 65% |
| 11 | Security Testing | 🟡 | 80% |
| 12 | Security Policy | ✅ | 90% |

## Critical Findings

### Requirement 3: Protect Cardholder Data

#### Storage Requirements
- ✅ Card numbers properly masked
- ✅ CVV not stored
- ❌ Missing encryption for some archived data
- ⚠️ Retention period exceeds requirements

#### Implementation Required
```python
# Automatic data purging
@celery.task
def purge_old_card_data():
    """Remove card data older than 6 months"""
    cutoff_date = datetime.now() - timedelta(days=180)
    
    # Archive required data
    archived = archive_for_compliance(cutoff_date)
    
    # Securely delete
    CardData.query.filter(
        CardData.created_at < cutoff_date
    ).delete()
    
    # Audit log
    log_pci_activity('data_purge', {
        'records_deleted': archived['count'],
        'cutoff_date': cutoff_date
    })
```

### Requirement 7: Restrict Access

#### Current Gaps
- Too many users with admin access
- No regular access reviews
- Service accounts overprivileged
- Missing need-to-know enforcement

#### Required Controls
```python
# Implement least privilege
class PCIAccessControl:
    ROLES = {
        'cardholder_data_viewer': [
            'view_masked_pan',
            'view_transaction_history'
        ],
        'cardholder_data_admin': [
            'view_masked_pan',
            'view_full_pan',  # Requires additional auth
            'modify_card_data'
        ],
        'system_admin': [
            'manage_users',
            'view_audit_logs'
        ]
    }
    
    @require_pci_permission('view_full_pan')
    @require_mfa
    @audit_log
    def view_full_card_number(self, card_id):
        # Implementation
```

### Requirement 10: Track and Monitor

#### Logging Requirements
```python
# PCI-compliant logging
import logging
from datetime import datetime

class PCILogger:
    def __init__(self):
        self.logger = logging.getLogger('pci_audit')
        
    def log_access(self, user, resource, action, result):
        self.logger.info({
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user.id,
            'user_ip': request.remote_addr,
            'resource': resource,
            'action': action,
            'result': result,
            'session_id': session.get('id'),
            'user_agent': request.headers.get('User-Agent')
        })
    
    def log_card_access(self, user, card_id, action):
        # Special handling for card data access
        self.log_access(
            user=user,
            resource=f'card_data:{mask_card_id(card_id)}',
            action=action,
            result='success'
        )
```

## Network Segmentation

### Current Architecture
```
Internet ──► WAF ──► Load Balancer ──► Application
                                         │
                                         └──► Database
```

### Required Architecture
```
Internet ──► WAF ──► DMZ ──► App Segment ──► CDE Segment
              │        │           │              │
              │        │           │              └─► Encrypted DB
              │        │           └─► Redis (no card data)
              │        └─► Static Assets
              └─► Monitoring (read-only)

CDE (Cardholder Data Environment) Requirements:
- Isolated network segment
- Strict firewall rules
- No direct internet access
- Encrypted communication
- Enhanced monitoring
```

## Compliance Checklist

### Technical Requirements
- [ ] Network segmentation implemented
- [ ] File integrity monitoring (FIM)
- [ ] Intrusion detection system (IDS)
- [ ] Web application firewall (WAF)
- [ ] Anti-virus on all systems
- [ ] Patch management process
- [ ] Secure coding training
- [ ] Penetration testing (annual)
- [ ] Vulnerability scanning (quarterly)

### Process Requirements
- [ ] Security policy documented
- [ ] Incident response plan
- [ ] Change control process
- [ ] Access review (quarterly)
- [ ] Risk assessment (annual)
- [ ] Security awareness training
- [ ] Vendor management
- [ ] Business continuity plan
```

### GDPR Compliance Report
```markdown
# GDPR Compliance Assessment

**Date**: 2024-01-15
**Data Controller**: MyCompany Ltd
**DPO**: privacy@mycompany.com
**Overall Compliance**: 83%
**Risk Level**: 🟡 MEDIUM

## Compliance Overview

| Article | Requirement | Status | Implementation |
|---------|-------------|--------|----------------|
| Art. 5 | Data Processing Principles | ✅ | 90% |
| Art. 6 | Lawful Basis | ✅ | 95% |
| Art. 7 | Consent | 🟡 | 75% |
| Art. 12-14 | Transparency | ✅ | 88% |
| Art. 15-22 | Data Subject Rights | 🟡 | 78% |
| Art. 25 | Data Protection by Design | 🟡 | 70% |
| Art. 32 | Security Measures | ✅ | 85% |
| Art. 33-34 | Breach Notification | ✅ | 92% |
| Art. 35 | Impact Assessment | 🔴 | 40% |

## Data Processing Inventory

### Personal Data Categories
```json
{
  "basic_identity": {
    "data_types": ["name", "email", "phone"],
    "purpose": "Account management",
    "legal_basis": "Contract",
    "retention": "Account lifetime + 1 year",
    "third_parties": ["Payment processor", "Email service"]
  },
  "behavioral": {
    "data_types": ["browsing_history", "purchase_history"],
    "purpose": "Personalization, Analytics",
    "legal_basis": "Legitimate interest",
    "retention": "2 years",
    "third_parties": ["Analytics provider"]
  },
  "financial": {
    "data_types": ["payment_method", "billing_address"],
    "purpose": "Payment processing",
    "legal_basis": "Contract",
    "retention": "7 years (tax requirements)",
    "third_parties": ["Stripe", "Accounting software"]
  }
}
```

## Data Subject Rights Implementation

### Right to Access (Art. 15)
```python
class GDPRDataAccess:
    @rate_limit("1/hour")
    @require_auth
    def export_user_data(self, user_id):
        """Export all user data in machine-readable format"""
        
        # Verify identity
        if not self.verify_identity(user_id):
            raise UnauthorizedError()
        
        # Collect data from all sources
        data = {
            'profile': self.get_profile_data(user_id),
            'orders': self.get_order_history(user_id),
            'interactions': self.get_interaction_logs(user_id),
            'preferences': self.get_preferences(user_id),
            'consents': self.get_consent_history(user_id)
        }
        
        # Generate report
        return {
            'generated_at': datetime.utcnow(),
            'data': data,
            'format': 'json',
            'download_link': self.generate_secure_download(data)
        }
```

### Right to Erasure (Art. 17)
```python
class GDPRDataErasure:
    def delete_user_data(self, user_id, reason):
        """Implement right to be forgotten"""
        
        # Check if deletion is allowed
        if self.has_legal_obligation(user_id):
            raise LegalObligationError("Cannot delete due to legal requirements")
        
        # Anonymize data that must be retained
        self.anonymize_financial_records(user_id)
        self.anonymize_audit_logs(user_id)
        
        # Delete personal data
        deleted = {
            'profile': self.delete_profile(user_id),
            'content': self.delete_user_content(user_id),
            'tracking': self.delete_tracking_data(user_id),
            'backups': self.schedule_backup_deletion(user_id)
        }
        
        # Notify third parties
        self.notify_processors(user_id, 'deletion')
        
        return deleted
```

### Consent Management
```python
class ConsentManager:
    PURPOSES = {
        'necessary': {
            'name': 'Essential Services',
            'required': True,
            'description': 'Required for service operation'
        },
        'analytics': {
            'name': 'Analytics',
            'required': False,
            'description': 'Help us improve our services'
        },
        'marketing': {
            'name': 'Marketing',
            'required': False,
            'description': 'Receive promotional content'
        }
    }
    
    def record_consent(self, user_id, consents):
        """Record user consent with full audit trail"""
        
        consent_record = {
            'user_id': user_id,
            'timestamp': datetime.utcnow(),
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'consents': consents,
            'version': self.CONSENT_VERSION
        }
        
        # Store immutable record
        self.consent_log.append(consent_record)
        
        # Update current state
        self.update_user_consents(user_id, consents)
        
        # Apply consent preferences
        self.apply_consent_preferences(user_id, consents)
```

## Privacy by Design Implementation

### Data Minimization
```python
# Collect only necessary data
class MinimalUserRegistration:
    REQUIRED_FIELDS = ['email', 'password']
    OPTIONAL_FIELDS = ['name', 'phone']
    
    def register(self, data):
        # Only process allowed fields
        allowed_data = {
            k: v for k, v in data.items()
            if k in self.REQUIRED_FIELDS + self.OPTIONAL_FIELDS
        }
        
        # Explicit consent for optional data
        if any(k in self.OPTIONAL_FIELDS for k in allowed_data):
            self.require_consent('optional_data_collection')
```

### Pseudonymization
```python
import hashlib
import hmac

class DataPseudonymizer:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def pseudonymize(self, identifier):
        """Create reversible pseudonym"""
        return hmac.new(
            self.secret_key.encode(),
            identifier.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def anonymize_for_analytics(self, user_data):
        """Prepare data for analytics while preserving privacy"""
        return {
            'user_id': self.pseudonymize(user_data['email']),
            'country': user_data.get('country'),  # Keep non-identifying
            'age_range': self.get_age_range(user_data.get('birth_date')),
            # Remove identifying information
            # 'email': REMOVED
            # 'name': REMOVED
            # 'address': REMOVED
        }
```

## Breach Notification Procedures

### Automated Detection and Response
```python
class BreachDetector:
    def detect_potential_breach(self, event):
        """Detect and respond to potential breaches"""
        
        severity = self.assess_severity(event)
        
        if severity >= self.BREACH_THRESHOLD:
            # Start 72-hour timer
            breach_id = self.initiate_breach_response(event)
            
            # Immediate actions
            self.contain_breach(breach_id)
            self.preserve_evidence(breach_id)
            
            # Notifications
            if self.requires_authority_notification(event):
                self.notify_dpa(breach_id, deadline_hours=72)
            
            if self.requires_user_notification(event):
                self.notify_affected_users(breach_id)
            
            # Document everything
            self.create_breach_record(breach_id, event)
```

## Compliance Gaps

### High Priority
1. **Data Protection Impact Assessment (DPIA)**
   - Required for high-risk processing
   - Currently only 40% complete
   - Need formal process

2. **Consent Management**
   - Granular consent options needed
   - Consent withdrawal process incomplete
   - Third-party consent tracking missing

3. **Data Portability**
   - API for data export exists
   - Need standard format (JSON/CSV)
   - Automated transfer to other controllers

### Remediation Timeline
- **Week 1-2**: Complete DPIA process
- **Week 3-4**: Implement granular consent
- **Week 5-6**: Data portability improvements
- **Week 7-8**: Third-party processor audit
```

## Compliance Automation

### Continuous Compliance Monitoring
```python
class ComplianceMonitor:
    def __init__(self):
        self.checks = {
            'owasp': OWASPChecker(),
            'pci': PCIDSSChecker(),
            'gdpr': GDPRChecker(),
            'hipaa': HIPAAChecker(),
            'soc2': SOC2Checker()
        }
    
    @scheduled(cron="0 0 * * *")  # Daily
    def run_compliance_checks(self):
        """Run automated compliance checks"""
        
        results = {}
        for standard, checker in self.checks.items():
            try:
                result = checker.run()
                results[standard] = result
                
                # Alert on degradation
                if result.score < result.previous_score:
                    self.alert_compliance_team(standard, result)
                
                # Auto-remediate where possible
                if result.auto_fixable:
                    self.apply_auto_fixes(standard, result.fixes)
                    
            except Exception as e:
                self.log_error(f"Compliance check failed: {standard}", e)
        
        # Generate report
        self.generate_compliance_dashboard(results)
        
        return results
```

### Compliance as Code
```yaml
# compliance-rules.yaml
rules:
  - id: OWASP-A01-001
    name: Enforce authentication on all endpoints
    severity: critical
    check: |
      all_endpoints.must_have(authentication)
      except: ['/health', '/metrics', '/public/*']
    
  - id: PCI-3.4
    name: Mask PAN when displayed
    severity: critical
    check: |
      when: displaying_card_number
      then: must_mask_except_last_four
    
  - id: GDPR-25
    name: Privacy by design
    severity: high
    check: |
      new_features.must_have(privacy_impact_assessment)
      personal_data.must_have(purpose_limitation)
      data_collection.must_be(minimal)
```

## Options

- `--standard`: Compliance standard(s) to check
- `--detail`: Level of detail (summary/normal/detailed)
- `--format`: Output format (markdown/json/pdf)
- `--evidence`: Include evidence/artifacts

## Integration

### CI/CD Pipeline
```yaml
compliance-check:
  stage: compliance
  script:
    - claude code "/security:compliance owasp,pci --format=json" > compliance.json
    - python check_compliance_thresholds.py compliance.json
  artifacts:
    reports:
      compliance: compliance.json
```

### Compliance Dashboard
```python
@app.route('/compliance/dashboard')
@require_admin
def compliance_dashboard():
    """Real-time compliance status"""
    
    standards = ['owasp', 'pci', 'gdpr', 'soc2']
    results = {}
    
    for standard in standards:
        result = run_compliance_check(standard)
        results[standard] = {
            'score': result.score,
            'status': get_status_emoji(result.score),
            'issues': result.critical_issues,
            'last_check': result.timestamp
        }
    
    return render_template('compliance_dashboard.html', results=results)
```

## Related Commands

- `/security:audit` - Full security audit
- `/security:scan` - Quick security scan
- `/project:docs` - Compliance documentation
- `/project:status` - Compliance metrics