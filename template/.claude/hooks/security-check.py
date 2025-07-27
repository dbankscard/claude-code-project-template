#!/usr/bin/env python3
"""
Security check hook - Performs security scans on code changes
"""

import os
import sys
import re
import json
import subprocess
import hashlib
from typing import Dict, List, Tuple, Optional
from pathlib import Path

class SecurityChecker:
    def __init__(self):
        self.config = self.load_config()
        self.vulnerabilities = []
        self.security_score = 100
    
    def load_config(self) -> Dict:
        """Load security configuration"""
        config_path = '.claude/hooks/security.json'
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
        return {
            'enabled_checks': {
                'secrets': True,
                'vulnerabilities': True,
                'permissions': True,
                'dependencies': True,
                'code_patterns': True
            },
            'severity_threshold': 'medium',
            'block_on_critical': True,
            'secret_patterns': [
                {
                    'name': 'AWS Access Key',
                    'pattern': r'AKIA[0-9A-Z]{16}',
                    'severity': 'critical'
                },
                {
                    'name': 'Generic API Key',
                    'pattern': r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']([a-zA-Z0-9]{32,})["\']',
                    'severity': 'high'
                },
                {
                    'name': 'Private Key',
                    'pattern': r'-----BEGIN (RSA |EC )?PRIVATE KEY-----',
                    'severity': 'critical'
                }
            ],
            'dangerous_functions': [
                'eval', 'exec', 'compile', '__import__',
                'subprocess.call', 'os.system', 'pickle.loads'
            ]
        }
    
    def check_file_permissions(self, filepath: str) -> List[Dict]:
        """Check file permissions for security issues"""
        issues = []
        
        try:
            stat_info = os.stat(filepath)
            mode = stat_info.st_mode
            
            # Check for world-writable files
            if mode & 0o002:
                issues.append({
                    'type': 'permissions',
                    'severity': 'high',
                    'file': filepath,
                    'issue': 'World-writable file',
                    'fix': f'chmod o-w {filepath}'
                })
            
            # Check for executable files that shouldn't be
            if mode & 0o111 and not filepath.endswith(('.sh', '.py', '.exe')):
                if not filepath.startswith(('bin/', 'scripts/')):
                    issues.append({
                        'type': 'permissions',
                        'severity': 'medium',
                        'file': filepath,
                        'issue': 'Unexpected executable permission',
                        'fix': f'chmod -x {filepath}'
                    })
        except:
            pass
        
        return issues
    
    def scan_for_secrets(self, filepath: str) -> List[Dict]:
        """Scan file for exposed secrets"""
        issues = []
        
        # Skip binary files
        if self.is_binary_file(filepath):
            return issues
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                # Check each configured pattern
                for secret_config in self.config['secret_patterns']:
                    pattern = re.compile(secret_config['pattern'])
                    
                    for i, line in enumerate(lines, 1):
                        matches = pattern.finditer(line)
                        for match in matches:
                            # Check if it's a false positive
                            if self.is_false_positive(filepath, line, match):
                                continue
                            
                            issues.append({
                                'type': 'secret',
                                'severity': secret_config['severity'],
                                'file': filepath,
                                'line': i,
                                'secret_type': secret_config['name'],
                                'matched': self.redact_secret(match.group(0)),
                                'fix': 'Move to environment variable or secret management system'
                            })
                
                # Additional patterns
                self.check_hardcoded_passwords(filepath, lines, issues)
                self.check_connection_strings(filepath, lines, issues)
                
        except Exception as e:
            print(f"Error scanning {filepath}: {e}")
        
        return issues
    
    def is_binary_file(self, filepath: str) -> bool:
        """Check if file is binary"""
        try:
            with open(filepath, 'rb') as f:
                chunk = f.read(8192)
                return b'\0' in chunk
        except:
            return True
    
    def is_false_positive(self, filepath: str, line: str, match) -> bool:
        """Check if a match is a false positive"""
        # Skip test files
        if 'test' in filepath.lower() or 'example' in filepath.lower():
            return True
        
        # Skip comments
        if line.strip().startswith(('#', '//', '/*', '*')):
            return True
        
        # Skip documentation
        if filepath.endswith(('.md', '.rst', '.txt')):
            return True
        
        # Skip if it's a placeholder
        secret = match.group(0)
        placeholders = ['xxx', 'your-', 'example', 'test', 'dummy', 'fake']
        if any(p in secret.lower() for p in placeholders):
            return True
        
        return False
    
    def redact_secret(self, secret: str) -> str:
        """Redact a secret for safe display"""
        if len(secret) <= 8:
            return '*' * len(secret)
        
        return secret[:3] + '*' * (len(secret) - 6) + secret[-3:]
    
    def check_hardcoded_passwords(self, filepath: str, lines: List[str], issues: List[Dict]):
        """Check for hardcoded passwords"""
        password_patterns = [
            r'(?i)password\s*[:=]\s*["\']([^"\']+)["\']',
            r'(?i)passwd\s*[:=]\s*["\']([^"\']+)["\']',
            r'(?i)pwd\s*[:=]\s*["\']([^"\']+)["\']'
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern in password_patterns:
                match = re.search(pattern, line)
                if match and not self.is_false_positive(filepath, line, match):
                    password = match.group(1)
                    
                    # Skip if it's reading from env
                    if 'environ' in line or 'getenv' in line:
                        continue
                    
                    issues.append({
                        'type': 'secret',
                        'severity': 'high',
                        'file': filepath,
                        'line': i,
                        'secret_type': 'Hardcoded Password',
                        'matched': self.redact_secret(password),
                        'fix': 'Use environment variables or secret management'
                    })
    
    def check_connection_strings(self, filepath: str, lines: List[str], issues: List[Dict]):
        """Check for database connection strings with passwords"""
        conn_patterns = [
            r'(?i)(mongodb|mysql|postgresql|postgres|redis)://[^:]+:([^@]+)@',
            r'(?i)data source=.*;password=([^;]+)',
            r'(?i)server=.*;pwd=([^;]+)'
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern in conn_patterns:
                match = re.search(pattern, line)
                if match and not self.is_false_positive(filepath, line, match):
                    issues.append({
                        'type': 'secret',
                        'severity': 'critical',
                        'file': filepath,
                        'line': i,
                        'secret_type': 'Connection String with Password',
                        'matched': self.redact_secret(match.group(0)),
                        'fix': 'Use connection string without password, authenticate separately'
                    })
    
    def scan_for_vulnerabilities(self, filepath: str) -> List[Dict]:
        """Scan for code vulnerabilities"""
        issues = []
        
        if not filepath.endswith(('.py', '.js', '.ts', '.java', '.go', '.rb')):
            return issues
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                # Language-specific checks
                if filepath.endswith('.py'):
                    issues.extend(self.check_python_vulnerabilities(filepath, lines))
                elif filepath.endswith(('.js', '.ts')):
                    issues.extend(self.check_javascript_vulnerabilities(filepath, lines))
                elif filepath.endswith('.java'):
                    issues.extend(self.check_java_vulnerabilities(filepath, lines))
                
                # Common vulnerability patterns
                issues.extend(self.check_injection_vulnerabilities(filepath, lines))
                issues.extend(self.check_path_traversal(filepath, lines))
                issues.extend(self.check_xxe_vulnerabilities(filepath, lines))
                
        except Exception as e:
            print(f"Error scanning {filepath}: {e}")
        
        return issues
    
    def check_python_vulnerabilities(self, filepath: str, lines: List[str]) -> List[Dict]:
        """Check Python-specific vulnerabilities"""
        issues = []
        
        # Check for dangerous functions
        for i, line in enumerate(lines, 1):
            for func in self.config['dangerous_functions']:
                if func in line and not line.strip().startswith('#'):
                    issues.append({
                        'type': 'vulnerability',
                        'severity': 'high',
                        'file': filepath,
                        'line': i,
                        'vulnerability': f'Use of dangerous function: {func}',
                        'cwe': 'CWE-95',
                        'fix': f'Replace {func} with safer alternative'
                    })
            
            # SQL injection
            sql_patterns = [
                r'(?i)(select|insert|update|delete).*%s*"%\s*%',
                r'(?i)(select|insert|update|delete).*\+.*\+',
                r'\.format\(.*\).*(?i)(select|insert|update|delete)'
            ]
            
            for pattern in sql_patterns:
                if re.search(pattern, line):
                    issues.append({
                        'type': 'vulnerability',
                        'severity': 'critical',
                        'file': filepath,
                        'line': i,
                        'vulnerability': 'Potential SQL injection',
                        'cwe': 'CWE-89',
                        'fix': 'Use parameterized queries'
                    })
            
            # Command injection
            if 'os.system' in line or 'subprocess.call' in line:
                if '+' in line or '%' in line or '.format' in line:
                    issues.append({
                        'type': 'vulnerability',
                        'severity': 'critical',
                        'file': filepath,
                        'line': i,
                        'vulnerability': 'Potential command injection',
                        'cwe': 'CWE-78',
                        'fix': 'Use subprocess with list arguments'
                    })
        
        return issues
    
    def check_javascript_vulnerabilities(self, filepath: str, lines: List[str]) -> List[Dict]:
        """Check JavaScript-specific vulnerabilities"""
        issues = []
        
        for i, line in enumerate(lines, 1):
            # eval() usage
            if 'eval(' in line and not line.strip().startswith('//'):
                issues.append({
                    'type': 'vulnerability',
                    'severity': 'high',
                    'file': filepath,
                    'line': i,
                    'vulnerability': 'Use of eval()',
                    'cwe': 'CWE-95',
                    'fix': 'Use JSON.parse() or safer alternatives'
                })
            
            # innerHTML without sanitization
            if '.innerHTML' in line and '=' in line:
                issues.append({
                    'type': 'vulnerability',
                    'severity': 'high',
                    'file': filepath,
                    'line': i,
                    'vulnerability': 'Potential XSS via innerHTML',
                    'cwe': 'CWE-79',
                    'fix': 'Use textContent or sanitize HTML'
                })
            
            # SQL in JavaScript (Node.js)
            if 'query(' in line and ('+' in line or '`' in line):
                issues.append({
                    'type': 'vulnerability',
                    'severity': 'critical',
                    'file': filepath,
                    'line': i,
                    'vulnerability': 'Potential SQL injection',
                    'cwe': 'CWE-89',
                    'fix': 'Use parameterized queries'
                })
        
        return issues
    
    def check_java_vulnerabilities(self, filepath: str, lines: List[str]) -> List[Dict]:
        """Check Java-specific vulnerabilities"""
        issues = []
        
        for i, line in enumerate(lines, 1):
            # SQL injection in Java
            if 'createStatement()' in line or ('Statement' in line and 'execute' in line):
                issues.append({
                    'type': 'vulnerability',
                    'severity': 'high',
                    'file': filepath,
                    'line': i,
                    'vulnerability': 'Use of Statement instead of PreparedStatement',
                    'cwe': 'CWE-89',
                    'fix': 'Use PreparedStatement for SQL queries'
                })
            
            # Weak random number generation
            if 'java.util.Random' in line:
                issues.append({
                    'type': 'vulnerability',
                    'severity': 'medium',
                    'file': filepath,
                    'line': i,
                    'vulnerability': 'Weak random number generator',
                    'cwe': 'CWE-338',
                    'fix': 'Use java.security.SecureRandom for security-sensitive operations'
                })
        
        return issues
    
    def check_injection_vulnerabilities(self, filepath: str, lines: List[str]) -> List[Dict]:
        """Check for various injection vulnerabilities"""
        issues = []
        
        # LDAP injection patterns
        ldap_patterns = [
            r'ldap.*\(.*\+.*\)',
            r'ldap.*%s',
            r'ldap.*\.format\('
        ]
        
        # XPath injection patterns
        xpath_patterns = [
            r'xpath.*\+',
            r'selectNodes.*\+',
            r'evaluate.*\+'
        ]
        
        for i, line in enumerate(lines, 1):
            # Check LDAP injection
            for pattern in ldap_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'type': 'vulnerability',
                        'severity': 'high',
                        'file': filepath,
                        'line': i,
                        'vulnerability': 'Potential LDAP injection',
                        'cwe': 'CWE-90',
                        'fix': 'Use LDAP query escaping'
                    })
            
            # Check XPath injection
            for pattern in xpath_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        'type': 'vulnerability',
                        'severity': 'high',
                        'file': filepath,
                        'line': i,
                        'vulnerability': 'Potential XPath injection',
                        'cwe': 'CWE-643',
                        'fix': 'Use parameterized XPath queries'
                    })
        
        return issues
    
    def check_path_traversal(self, filepath: str, lines: List[str]) -> List[Dict]:
        """Check for path traversal vulnerabilities"""
        issues = []
        
        path_operations = [
            'open(', 'file(', 'fopen(', 'readFile(', 'writeFile(',
            'File(', 'FileReader(', 'FileWriter(', 'Path('
        ]
        
        for i, line in enumerate(lines, 1):
            for op in path_operations:
                if op in line:
                    # Check if user input is used
                    if any(x in line for x in ['request.', 'req.', 'params', 'query', 'body', 'args']):
                        # Check if path is validated
                        if not any(x in line for x in ['sanitize', 'validate', 'normalize', 'basename']):
                            issues.append({
                                'type': 'vulnerability',
                                'severity': 'high',
                                'file': filepath,
                                'line': i,
                                'vulnerability': 'Potential path traversal',
                                'cwe': 'CWE-22',
                                'fix': 'Validate and sanitize file paths'
                            })
        
        return issues
    
    def check_xxe_vulnerabilities(self, filepath: str, lines: List[str]) -> List[Dict]:
        """Check for XML External Entity (XXE) vulnerabilities"""
        issues = []
        
        # XML parsing patterns
        xml_patterns = [
            r'XMLReader|XmlReader',
            r'DocumentBuilder',
            r'SAXParser',
            r'XMLStreamReader',
            r'etree\.parse',
            r'minidom\.parse'
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern in xml_patterns:
                if re.search(pattern, line):
                    # Check if XXE protection is enabled
                    xxe_protection = [
                        'setFeature.*FEATURE_SECURE_PROCESSING',
                        'setFeature.*disallow-doctype-decl',
                        'setExpandEntityReferences.*false',
                        'XMLConstants.FEATURE_SECURE_PROCESSING'
                    ]
                    
                    # Look ahead for protection
                    protected = False
                    for j in range(max(0, i-5), min(len(lines), i+5)):
                        if any(re.search(p, lines[j]) for p in xxe_protection):
                            protected = True
                            break
                    
                    if not protected:
                        issues.append({
                            'type': 'vulnerability',
                            'severity': 'high',
                            'file': filepath,
                            'line': i,
                            'vulnerability': 'Potential XXE vulnerability',
                            'cwe': 'CWE-611',
                            'fix': 'Disable external entity processing'
                        })
        
        return issues
    
    def check_dependencies(self, filepath: str) -> List[Dict]:
        """Check for vulnerable dependencies"""
        issues = []
        
        if filepath.endswith('requirements.txt'):
            issues.extend(self.check_python_dependencies(filepath))
        elif filepath.endswith('package.json'):
            issues.extend(self.check_npm_dependencies(filepath))
        elif filepath.endswith('pom.xml'):
            issues.extend(self.check_maven_dependencies(filepath))
        elif filepath.endswith('go.mod'):
            issues.extend(self.check_go_dependencies(filepath))
        
        return issues
    
    def check_python_dependencies(self, filepath: str) -> List[Dict]:
        """Check Python dependencies for vulnerabilities"""
        issues = []
        
        # Known vulnerable packages (simplified - real implementation would use a database)
        vulnerable_packages = {
            'django<3.2.18': {'severity': 'high', 'cve': 'CVE-2023-23969'},
            'requests<2.31.0': {'severity': 'medium', 'cve': 'CVE-2023-32681'},
            'pillow<9.0.1': {'severity': 'high', 'cve': 'CVE-2022-22815'},
            'pyyaml<5.4': {'severity': 'critical', 'cve': 'CVE-2020-14343'}
        }
        
        try:
            with open(filepath, 'r') as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse package and version
                    parts = re.split(r'[<>=]+', line)
                    if len(parts) >= 2:
                        package = parts[0].lower()
                        version = parts[1]
                        
                        # Check against known vulnerabilities
                        for vuln_spec, vuln_info in vulnerable_packages.items():
                            vuln_package = vuln_spec.split('<')[0]
                            if package == vuln_package:
                                issues.append({
                                    'type': 'dependency',
                                    'severity': vuln_info['severity'],
                                    'file': filepath,
                                    'line': i,
                                    'package': package,
                                    'version': version,
                                    'vulnerability': vuln_info['cve'],
                                    'fix': f'Update {package} to latest version'
                                })
        except Exception as e:
            print(f"Error checking dependencies: {e}")
        
        return issues
    
    def check_npm_dependencies(self, filepath: str) -> List[Dict]:
        """Check npm dependencies for vulnerabilities"""
        issues = []
        
        # Run npm audit if available
        try:
            result = subprocess.run(
                ['npm', 'audit', '--json'],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(filepath)
            )
            
            if result.returncode != 0 and result.stdout:
                audit_data = json.loads(result.stdout)
                
                for advisory_id, advisory in audit_data.get('advisories', {}).items():
                    issues.append({
                        'type': 'dependency',
                        'severity': advisory['severity'],
                        'file': filepath,
                        'package': advisory['module_name'],
                        'vulnerability': advisory['title'],
                        'cve': advisory.get('cves', ['N/A'])[0],
                        'fix': advisory.get('recommendation', 'Update package')
                    })
        except:
            # Fallback to basic checking
            pass
        
        return issues
    
    def generate_report(self, files_scanned: List[str]) -> Dict:
        """Generate security scan report"""
        # Group vulnerabilities by severity
        by_severity = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        for vuln in self.vulnerabilities:
            severity = vuln.get('severity', 'medium')
            by_severity[severity].append(vuln)
        
        # Calculate security score
        deductions = {
            'critical': 25,
            'high': 15,
            'medium': 5,
            'low': 2
        }
        
        for severity, vulns in by_severity.items():
            self.security_score -= len(vulns) * deductions[severity]
        
        self.security_score = max(0, self.security_score)
        
        return {
            'files_scanned': len(files_scanned),
            'vulnerabilities_found': len(self.vulnerabilities),
            'security_score': self.security_score,
            'by_severity': {
                k: len(v) for k, v in by_severity.items()
            },
            'critical_vulnerabilities': by_severity['critical'],
            'high_vulnerabilities': by_severity['high'][:5],  # Top 5
            'summary': self.generate_summary(by_severity)
        }
    
    def generate_summary(self, by_severity: Dict) -> str:
        """Generate human-readable summary"""
        if self.security_score >= 90:
            status = "✅ Excellent"
        elif self.security_score >= 70:
            status = "🟡 Good (needs attention)"
        elif self.security_score >= 50:
            status = "🟠 Poor (action required)"
        else:
            status = "🔴 Critical (immediate action needed)"
        
        summary = [
            f"Security Score: {self.security_score}/100 - {status}",
            f"Critical: {len(by_severity['critical'])}",
            f"High: {len(by_severity['high'])}",
            f"Medium: {len(by_severity['medium'])}",
            f"Low: {len(by_severity['low'])}"
        ]
        
        return " | ".join(summary)
    
    def scan_files(self, files: List[str]) -> Dict:
        """Scan multiple files for security issues"""
        for filepath in files:
            if not os.path.exists(filepath):
                continue
            
            # Skip certain file types
            skip_extensions = ['.md', '.txt', '.log', '.gitignore', '.dockerignore']
            if any(filepath.endswith(ext) for ext in skip_extensions):
                continue
            
            # Run various security checks
            if self.config['enabled_checks']['permissions']:
                self.vulnerabilities.extend(self.check_file_permissions(filepath))
            
            if self.config['enabled_checks']['secrets']:
                self.vulnerabilities.extend(self.scan_for_secrets(filepath))
            
            if self.config['enabled_checks']['vulnerabilities']:
                self.vulnerabilities.extend(self.scan_for_vulnerabilities(filepath))
            
            if self.config['enabled_checks']['dependencies']:
                self.vulnerabilities.extend(self.check_dependencies(filepath))
        
        return self.generate_report(files)

def main():
    """Main entry point"""
    # Get files to scan from arguments or git
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        # Get changed files from git
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                capture_output=True,
                text=True,
                check=True
            )
            files = result.stdout.strip().split('\n') if result.stdout else []
        except:
            files = []
    
    if not files:
        print("No files to scan")
        sys.exit(0)
    
    # Run security scan
    checker = SecurityChecker()
    report = checker.scan_files(files)
    
    # Output report
    print("\n🔒 Security Scan Report")
    print("=" * 50)
    print(f"Files scanned: {report['files_scanned']}")
    print(f"Issues found: {report['vulnerabilities_found']}")
    print(f"\n{report['summary']}\n")
    
    # Show critical issues
    if report['critical_vulnerabilities']:
        print("🚨 CRITICAL ISSUES:")
        for vuln in report['critical_vulnerabilities'][:3]:
            print(f"  - {vuln['file']}:{vuln.get('line', '?')}")
            print(f"    {vuln.get('vulnerability', vuln.get('issue', 'Unknown issue'))}")
            print(f"    Fix: {vuln['fix']}\n")
    
    # Block on critical issues if configured
    if checker.config['block_on_critical'] and report['critical_vulnerabilities']:
        print("❌ Blocking due to critical security issues")
        print("   Fix these issues before proceeding")
        sys.exit(1)
    
    # Save detailed report
    report_file = '.claude/security-report.json'
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    
    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': datetime.utcnow().isoformat(),
            'report': report,
            'vulnerabilities': checker.vulnerabilities
        }, f, indent=2)
    
    print(f"📄 Detailed report saved to {report_file}")
    
    # Exit with appropriate code
    if report['security_score'] < 50:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == '__main__':
    main()