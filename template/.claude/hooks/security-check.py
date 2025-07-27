#!/usr/bin/env python3
"""
Security check hook - validates security concerns before operations
"""
import re
import sys
from pathlib import Path

# Patterns that indicate security-sensitive content
SENSITIVE_PATTERNS = [
    # Credentials and secrets
    r'(api[_-]?key|apikey|api[_-]?secret)',
    r'(secret[_-]?key|secret|private[_-]?key)',
    r'(password|passwd|pwd)',
    r'(token|auth[_-]?token|access[_-]?token)',
    r'(aws[_-]?access[_-]?key|aws[_-]?secret)',
    
    # Connection strings
    r'(mongodb://|postgres://|mysql://|redis://)',
    r'(connection[_-]?string|conn[_-]?str)',
    
    # Private keys
    r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
    r'-----BEGIN PGP PRIVATE KEY BLOCK-----',
    
    # Common secret file patterns
    r'\.env\.',
    r'\.pem$',
    r'\.key$',
    r'id_rsa',
    r'id_dsa',
    r'id_ecdsa',
    r'id_ed25519',
]

def check_file_content(file_path):
    """Check file content for security issues."""
    issues = []
    
    try:
        content = Path(file_path).read_text()
        
        # Check for sensitive patterns
        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"Potential sensitive data pattern found: {pattern}")
        
        # Check for hardcoded IPs (except localhost)
        ip_pattern = r'\b(?!127\.0\.0\.1|localhost|0\.0\.0\.0)(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        if re.search(ip_pattern, content):
            issues.append("Hardcoded IP address detected")
        
        # Check for base64 encoded secrets
        base64_pattern = r'[A-Za-z0-9+/]{40,}={0,2}'
        if re.search(base64_pattern, content):
            # Only flag if it looks like a key/secret context
            context_pattern = r'(key|secret|token|password).{0,20}["\']?\s*[:=]\s*["\']?' + base64_pattern
            if re.search(context_pattern, content, re.IGNORECASE):
                issues.append("Potential base64 encoded secret detected")
    
    except Exception as e:
        # If we can't read the file, skip security check
        pass
    
    return issues

def check_command_security(command):
    """Check if a command has security implications."""
    dangerous_commands = [
        (r'curl .* \| .*sh', "Downloading and executing remote scripts"),
        (r'wget .* \| .*sh', "Downloading and executing remote scripts"),
        (r'eval\s*\(', "Using eval() with user input"),
        (r'exec\s*\(', "Using exec() with user input"),
        (r'chmod\s+777', "Setting overly permissive file permissions"),
        (r'sudo\s+rm\s+-rf\s+/', "Dangerous system deletion command"),
        (r':(){ :|:& };:', "Fork bomb detected"),
    ]
    
    issues = []
    for pattern, description in dangerous_commands:
        if re.search(pattern, command, re.IGNORECASE):
            issues.append(f"Dangerous command pattern: {description}")
    
    return issues

def main():
    """Main hook entry point."""
    # This hook can be called with different contexts
    if len(sys.argv) > 1:
        context = sys.argv[1]
        
        if context == "file" and len(sys.argv) > 2:
            # File operation
            file_path = sys.argv[2]
            issues = check_file_content(file_path)
            
            if issues:
                print("\n⚠️  Security Check Results:")
                print("-" * 50)
                for issue in issues:
                    print(f"🔸 {issue}")
                print("-" * 50)
                print("📌 Recommendation: Review and address these security concerns")
                
        elif context == "command" and len(sys.argv) > 2:
            # Command execution
            command = sys.argv[2]
            issues = check_command_security(command)
            
            if issues:
                print("\n🚨 Security Warning:")
                print("-" * 50)
                for issue in issues:
                    print(f"❌ {issue}")
                print("-" * 50)
                print("🛑 This command has been blocked for security reasons")
                sys.exit(1)

if __name__ == '__main__':
    main()