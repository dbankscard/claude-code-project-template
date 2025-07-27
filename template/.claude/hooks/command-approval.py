#!/usr/bin/env python3
"""
Command approval hook - Determines which commands need user approval
"""

import sys
import re
import json
import os
from typing import Dict, List, Tuple, Optional

# Commands that are always safe (no approval needed)
SAFE_COMMANDS = {
    # Read-only operations
    'ls', 'dir', 'pwd', 'cat', 'head', 'tail', 'less', 'more',
    'grep', 'find', 'which', 'echo', 'printf', 'date', 'whoami',
    'hostname', 'uname', 'env', 'printenv', 'type', 'file',
    
    # Git read operations
    'git status', 'git diff', 'git log', 'git branch', 'git remote',
    'git show', 'git config --get', 'git describe', 'git tag -l',
    
    # Development tools (read-only)
    'python --version', 'node --version', 'npm --version',
    'pip list', 'pip show', 'npm list', 'yarn list',
    
    # Testing and linting
    'pytest', 'python -m pytest', 'npm test', 'yarn test',
    'flake8', 'pylint', 'mypy', 'black --check', 'isort --check',
    'eslint', 'prettier --check',
}

# Command patterns that are safe
SAFE_PATTERNS = [
    r'^cd\s+[\w\-\./]+$',  # Change directory
    r'^export\s+\w+=[\w\-\./]+$',  # Set environment variable
    r'^source\s+[\w\-\./]+$',  # Source a file
    r'^\.\s+[\w\-\./]+$',  # Source a file (alternative)
    r'^man\s+\w+$',  # Manual pages
    r'^help\s+\w+$',  # Help command
    r'^\w+\s+--help$',  # Help flag
    r'^\w+\s+-h$',  # Help flag (short)
    r'^pip\s+freeze',  # List pip packages
    r'^docker\s+ps',  # List docker containers
    r'^docker\s+images',  # List docker images
]

# Commands that always need approval
DANGEROUS_COMMANDS = {
    'rm', 'rmdir', 'del', 'unlink',
    'mv', 'move', 'rename',
    'cp', 'copy', 'xcopy',
    'chmod', 'chown', 'chgrp',
    'kill', 'killall', 'pkill',
    'shutdown', 'reboot', 'halt',
    'dd', 'format', 'mkfs',
    'curl', 'wget', 'nc', 'netcat',
    'eval', 'exec', 'source',
    'sudo', 'su', 'doas',
}

# Dangerous patterns
DANGEROUS_PATTERNS = [
    r'>\s*/dev/',  # Writing to device files
    r'curl.*\|.*sh',  # Curl pipe to shell
    r'wget.*\|.*sh',  # Wget pipe to shell
    r'npm\s+install.*-g',  # Global npm install
    r'pip\s+install.*--user',  # User pip install
    r':\(\)\s*\{.*\}',  # Fork bomb pattern
    r'.*\$\(.*\)',  # Command substitution
    r'.*`.*`',  # Backtick substitution
]

