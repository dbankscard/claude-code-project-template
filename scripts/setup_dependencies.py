#!/usr/bin/env python3
"""
Setup and manage project dependencies
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path
from typing import List, Dict, Optional

class DependencyManager:
    def __init__(self, project_dir: Optional[Path] = None):
        self.project_dir = project_dir or Path.cwd()
        self.venv_path = self.project_dir / 'venv'
        self.system = platform.system().lower()
        
    def setup_all(self):
        """Setup all dependencies and tools"""
        print("🔧 Setting up project dependencies...\n")
        
        # Python dependencies
        self.setup_python_environment()
        
        # Node.js dependencies (if package.json exists)
        if (self.project_dir / 'package.json').exists():
            self.setup_node_dependencies()
        
        # Development tools
        self.setup_dev_tools()
        
        # Pre-commit hooks
        self.setup_pre_commit_hooks()
        
        # Claude Code specific setup
        self.setup_claude_code()
        
        print("\n✅ All dependencies set up successfully!")
    
    def setup_python_environment(self):
        """Setup Python environment and dependencies"""
        print("🐍 Setting up Python environment...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 12):
            print(f"⚠️  Warning: Python {python_version.major}.{python_version.minor} detected.")
            print("   Python 3.12+ is recommended for this template.")
        
        # Create virtual environment if it doesn't exist
        if not self.venv_path.exists():
            print("  Creating virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', str(self.venv_path)], check=True)
        
        # Get pip path
        pip_path = self.get_pip_path()
        
        # Upgrade pip
        print("  Upgrading pip...")
        subprocess.run([str(pip_path), 'install', '--upgrade', 'pip'], capture_output=True)
        
        # Install requirements
        requirements_files = [
            'requirements.txt',
            'requirements-dev.txt',
            'requirements-test.txt'
        ]
        
        for req_file in requirements_files:
            req_path = self.project_dir / req_file
            if req_path.exists():
                print(f"  Installing {req_file}...")
                subprocess.run([str(pip_path), 'install', '-r', str(req_path)], check=True)
        
        # Install package in editable mode if setup.py exists
        if (self.project_dir / 'setup.py').exists():
            print("  Installing package in editable mode...")
            subprocess.run([str(pip_path), 'install', '-e', '.'], check=True)
        
        print("✅ Python environment ready")
    
    def setup_node_dependencies(self):
        """Setup Node.js dependencies"""
        print("\n📦 Setting up Node.js dependencies...")
        
        # Check if npm is available
        try:
            subprocess.run(['npm', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  npm not found. Skipping Node.js setup.")
            print("   Install Node.js from https://nodejs.org/")
            return
        
        # Install dependencies
        print("  Installing npm packages...")
        subprocess.run(['npm', 'install'], cwd=self.project_dir, check=True)
        
        print("✅ Node.js dependencies installed")
    
    def setup_dev_tools(self):
        """Setup development tools"""
        print("\n🛠️  Setting up development tools...")
        
        pip_path = self.get_pip_path()
        
        # Python development tools
        python_tools = {
            'black': 'Code formatter',
            'isort': 'Import sorter',
            'flake8': 'Linter',
            'mypy': 'Type checker',
            'pytest': 'Testing framework',
            'pytest-cov': 'Coverage plugin',
            'pre-commit': 'Git hooks manager'
        }
        
        print("  Installing Python development tools:")
        for tool, description in python_tools.items():
            try:
                # Check if already installed
                result = subprocess.run(
                    [str(pip_path), 'show', tool],
                    capture_output=True
                )
                if result.returncode == 0:
                    print(f"    ✓ {tool} ({description}) - already installed")
                else:
                    print(f"    Installing {tool} ({description})...")
                    subprocess.run(
                        [str(pip_path), 'install', tool],
                        capture_output=True,
                        check=True
                    )
                    print(f"    ✓ {tool} installed")
            except subprocess.CalledProcessError:
                print(f"    ⚠️  Failed to install {tool}")
        
        # Create tool configuration files if they don't exist
        self.create_tool_configs()
        
        print("✅ Development tools ready")
    
    def create_tool_configs(self):
        """Create configuration files for development tools"""
        configs = {
            '.flake8': """[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,venv,build,dist
""",
            '.isort.cfg': """[settings]
profile = black
line_length = 88
""",
            'mypy.ini': """[mypy]
python_version = 3.12
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
"""
        }
        
        for filename, content in configs.items():
            config_path = self.project_dir / filename
            if not config_path.exists():
                config_path.write_text(content)
    
    def setup_pre_commit_hooks(self):
        """Setup pre-commit hooks"""
        print("\n🪝 Setting up pre-commit hooks...")
        
        # Create .pre-commit-config.yaml if it doesn't exist
        pre_commit_config = self.project_dir / '.pre-commit-config.yaml'
        if not pre_commit_config.exists():
            pre_commit_config.write_text("""repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-merge-conflict
      
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.12
        
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        
  - repo: local
    hooks:
      - id: security-check
        name: Security Check
        entry: python .claude/hooks/security-check.py
        language: python
        pass_filenames: true
""")
        
        # Install pre-commit
        pip_path = self.get_pip_path()
        subprocess.run([str(pip_path), 'install', 'pre-commit'], capture_output=True)
        
        # Install the git hooks
        pre_commit_path = self.venv_path / ('Scripts' if self.system == 'windows' else 'bin') / 'pre-commit'
        if pre_commit_path.exists():
            print("  Installing git hooks...")
            subprocess.run([str(pre_commit_path), 'install'], capture_output=True)
            print("✅ Pre-commit hooks installed")
        else:
            print("⚠️  pre-commit not found in virtual environment")
    
    def setup_claude_code(self):
        """Setup Claude Code specific configurations"""
        print("\n🤖 Setting up Claude Code integration...")
        
        # Ensure .claude directory exists
        claude_dir = self.project_dir / '.claude'
        claude_dir.mkdir(exist_ok=True)
        
        # Create settings.json if it doesn't exist
        settings_file = claude_dir / 'settings.json'
        if not settings_file.exists():
            settings = {
                "auto_approval": {
                    "enabled": True,
                    "percentage_target": 90
                },
                "hooks": {
                    "auto_format": True,
                    "security_check": True,
                    "intelligent_automation": True
                },
                "agents": {
                    "auto_trigger": True,
                    "preferred_agents": [
                        "code_reviewer",
                        "test_engineer",
                        "security_auditor"
                    ]
                }
            }
            settings_file.write_text(json.dumps(settings, indent=2))
        
        # Make hook scripts executable
        hooks_dir = claude_dir / 'hooks'
        if hooks_dir.exists():
            for hook_file in hooks_dir.glob('*.sh'):
                os.chmod(hook_file, 0o755)
            for hook_file in hooks_dir.glob('*.py'):
                os.chmod(hook_file, 0o755)
        
        print("✅ Claude Code integration configured")
    
    def get_pip_path(self) -> Path:
        """Get the path to pip in the virtual environment"""
        if self.system == 'windows':
            return self.venv_path / 'Scripts' / 'pip'
        return self.venv_path / 'bin' / 'pip'
    
    def check_system_requirements(self):
        """Check system requirements"""
        print("🔍 Checking system requirements...\n")
        
        requirements = {
            'Python': self.check_python(),
            'Git': self.check_git(),
            'Node.js': self.check_node(),
            'Docker': self.check_docker()
        }
        
        all_good = True
        for tool, (installed, version) in requirements.items():
            if installed:
                print(f"✅ {tool}: {version}")
            else:
                print(f"❌ {tool}: Not found")
                if tool in ['Python', 'Git']:
                    all_good = False
        
        if not all_good:
            print("\n⚠️  Some required tools are missing!")
            sys.exit(1)
        
        print("\n✅ All requirements satisfied")
    
    def check_python(self) -> tuple[bool, str]:
        """Check Python installation"""
        try:
            version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            return True, version
        except:
            return False, "Not found"
    
    def check_git(self) -> tuple[bool, str]:
        """Check Git installation"""
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return True, result.stdout.strip()
        except:
            pass
        return False, "Not found"
    
    def check_node(self) -> tuple[bool, str]:
        """Check Node.js installation"""
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return True, result.stdout.strip()
        except:
            pass
        return False, "Not found (optional)"
    
    def check_docker(self) -> tuple[bool, str]:
        """Check Docker installation"""
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return True, result.stdout.strip()
        except:
            pass
        return False, "Not found (optional)"

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup project dependencies")
    parser.add_argument('--check', action='store_true', help='Only check requirements')
    parser.add_argument('--python-only', action='store_true', help='Only setup Python dependencies')
    parser.add_argument('--project-dir', type=Path, default=Path.cwd(), help='Project directory')
    
    args = parser.parse_args()
    
    manager = DependencyManager(args.project_dir)
    
    if args.check:
        manager.check_system_requirements()
    else:
        manager.check_system_requirements()
        print("\n" + "="*60 + "\n")
        
        if args.python_only:
            manager.setup_python_environment()
        else:
            manager.setup_all()

if __name__ == '__main__':
    main()