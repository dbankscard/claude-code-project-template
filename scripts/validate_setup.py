#!/usr/bin/env python3
"""
Validate Claude Code project setup
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class SetupValidator:
    def __init__(self, project_dir: Optional[Path] = None):
        self.project_dir = project_dir or Path.cwd()
        self.issues = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_failed = 0
        
    def validate(self) -> bool:
        """Run all validation checks"""
        print("🔍 Validating Claude Code project setup...\n")
        
        checks = [
            ("Project Structure", self.check_project_structure),
            ("Claude Configuration", self.check_claude_configuration),
            ("Git Repository", self.check_git_setup),
            ("Python Environment", self.check_python_environment),
            ("Dependencies", self.check_dependencies),
            ("Hooks", self.check_hooks),
            ("Sub-Agents", self.check_subagents),
            ("Commands", self.check_commands),
            ("Documentation", self.check_documentation),
            ("Security", self.check_security)
        ]
        
        for check_name, check_func in checks:
            print(f"Checking {check_name}...")
            try:
                result = check_func()
                if result:
                    print(f"  ✅ {check_name} - OK")
                    self.checks_passed += 1
                else:
                    print(f"  ❌ {check_name} - FAILED")
                    self.checks_failed += 1
            except Exception as e:
                print(f"  ❌ {check_name} - ERROR: {e}")
                self.checks_failed += 1
                self.issues.append(f"{check_name}: {str(e)}")
        
        # Display summary
        self.display_summary()
        
        return self.checks_failed == 0
    
    def check_project_structure(self) -> bool:
        """Check if required project structure exists"""
        required_dirs = [
            '.claude',
            '.claude/agents',
            '.claude/commands',
            '.claude/hooks',
            'src',
            'tests',
            'docs'
        ]
        
        required_files = [
            'CLAUDE.md',
            'README.md',
            '.gitignore'
        ]
        
        missing_dirs = []
        missing_files = []
        
        for dir_path in required_dirs:
            if not (self.project_dir / dir_path).exists():
                missing_dirs.append(dir_path)
        
        for file_path in required_files:
            if not (self.project_dir / file_path).exists():
                missing_files.append(file_path)
        
        if missing_dirs:
            self.issues.append(f"Missing directories: {', '.join(missing_dirs)}")
        
        if missing_files:
            self.issues.append(f"Missing files: {', '.join(missing_files)}")
        
        return len(missing_dirs) == 0 and len(missing_files) == 0
    
    def check_claude_configuration(self) -> bool:
        """Check Claude-specific configuration"""
        claude_dir = self.project_dir / '.claude'
        
        # Check settings.json
        settings_file = claude_dir / 'settings.json'
        if settings_file.exists():
            try:
                with open(settings_file) as f:
                    settings = json.load(f)
                
                # Validate settings structure
                required_keys = ['auto_approval', 'hooks', 'agents']
                missing_keys = [k for k in required_keys if k not in settings]
                
                if missing_keys:
                    self.warnings.append(f"Missing settings keys: {', '.join(missing_keys)}")
            except json.JSONDecodeError:
                self.issues.append("Invalid JSON in .claude/settings.json")
                return False
        else:
            self.warnings.append("No .claude/settings.json found (using defaults)")
        
        # Check CLAUDE.md
        claude_md = self.project_dir / 'CLAUDE.md'
        if claude_md.exists():
            content = claude_md.read_text()
            if len(content) < 100:
                self.warnings.append("CLAUDE.md seems too short - add more project context")
        else:
            self.issues.append("CLAUDE.md not found")
            return False
        
        return True
    
    def check_git_setup(self) -> bool:
        """Check git repository setup"""
        git_dir = self.project_dir / '.git'
        
        if not git_dir.exists():
            self.issues.append("Not a git repository")
            return False
        
        # Check git status
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                cwd=self.project_dir
            )
            
            if result.returncode != 0:
                self.issues.append("Git repository has errors")
                return False
            
            # Check for uncommitted changes
            if result.stdout.strip():
                self.warnings.append("Uncommitted changes in repository")
        
        except subprocess.CalledProcessError:
            self.issues.append("Unable to check git status")
            return False
        
        # Check for remote
        try:
            result = subprocess.run(
                ['git', 'remote', '-v'],
                capture_output=True,
                text=True,
                cwd=self.project_dir
            )
            
            if not result.stdout.strip():
                self.warnings.append("No git remote configured")
        
        except subprocess.CalledProcessError:
            pass
        
        return True
    
    def check_python_environment(self) -> bool:
        """Check Python environment setup"""
        venv_path = self.project_dir / 'venv'
        
        if not venv_path.exists():
            self.issues.append("No virtual environment found")
            return False
        
        # Check Python version
        if sys.version_info < (3, 12):
            self.warnings.append(f"Python {sys.version_info.major}.{sys.version_info.minor} detected, 3.12+ recommended")
        
        # Check if venv is activated
        if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            self.warnings.append("Virtual environment not activated")
        
        return True
    
    def check_dependencies(self) -> bool:
        """Check if dependencies are installed"""
        requirements_files = ['requirements.txt', 'requirements-dev.txt']
        
        for req_file in requirements_files:
            req_path = self.project_dir / req_file
            if req_path.exists():
                # Check if requirements are satisfied
                try:
                    if sys.platform == 'win32':
                        pip_path = self.project_dir / 'venv' / 'Scripts' / 'pip'
                    else:
                        pip_path = self.project_dir / 'venv' / 'bin' / 'pip'
                    
                    result = subprocess.run(
                        [str(pip_path), 'check'],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode != 0:
                        self.warnings.append(f"Some dependencies have issues: {result.stdout}")
                
                except:
                    self.warnings.append("Unable to check pip dependencies")
        
        return True
    
    def check_hooks(self) -> bool:
        """Check if hooks are properly set up"""
        hooks_dir = self.project_dir / '.claude' / 'hooks'
        
        if not hooks_dir.exists():
            self.issues.append("Hooks directory not found")
            return False
        
        required_hooks = [
            'auto-format.sh',
            'command-approval.py',
            'intelligent-automation.py',
            'security-check.py'
        ]
        
        missing_hooks = []
        non_executable = []
        
        for hook in required_hooks:
            hook_path = hooks_dir / hook
            if not hook_path.exists():
                missing_hooks.append(hook)
            elif not os.access(hook_path, os.X_OK):
                non_executable.append(hook)
        
        if missing_hooks:
            self.issues.append(f"Missing hooks: {', '.join(missing_hooks)}")
        
        if non_executable:
            self.warnings.append(f"Non-executable hooks: {', '.join(non_executable)}")
        
        # Check pre-commit hooks
        pre_commit_config = self.project_dir / '.pre-commit-config.yaml'
        if not pre_commit_config.exists():
            self.warnings.append("No .pre-commit-config.yaml found")
        
        return len(missing_hooks) == 0
    
    def check_subagents(self) -> bool:
        """Check if sub-agents are properly configured"""
        agents_dir = self.project_dir / '.claude' / 'agents'
        
        if not agents_dir.exists():
            self.issues.append("Agents directory not found")
            return False
        
        required_agents = [
            'master-orchestrator.md',
            'planning-architect.md',
            'code-reviewer.md',
            'test-engineer.md',
            'security-auditor.md',
            'documentation-specialist.md',
            'performance-optimizer.md'
        ]
        
        missing_agents = []
        
        for agent in required_agents:
            if not (agents_dir / agent).exists():
                missing_agents.append(agent)
        
        if missing_agents:
            self.issues.append(f"Missing agents: {', '.join(missing_agents)}")
            return False
        
        return True
    
    def check_commands(self) -> bool:
        """Check if custom commands are properly configured"""
        commands_dir = self.project_dir / '.claude' / 'commands'
        
        if not commands_dir.exists():
            self.issues.append("Commands directory not found")
            return False
        
        command_categories = ['dev', 'project', 'git', 'security']
        missing_categories = []
        
        for category in command_categories:
            category_dir = commands_dir / category
            if not category_dir.exists():
                missing_categories.append(category)
            elif not list(category_dir.glob('*.md')):
                self.warnings.append(f"No commands found in {category}/ directory")
        
        if missing_categories:
            self.issues.append(f"Missing command categories: {', '.join(missing_categories)}")
            return False
        
        return True
    
    def check_documentation(self) -> bool:
        """Check if documentation is present"""
        docs_dir = self.project_dir / 'docs'
        
        if not docs_dir.exists():
            self.warnings.append("No docs directory found")
            return True  # Not critical
        
        # Check for key documentation files
        key_docs = ['README.md', 'CONTRIBUTING.md', 'CHANGELOG.md']
        missing_docs = []
        
        for doc in key_docs:
            doc_path = self.project_dir / doc
            if not doc_path.exists():
                doc_path = docs_dir / doc
                if not doc_path.exists():
                    missing_docs.append(doc)
        
        if missing_docs:
            self.warnings.append(f"Missing documentation: {', '.join(missing_docs)}")
        
        return True
    
    def check_security(self) -> bool:
        """Run basic security checks"""
        security_issues = []
        
        # Check for common security files
        env_file = self.project_dir / '.env'
        if env_file.exists():
            # Check if .env is in .gitignore
            gitignore = self.project_dir / '.gitignore'
            if gitignore.exists():
                gitignore_content = gitignore.read_text()
                if '.env' not in gitignore_content:
                    security_issues.append(".env file not in .gitignore")
            else:
                security_issues.append("No .gitignore file found")
        
        # Check for hardcoded secrets in CLAUDE.md
        claude_md = self.project_dir / 'CLAUDE.md'
        if claude_md.exists():
            content = claude_md.read_text().lower()
            suspicious_patterns = ['password', 'api_key', 'secret', 'token']
            
            for pattern in suspicious_patterns:
                if f'{pattern} = ' in content or f'{pattern}=' in content:
                    self.warnings.append(f"Possible hardcoded {pattern} in CLAUDE.md")
        
        if security_issues:
            self.issues.extend(security_issues)
            return False
        
        return True
    
    def display_summary(self):
        """Display validation summary"""
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        
        total_checks = self.checks_passed + self.checks_failed
        success_rate = (self.checks_passed / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\nChecks Passed: {self.checks_passed}/{total_checks} ({success_rate:.0f}%)")
        
        if self.issues:
            print(f"\n❌ Critical Issues ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  • {issue}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.checks_failed == 0:
            print("\n✅ Project setup is valid!")
            print("\n🚀 You're ready to start developing with Claude Code!")
        else:
            print("\n❌ Project setup has issues that need to be fixed.")
            print("\nRun 'python scripts/setup_dependencies.py' to fix some issues automatically.")
        
        print("="*60)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Claude Code project setup")
    parser.add_argument('--project-dir', type=Path, default=Path.cwd(), 
                       help='Project directory to validate')
    parser.add_argument('--fix', action='store_true',
                       help='Attempt to fix issues automatically')
    
    args = parser.parse_args()
    
    validator = SetupValidator(args.project_dir)
    is_valid = validator.validate()
    
    if not is_valid and args.fix:
        print("\n🔧 Attempting to fix issues...")
        # Import and run setup_dependencies
        from setup_dependencies import DependencyManager
        manager = DependencyManager(args.project_dir)
        manager.setup_all()
        
        # Re-validate
        print("\n🔍 Re-validating after fixes...")
        validator = SetupValidator(args.project_dir)
        is_valid = validator.validate()
    
    sys.exit(0 if is_valid else 1)

if __name__ == '__main__':
    main()