class CommandApproval:
    def __init__(self):
        self.config = self.load_config()
        self.context = self.get_context()
    
    def load_config(self) -> Dict:
        """Load approval configuration"""
        config_paths = [
            '.claude/hooks/approval.json',
            '.claude/approval.json',
            'approval.json'
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return json.load(f)
        
        # Default config
        return {
            'auto_approve_percentage': 90,
            'require_approval_in_production': True,
            'additional_safe_commands': [],
            'additional_dangerous_commands': [],
            'custom_rules': []
        }
    
    def get_context(self) -> Dict:
        """Get execution context"""
        return {
            'environment': os.environ.get('ENVIRONMENT', 'development'),
            'user': os.environ.get('USER', 'unknown'),
            'cwd': os.getcwd(),
            'is_ci': os.environ.get('CI', 'false').lower() == 'true',
            'is_production': os.environ.get('ENVIRONMENT') == 'production'
        }
    
    def is_safe_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """Check if command is safe to execute without approval"""
        
        # Clean the command
        command = command.strip()
        
        # Check exact matches
        if command in SAFE_COMMANDS:
            return True, "Command is in safe list"
        
        # Check if command starts with safe command
        for safe_cmd in SAFE_COMMANDS:
            if command.startswith(safe_cmd + ' '):
                return True, f"Command starts with safe command: {safe_cmd}"
        
        # Check safe patterns
        for pattern in SAFE_PATTERNS:
            if re.match(pattern, command):
                return True, f"Command matches safe pattern: {pattern}"
        
        # Check custom safe commands from config
        for safe_cmd in self.config.get('additional_safe_commands', []):
            if command.startswith(safe_cmd):
                return True, f"Command in custom safe list: {safe_cmd}"
        
        return False, None
    
    def is_dangerous_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """Check if command is potentially dangerous"""
        
        # Check dangerous commands
        cmd_parts = command.split()
        if cmd_parts and cmd_parts[0] in DANGEROUS_COMMANDS:
            return True, f"Command '{cmd_parts[0]}' requires approval"
        
        # Check dangerous patterns
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, command):
                return True, f"Command matches dangerous pattern: {pattern}"
        
        # Check custom dangerous commands
        for danger_cmd in self.config.get('additional_dangerous_commands', []):
            if command.startswith(danger_cmd):
                return True, f"Command in custom dangerous list: {danger_cmd}"
        
        # Production environment checks
        if self.context['is_production']:
            # In production, be more restrictive
            write_operations = ['write', 'create', 'update', 'delete', 'drop', 'truncate']
            for op in write_operations:
                if op in command.lower():
                    return True, "Write operation in production environment"
        
        return False, None
    
    def analyze_command(self, command: str) -> Dict:
        """Analyze a command and determine if it needs approval"""
        
        # Check if safe
        is_safe, safe_reason = self.is_safe_command(command)
        if is_safe:
            return {
                'needs_approval': False,
                'reason': safe_reason,
                'risk_level': 'low',
                'auto_approve': True
            }
        
        # Check if dangerous
        is_dangerous, danger_reason = self.is_dangerous_command(command)
        if is_dangerous:
            return {
                'needs_approval': True,
                'reason': danger_reason,
                'risk_level': 'high',
                'auto_approve': False
            }
        
        # Apply custom rules
        for rule in self.config.get('custom_rules', []):
            if re.match(rule.get('pattern', ''), command):
                return {
                    'needs_approval': rule.get('needs_approval', True),
                    'reason': rule.get('reason', 'Matches custom rule'),
                    'risk_level': rule.get('risk_level', 'medium'),
                    'auto_approve': rule.get('auto_approve', False)
                }
        
        # Default: require approval for unknown commands
        return {
            'needs_approval': True,
            'reason': 'Command not in safe list',
            'risk_level': 'medium',
            'auto_approve': False
        }
    
    def get_statistics(self) -> Dict:
        """Get command approval statistics"""
        stats_file = '.claude/hooks/approval_stats.json'
        
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                stats = json.load(f)
        else:
            stats = {
                'total_commands': 0,
                'auto_approved': 0,
                'user_approved': 0,
                'rejected': 0,
                'by_risk_level': {'low': 0, 'medium': 0, 'high': 0}
            }
        
        return stats
    
    def update_statistics(self, command: str, result: Dict, approved: bool):
        """Update command approval statistics"""
        stats = self.get_statistics()
        
        stats['total_commands'] += 1
        
        if result['auto_approve']:
            stats['auto_approved'] += 1
        elif approved:
            stats['user_approved'] += 1
        else:
            stats['rejected'] += 1
        
        risk_level = result.get('risk_level', 'medium')
        stats['by_risk_level'][risk_level] = stats['by_risk_level'].get(risk_level, 0) + 1
        
        # Save stats
        stats_file = '.claude/hooks/approval_stats.json'
        os.makedirs(os.path.dirname(stats_file), exist_ok=True)
        
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        
        # Log command for audit
        self.log_command(command, result, approved)
    
    def log_command(self, command: str, result: Dict, approved: bool):
        """Log command for audit trail"""
        log_file = '.claude/hooks/command_audit.log'
        
        import datetime
        log_entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'command': command,
            'risk_level': result.get('risk_level'),
            'auto_approved': result.get('auto_approve'),
            'user_approved': approved and not result.get('auto_approve'),
            'reason': result.get('reason'),
            'user': self.context.get('user'),
            'cwd': self.context.get('cwd')
        }
        
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def print_statistics(self):
        """Print approval statistics"""
        stats = self.get_statistics()
        
        if stats['total_commands'] > 0:
            auto_approve_rate = (stats['auto_approved'] / stats['total_commands']) * 100
            
            print(f"\n📊 Command Approval Statistics:")
            print(f"  Total Commands: {stats['total_commands']}")
            print(f"  Auto-Approved: {stats['auto_approved']} ({auto_approve_rate:.1f}%)")
            print(f"  User-Approved: {stats['user_approved']}")
            print(f"  Rejected: {stats['rejected']}")
            print(f"  Risk Levels: Low={stats['by_risk_level']['low']}, "
                  f"Medium={stats['by_risk_level']['medium']}, "
                  f"High={stats['by_risk_level']['high']}")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: command-approval.py <command>")
        sys.exit(1)
    
    command = ' '.join(sys.argv[1:])
    approver = CommandApproval()
    
    # Analyze command
    result = approver.analyze_command(command)
    
    # Output result
    output = {
        'command': command,
        'needs_approval': result['needs_approval'],
        'auto_approve': result['auto_approve'],
        'reason': result['reason'],
        'risk_level': result['risk_level']
    }
    
    print(json.dumps(output))
    
    # Update statistics (assume approved if auto-approve)
    approver.update_statistics(command, result, result['auto_approve'])
    
    # Print statistics occasionally
    import random
    if random.random() < 0.1:  # 10% chance
        approver.print_statistics()
    
    # Exit with appropriate code
    sys.exit(0 if result['auto_approve'] else 1)

if __name__ == '__main__':
    main()