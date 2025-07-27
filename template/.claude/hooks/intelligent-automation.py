#!/usr/bin/env python3
"""
Intelligent automation hook - triggers appropriate sub-agents based on context
"""
import json
import os
import sys
from pathlib import Path

def get_changed_files():
    """Get list of changed files from git."""
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except:
        return []

def analyze_changes(changed_files):
    """Analyze what types of changes were made."""
    changes = {
        'code': False,
        'tests': False,
        'docs': False,
        'config': False,
        'security': False,
        'api': False
    }
    
    for file in changed_files:
        if not file:
            continue
            
        # Code changes
        if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
            changes['code'] = True
            
        # Test changes
        if 'test' in file.lower() or file.endswith('_test.py'):
            changes['tests'] = True
            
        # Documentation changes
        if file.endswith(('.md', '.rst', '.txt')) or 'docs/' in file:
            changes['docs'] = True
            
        # Configuration changes
        if file in ['pyproject.toml', 'package.json', '.env', 'config.py']:
            changes['config'] = True
            
        # Security-sensitive files
        if 'auth' in file.lower() or 'security' in file.lower() or 'crypto' in file.lower():
            changes['security'] = True
            
        # API changes
        if 'api/' in file or 'routes/' in file or 'endpoints/' in file:
            changes['api'] = True
    
    return changes

def recommend_agents(changes):
    """Recommend which sub-agents to invoke based on changes."""
    recommendations = []
    
    if changes['code']:
        recommendations.append({
            'agent': 'code-reviewer',
            'reason': 'Code changes detected - review recommended'
        })
        
    if changes['tests']:
        recommendations.append({
            'agent': 'test-engineer',
            'reason': 'Test changes detected - test validation recommended'
        })
    elif changes['code'] and not changes['tests']:
        recommendations.append({
            'agent': 'test-engineer',
            'reason': 'Code changes without test updates - new tests may be needed'
        })
        
    if changes['docs']:
        recommendations.append({
            'agent': 'documentation-specialist',
            'reason': 'Documentation changes detected - review recommended'
        })
    elif changes['code'] and not changes['docs']:
        recommendations.append({
            'agent': 'documentation-specialist',
            'reason': 'Code changes without documentation updates'
        })
        
    if changes['security']:
        recommendations.append({
            'agent': 'security-auditor',
            'reason': 'Security-sensitive changes detected - audit required',
            'priority': 'high'
        })
        
    if changes['api']:
        recommendations.append({
            'agent': 'planning-architect',
            'reason': 'API changes detected - architectural review recommended'
        })
        
    # If multiple significant changes, recommend orchestrator
    significant_changes = sum(1 for v in changes.values() if v)
    if significant_changes >= 3:
        recommendations.insert(0, {
            'agent': 'master-orchestrator',
            'reason': 'Multiple significant changes detected - orchestration recommended',
            'priority': 'highest'
        })
    
    return recommendations

def main():
    """Main hook entry point."""
    # Get changed files
    changed_files = get_changed_files()
    
    if not changed_files:
        return
    
    # Analyze changes
    changes = analyze_changes(changed_files)
    
    # Get recommendations
    recommendations = recommend_agents(changes)
    
    if recommendations:
        # Output recommendations
        print("\n🤖 Intelligent Automation Recommendations:")
        print("-" * 50)
        
        for rec in recommendations:
            priority = rec.get('priority', 'normal')
            emoji = '🔴' if priority == 'high' else '🟡' if priority == 'highest' else '🟢'
            print(f"{emoji} {rec['agent']}: {rec['reason']}")
        
        print("-" * 50)
        print("💡 Tip: Use these agents to ensure comprehensive quality checks")

if __name__ == '__main__':
    main()