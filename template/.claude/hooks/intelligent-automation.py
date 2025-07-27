#!/usr/bin/env python3
"""
Intelligent automation hook - Triggers appropriate sub-agents based on context
"""

import os
import sys
import json
import re
import subprocess
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path

class IntelligentAutomation:
    def __init__(self):
        self.config = self.load_config()
        self.context = self.analyze_context()
        self.recent_actions = self.load_recent_actions()
    
    def load_config(self) -> Dict:
        """Load automation configuration"""
        config_path = '.claude/hooks/automation.json'
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
        return {
            'triggers': {
                'code_changes': {
                    'enabled': True,
                    'file_threshold': 5,
                    'line_threshold': 100
                },
                'test_failures': {
                    'enabled': True,
                    'auto_fix_attempt': True
                },
                'security_issues': {
                    'enabled': True,
                    'severity_threshold': 'medium'
                },
                'performance_degradation': {
                    'enabled': True,
                    'threshold_percent': 10
                }
            },
            'agents': {
                'code_reviewer': {
                    'trigger_on': ['code_changes', 'pull_request'],
                    'auto_trigger': True
                },
                'test_engineer': {
                    'trigger_on': ['new_feature', 'test_failures'],
                    'auto_trigger': True
                },
                'security_auditor': {
                    'trigger_on': ['security_changes', 'dependency_update'],
                    'auto_trigger': True
                },
                'performance_optimizer': {
                    'trigger_on': ['performance_degradation', 'scale_issues'],
                    'auto_trigger': False
                }
            }
        }
    
    def analyze_context(self) -> Dict:
        """Analyze current context to determine appropriate actions"""
        context = {
            'timestamp': datetime.utcnow().isoformat(),
            'changed_files': self.get_changed_files(),
            'current_branch': self.get_current_branch(),
            'last_commit': self.get_last_commit(),
            'test_status': self.get_test_status(),
            'performance_metrics': self.get_performance_metrics(),
            'security_alerts': self.check_security_alerts()
        }
        
        # Analyze patterns
        context['patterns'] = {
            'is_feature_branch': 'feature/' in context['current_branch'],
            'is_hotfix': 'hotfix/' in context['current_branch'],
            'has_test_changes': any('test' in f for f in context['changed_files']),
            'has_security_changes': self.has_security_changes(context['changed_files']),
            'has_api_changes': any('api' in f for f in context['changed_files']),
            'has_db_changes': any('migration' in f or 'schema' in f for f in context['changed_files'])
        }
        
        return context
    
    def get_changed_files(self) -> List[str]:
        """Get list of changed files"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD~1..HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n') if result.stdout else []
        except:
            return []
    
    def get_current_branch(self) -> str:
        """Get current git branch"""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except:
            return 'unknown'
    
    def get_last_commit(self) -> Dict:
        """Get information about last commit"""
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%H|%an|%ae|%s|%b'],
                capture_output=True,
                text=True,
                check=True
            )
            
            parts = result.stdout.strip().split('|')
            return {
                'hash': parts[0],
                'author': parts[1],
                'email': parts[2],
                'subject': parts[3],
                'body': parts[4] if len(parts) > 4 else ''
            }
        except:
            return {}
    
    def get_test_status(self) -> Dict:
        """Check test status"""
        test_report_paths = [
            'test-results.xml',
            'coverage.xml',
            '.coverage',
            'pytest.xml'
        ]
        
        for path in test_report_paths:
            if os.path.exists(path):
                # Parse test results
                return self.parse_test_results(path)
        
        return {'status': 'unknown', 'passed': 0, 'failed': 0, 'coverage': 0}
    
    def parse_test_results(self, path: str) -> Dict:
        """Parse test result file"""
        # Simplified parsing - in real implementation, use proper XML parser
        try:
            with open(path, 'r') as f:
                content = f.read()
                
                # Extract basic metrics
                passed = len(re.findall(r'<testcase.*?(?:/>|>.*?</testcase>)', content, re.DOTALL))
                failed = len(re.findall(r'<failure', content))
                
                return {
                    'status': 'passed' if failed == 0 else 'failed',
                    'passed': passed - failed,
                    'failed': failed,
                    'total': passed
                }
        except:
            return {'status': 'error', 'passed': 0, 'failed': 0}
    
    def get_performance_metrics(self) -> Dict:
        """Get performance metrics if available"""
        metrics = {
            'response_time': None,
            'throughput': None,
            'error_rate': None,
            'degradation': False
        }
        
        # Check for performance test results
        perf_file = '.claude/metrics/performance.json'
        if os.path.exists(perf_file):
            try:
                with open(perf_file, 'r') as f:
                    data = json.load(f)
                    
                    # Compare with baseline
                    if 'current' in data and 'baseline' in data:
                        current = data['current']
                        baseline = data['baseline']
                        
                        # Check for degradation
                        if current.get('response_time', 0) > baseline.get('response_time', 0) * 1.1:
                            metrics['degradation'] = True
                        
                        metrics.update(current)
            except:
                pass
        
        return metrics
    
    def check_security_alerts(self) -> List[Dict]:
        """Check for security alerts"""
        alerts = []
        
        # Check for vulnerable dependencies
        if os.path.exists('package-lock.json'):
            try:
                result = subprocess.run(
                    ['npm', 'audit', '--json'],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    audit_data = json.loads(result.stdout)
                    if 'vulnerabilities' in audit_data:
                        for severity in ['critical', 'high', 'moderate']:
                            count = audit_data['vulnerabilities'].get(severity, 0)
                            if count > 0:
                                alerts.append({
                                    'type': 'npm_vulnerability',
                                    'severity': severity,
                                    'count': count
                                })
            except:
                pass
        
        # Check for secrets in code
        secret_patterns = [
            (r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']([^"\']+)["\']', 'api_key'),
            (r'(?i)(secret|password)\s*[:=]\s*["\']([^"\']+)["\']', 'secret'),
            (r'(?i)aws[_-]?access[_-]?key[_-]?id\s*[:=]\s*["\']([^"\']+)["\']', 'aws_key'),
        ]
        
        for file in self.context.get('changed_files', []):
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        content = f.read()
                        
                        for pattern, alert_type in secret_patterns:
                            if re.search(pattern, content):
                                alerts.append({
                                    'type': 'exposed_secret',
                                    'severity': 'critical',
                                    'file': file,
                                    'secret_type': alert_type
                                })
                except:
                    pass
        
        return alerts
    
    def has_security_changes(self, files: List[str]) -> bool:
        """Check if changes affect security"""
        security_patterns = [
            'auth', 'security', 'crypto', 'password', 'token',
            'permission', 'access', 'role', 'encryption'
        ]
        
        for file in files:
            for pattern in security_patterns:
                if pattern in file.lower():
                    return True
        
        return False
    
    def determine_required_agents(self) -> List[Tuple[str, str]]:
        """Determine which agents should be triggered"""
        required_agents = []
        
        # Code Review Agent
        if len(self.context['changed_files']) >= self.config['triggers']['code_changes']['file_threshold']:
            required_agents.append(('code_reviewer', 'Significant code changes detected'))
        
        # Test Engineer Agent
        if self.context['test_status']['failed'] > 0:
            required_agents.append(('test_engineer', f"{self.context['test_status']['failed']} tests failing"))
        elif self.context['patterns']['is_feature_branch'] and not self.context['patterns']['has_test_changes']:
            required_agents.append(('test_engineer', 'New feature without tests'))
        
        # Security Auditor Agent
        if self.context['security_alerts']:
            required_agents.append(('security_auditor', f"{len(self.context['security_alerts'])} security alerts"))
        elif self.context['patterns']['has_security_changes']:
            required_agents.append(('security_auditor', 'Security-related changes detected'))
        
        # Performance Optimizer Agent
        if self.context['performance_metrics']['degradation']:
            required_agents.append(('performance_optimizer', 'Performance degradation detected'))
        
        # Documentation Specialist Agent
        if self.context['patterns']['has_api_changes']:
            required_agents.append(('documentation_specialist', 'API changes require documentation update'))
        
        # Planning Architect Agent
        if self.context['patterns']['has_db_changes']:
            required_agents.append(('planning_architect', 'Database changes require architecture review'))
        
        return required_agents
    
    def should_trigger_agent(self, agent: str, reason: str) -> bool:
        """Determine if agent should be auto-triggered"""
        agent_config = self.config['agents'].get(agent, {})
        
        # Check if auto-trigger is enabled
        if not agent_config.get('auto_trigger', True):
            return False
        
        # Check recent actions to avoid spam
        recent_trigger = self.get_recent_trigger(agent)
        if recent_trigger:
            time_since = datetime.utcnow() - datetime.fromisoformat(recent_trigger['timestamp'])
            
            # Don't trigger same agent within 30 minutes
            if time_since < timedelta(minutes=30):
                return False
        
        # Check if in CI environment
        if os.environ.get('CI', 'false').lower() == 'true':
            # More conservative in CI
            return agent in ['test_engineer', 'security_auditor']
        
        return True
    
    def get_recent_trigger(self, agent: str) -> Optional[Dict]:
        """Get most recent trigger for an agent"""
        for action in self.recent_actions:
            if action.get('agent') == agent:
                return action
        return None
    
    def load_recent_actions(self) -> List[Dict]:
        """Load recent automation actions"""
        actions_file = '.claude/hooks/automation_history.json'
        
        if os.path.exists(actions_file):
            try:
                with open(actions_file, 'r') as f:
                    actions = json.load(f)
                    
                    # Keep only recent actions (last 24 hours)
                    cutoff = datetime.utcnow() - timedelta(hours=24)
                    return [
                        a for a in actions
                        if datetime.fromisoformat(a['timestamp']) > cutoff
                    ]
            except:
                pass
        
        return []
    
    def record_action(self, agent: str, reason: str, triggered: bool):
        """Record automation action"""
        action = {
            'timestamp': datetime.utcnow().isoformat(),
            'agent': agent,
            'reason': reason,
            'triggered': triggered,
            'context': {
                'branch': self.context['current_branch'],
                'commit': self.context['last_commit'].get('hash', '')[:8]
            }
        }
        
        self.recent_actions.append(action)
        
        # Save to file
        actions_file = '.claude/hooks/automation_history.json'
        os.makedirs(os.path.dirname(actions_file), exist_ok=True)
        
        with open(actions_file, 'w') as f:
            json.dump(self.recent_actions, f, indent=2)
    
    def trigger_agent(self, agent: str, reason: str):
        """Trigger a specific agent"""
        print(f"🤖 Triggering {agent}: {reason}")
        
        # Map agent to command
        agent_commands = {
            'code_reviewer': '/dev:review',
            'test_engineer': '/dev:test',
            'security_auditor': '/security:audit',
            'performance_optimizer': '/dev:refactor performance',
            'documentation_specialist': '/project:docs',
            'planning_architect': '/project:plan review'
        }
        
        command = agent_commands.get(agent)
        if command:
            # Create a command file for Claude to execute
            command_file = '.claude/pending_commands.txt'
            os.makedirs(os.path.dirname(command_file), exist_ok=True)
            
            with open(command_file, 'a') as f:
                f.write(f"{command} # Auto-triggered: {reason}\n")
            
            print(f"  → Command queued: {command}")
    
    def generate_summary(self) -> str:
        """Generate automation summary"""
        summary = ["🔍 Intelligent Automation Analysis\n"]
        
        # Context summary
        summary.append(f"Branch: {self.context['current_branch']}")
        summary.append(f"Changed files: {len(self.context['changed_files'])}")
        
        if self.context['test_status']['status'] != 'unknown':
            summary.append(f"Tests: {self.context['test_status']['passed']} passed, "
                         f"{self.context['test_status']['failed']} failed")
        
        if self.context['security_alerts']:
            summary.append(f"Security alerts: {len(self.context['security_alerts'])}")
        
        # Required agents
        required_agents = self.determine_required_agents()
        if required_agents:
            summary.append("\n📋 Recommended Actions:")
            for agent, reason in required_agents:
                if self.should_trigger_agent(agent, reason):
                    summary.append(f"  ✅ {agent}: {reason}")
                else:
                    summary.append(f"  ⏸️  {agent}: {reason} (recently triggered)")
        else:
            summary.append("\n✨ No immediate actions required")
        
        return '\n'.join(summary)

def main():
    """Main entry point"""
    automation = IntelligentAutomation()
    
    # Generate summary
    print(automation.generate_summary())
    
    # Determine and trigger required agents
    required_agents = automation.determine_required_agents()
    
    triggered_count = 0
    for agent, reason in required_agents:
        if automation.should_trigger_agent(agent, reason):
            automation.trigger_agent(agent, reason)
            automation.record_action(agent, reason, True)
            triggered_count += 1
        else:
            automation.record_action(agent, reason, False)
    
    if triggered_count > 0:
        print(f"\n🚀 Triggered {triggered_count} automated actions")
    
    # Output for Claude to process
    output = {
        'context': automation.context,
        'required_agents': required_agents,
        'triggered': triggered_count
    }
    
    # Save for other hooks to use
    output_file = '.claude/hooks/automation_output.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == '__main__':
    main()