#!/usr/bin/env python3
"""
Initialize a new project from the Claude Code Project Template
"""

import os
import sys
import shutil
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# Import MCP detection module
from detect_mcp_servers import interactive_mcp_setup

class ProjectInitializer:
    def __init__(self, project_name: str, options: Dict):
        self.project_name = self.sanitize_name(project_name)
        self.project_dir = Path(self.project_name)
        self.template_dir = Path(__file__).parent.parent / "template"
        self.options = options
        
    def sanitize_name(self, name: str) -> str:
        """Sanitize project name for use as directory and package name"""
        # Replace spaces and hyphens with underscores for Python package
        sanitized = name.lower().replace(" ", "_").replace("-", "_")
        # Remove any non-alphanumeric characters except underscores
        sanitized = ''.join(c for c in sanitized if c.isalnum() or c == '_')
        # Ensure it doesn't start with a number
        if sanitized and sanitized[0].isdigit():
            sanitized = f"project_{sanitized}"
        return sanitized or "my_project"
    
    def initialize(self):
        """Main initialization process"""
        print(f"🚀 Initializing Claude Code project: {self.project_name}")
        
        try:
            # Create project directory
            self.create_project_directory()
            
            # Copy template files
            self.copy_template_files()
            
            # Customize files
            self.customize_files()
            
            # Initialize git repository
            if not self.options.get('skip_git'):
                self.init_git_repo()
            
            # Create virtual environment
            if not self.options.get('skip_venv'):
                self.create_virtual_environment()
            
            # Install dependencies
            if not self.options.get('skip_install'):
                self.install_dependencies()
            
            # Configure MCP servers
            if not self.options.get('skip_mcp'):
                self.configure_mcp_servers()
            
            # Generate initial documentation
            self.generate_documentation()
            
            # Display success message
            self.display_success_message()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    def create_project_directory(self):
        """Create the project directory"""
        if self.project_dir.exists():
            if not self.options.get('force'):
                response = input(f"Directory '{self.project_name}' already exists. Overwrite? (y/N): ")
                if response.lower() != 'y':
                    print("Aborted.")
                    sys.exit(0)
            shutil.rmtree(self.project_dir)
        
        self.project_dir.mkdir(parents=True)
        print(f"✅ Created project directory: {self.project_dir}")
    
    def copy_template_files(self):
        """Copy template files to project directory"""
        print("📁 Copying template files...")
        
        # Copy all template files
        for item in self.template_dir.iterdir():
            # Skip .git directory but allow other hidden files/directories
            if item.name == '.git':
                continue
                
            dest = self.project_dir / item.name
            
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)
        
        # Rename template files
        template_files = [
            ('CLAUDE.md.template', 'CLAUDE.md'),
            ('.gitignore.template', '.gitignore'),
            ('pyproject.toml.template', 'pyproject.toml')
        ]
        
        for template_name, final_name in template_files:
            template_path = self.project_dir / template_name
            if template_path.exists():
                template_path.rename(self.project_dir / final_name)
        
        # Rename project_name directory to actual project name
        project_src = self.project_dir / 'src' / 'project_name'
        if project_src.exists():
            project_src.rename(self.project_dir / 'src' / self.project_name)
        
        print("✅ Template files copied")
    
    def customize_files(self):
        """Customize template files with project-specific information"""
        print("🔧 Customizing files...")
        
        replacements = {
            'PROJECT_NAME': self.options.get('display_name', self.project_name.replace('_', ' ').title()),
            'project_name': self.project_name,
            'PROJECT_DESCRIPTION': self.options.get('description', f'A Claude Code project: {self.project_name}'),
            'AUTHOR_NAME': self.options.get('author', 'Your Name'),
            'AUTHOR_EMAIL': self.options.get('email', 'your.email@example.com'),
            'CURRENT_YEAR': str(datetime.now().year),
            'CURRENT_DATE': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Files to customize
        files_to_customize = [
            'CLAUDE.md',
            'README.md',
            'pyproject.toml',
            'setup.py',
            '.claude/settings.json',
            'src/*/__init__.py',
            'tests/conftest.py',
            'docs/source/index.md'
        ]
        
        for pattern in files_to_customize:
            for file_path in self.project_dir.glob(pattern):
                if file_path.is_file():
                    self.replace_in_file(file_path, replacements)
        
        print("✅ Files customized")
    
    def replace_in_file(self, file_path: Path, replacements: Dict[str, str]):
        """Replace placeholders in a file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            for placeholder, value in replacements.items():
                if value is not None:  # Only replace if value is not None
                    # Replace different placeholder formats
                    content = content.replace('{{' + placeholder + '}}', value)     # {{VAR}}
                    content = content.replace('${' + placeholder + '}', value)      # ${VAR}
                    content = content.replace('{' + placeholder + '}', value)       # {VAR}
            
            file_path.write_text(content, encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not customize {file_path}: {e}")
    
    def init_git_repo(self):
        """Initialize git repository"""
        print("🔗 Initializing git repository...")
        
        original_dir = os.getcwd()
        os.chdir(self.project_dir)
        
        # Initialize repo
        subprocess.run(['git', 'init'], check=True, capture_output=True)
        
        # Add all files
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        
        # Initial commit
        subprocess.run(
            ['git', 'commit', '-m', f'🎉 Initial commit: {self.project_name} from Claude Code Template'],
            check=True,
            capture_output=True
        )
        
        # Create main branch
        subprocess.run(['git', 'branch', '-M', 'main'], capture_output=True)
        
        os.chdir(original_dir)
        print("✅ Git repository initialized")
    
    def create_virtual_environment(self):
        """Create Python virtual environment"""
        print("🐍 Creating virtual environment...")
        
        original_dir = os.getcwd()
        os.chdir(self.project_dir)
        
        # Create venv
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        
        os.chdir(original_dir)
        print("✅ Virtual environment created")
    
    def install_dependencies(self):
        """Install project dependencies"""
        print("📦 Installing dependencies...")
        
        original_dir = os.getcwd()
        os.chdir(self.project_dir)
        
        # Determine pip path
        if sys.platform == 'win32':
            pip_path = Path('venv/Scripts/pip')
        else:
            pip_path = Path('venv/bin/pip')
        
        if not pip_path.exists():
            print("⚠️  Virtual environment not found, skipping dependency installation")
            return
        
        # Upgrade pip
        subprocess.run([str(pip_path), 'install', '--upgrade', 'pip'], capture_output=True)
        
        # Install requirements
        requirements_files = ['requirements.txt', 'requirements-dev.txt']
        for req_file in requirements_files:
            if (self.project_dir / req_file).exists():
                subprocess.run(
                    [str(pip_path), 'install', '-r', req_file],
                    capture_output=True
                )
        
        # Install package in editable mode
        if (self.project_dir / 'setup.py').exists():
            subprocess.run([str(pip_path), 'install', '-e', '.'], capture_output=True)
        
        os.chdir(original_dir)
        print("✅ Dependencies installed")
    
    def configure_mcp_servers(self):
        """Configure MCP servers interactively"""
        print("\n🔌 Configuring MCP Servers...")
        
        # Run interactive MCP setup
        mcp_config = interactive_mcp_setup(self.project_dir)
        
        if mcp_config:
            # If .mcp.json template exists and user configured servers, it's already saved
            print("✅ MCP servers configured")
        else:
            # Create a minimal .mcp.json if user skipped
            minimal_config = {
                "servers": {
                    "filesystem": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
                        "settings": {
                            "extensions": [".py", ".js", ".ts", ".json", ".yaml", ".md"],
                            "ignore": ["node_modules", "__pycache__", ".git", "venv"]
                        }
                    }
                },
                "globalSettings": {
                    "timeout": 30000,
                    "retries": 3,
                    "concurrentRequests": 5
                }
            }
            
            mcp_file = self.project_dir / ".mcp.json"
            with open(mcp_file, "w") as f:
                json.dump(minimal_config, f, indent=2)
            
            print("ℹ️  Created minimal .mcp.json with filesystem server")
            print("   You can configure additional MCP servers later.")
    
    def generate_documentation(self):
        """Generate initial documentation"""
        print("📚 Generating documentation...")
        
        # Create additional documentation
        docs_dir = self.project_dir / 'docs'
        docs_dir.mkdir(exist_ok=True)
        
        # Create initial CHANGELOG
        changelog = docs_dir / 'CHANGELOG.md'
        if not changelog.exists():
            changelog.write_text(f"""# Changelog

All notable changes to {self.project_name} will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure from Claude Code Template
- Basic project configuration
- Development environment setup

[Unreleased]: https://github.com/username/{self.project_name}/compare/v0.0.0...HEAD
""")
        
        # Create CONTRIBUTING guide
        contributing = self.project_dir / 'CONTRIBUTING.md'
        if not contributing.exists():
            contributing.write_text(f"""# Contributing to {self.project_name.replace('_', ' ').title()}

We welcome contributions! Please follow these guidelines:

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a virtual environment
4. Install dependencies: `pip install -r requirements-dev.txt`
5. Create a feature branch

## Making Changes

1. Write clear, concise commit messages
2. Add tests for new functionality
3. Ensure all tests pass
4. Update documentation as needed

## Submitting Changes

1. Push to your fork
2. Create a pull request
3. Describe your changes clearly
4. Link any related issues

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Keep functions focused and small

## Testing

Run tests with: `pytest`
Check coverage: `pytest --cov`

Thank you for contributing!
""")
        
        print("✅ Documentation generated")
    
    def display_success_message(self):
        """Display success message with next steps"""
        print("\n" + "="*60)
        print(f"✨ Project '{self.project_name}' initialized successfully!")
        print("="*60 + "\n")
        
        print("📋 Next steps:\n")
        print(f"1. Navigate to your project:")
        print(f"   cd {self.project_name}\n")
        
        if not self.options.get('skip_venv'):
            print("2. Activate virtual environment:")
            if sys.platform == 'win32':
                print("   venv\\Scripts\\activate")
            else:
                print("   source venv/bin/activate")
            print()
        
        print("3. Start Claude Code:")
        print("   claude\n")
        
        print("4. Try your first command:")
        print("   > Use the master-orchestrator to create a user authentication feature\n")
        
        print("💡 MCP Servers:")
        print("   - Check .mcp.json for configured servers")
        print("   - Add environment variables to .env if needed")
        print("   - Run 'python scripts/detect_mcp_servers.py' to reconfigure\n")
        
        print("📚 Resources:")
        print("   - CLAUDE.md: AI context and project configuration")
        print("   - README.md: Project documentation")
        print("   - docs/guides/: Detailed guides\n")
        
        print("🚀 Happy coding with Claude Code!")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude Code project from template"
    )
    
    parser.add_argument(
        'project_name',
        help='Name of the new project'
    )
    
    parser.add_argument(
        '--author',
        help='Author name',
        default=os.environ.get('USER', 'Your Name')
    )
    
    parser.add_argument(
        '--email',
        help='Author email',
        default='your.email@example.com'
    )
    
    parser.add_argument(
        '--description',
        help='Project description',
        default=None
    )
    
    parser.add_argument(
        '--display-name',
        help='Display name for the project',
        default=None
    )
    
    parser.add_argument(
        '--skip-git',
        action='store_true',
        help='Skip git repository initialization'
    )
    
    parser.add_argument(
        '--skip-venv',
        action='store_true',
        help='Skip virtual environment creation'
    )
    
    parser.add_argument(
        '--skip-install',
        action='store_true',
        help='Skip dependency installation'
    )
    
    parser.add_argument(
        '--skip-mcp',
        action='store_true',
        help='Skip MCP server configuration'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force overwrite existing directory'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without doing it'
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        print(f"Would initialize project: {args.project_name}")
        print(f"Options: {vars(args)}")
        return
    
    # Initialize project
    initializer = ProjectInitializer(args.project_name, vars(args))
    initializer.initialize()

if __name__ == '__main__':
    main()