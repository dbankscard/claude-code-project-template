import unittest
import tempfile
import shutil
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from validate_setup import SetupValidator

class TestSetupValidator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.validator = SetupValidator(self.test_dir)
        
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
    def test_check_claude_structure_complete(self):
        claude_dirs = [
            ".claude/agents",
            ".claude/commands/dev",
            ".claude/commands/project", 
            ".claude/commands/git",
            ".claude/commands/security",
            ".claude/hooks"
        ]
        
        for dir_path in claude_dirs:
            os.makedirs(os.path.join(self.test_dir, dir_path), exist_ok=True)
            
        os.makedirs(os.path.join(self.test_dir, ".claude"), exist_ok=True)
        settings_path = os.path.join(self.test_dir, ".claude", "settings.json")
        with open(settings_path, "w") as f:
            json.dump({"version": "1.0.0"}, f)
            
        result = self.validator.check_claude_structure()
        self.assertTrue(result)
        
    def test_check_claude_structure_missing_dirs(self):
        result = self.validator.check_claude_structure()
        self.assertFalse(result)
        
    def test_validate_agents(self):
        agents_dir = os.path.join(self.test_dir, ".claude", "agents")
        os.makedirs(agents_dir, exist_ok=True)
        
        agent_content = """# master-orchestrator

## Role
Orchestrates complex multi-agent workflows.

## Expertise
- Multi-agent coordination

## Activation Triggers
- Complex tasks requiring multiple specialists
"""
        
        agent_path = os.path.join(agents_dir, "master-orchestrator.md")
        with open(agent_path, "w") as f:
            f.write(agent_content)
            
        result = self.validator.validate_agents()
        self.assertTrue(result)
        
    def test_validate_commands(self):
        commands_dir = os.path.join(self.test_dir, ".claude", "commands", "dev")
        os.makedirs(commands_dir, exist_ok=True)
        
        command_content = """# /dev:feature

## Usage
/dev:feature <feature-name> <description>

## Description
Creates a new feature branch and sets up the development environment.

## Examples
/dev:feature user-auth "Add user authentication system"
"""
        
        command_path = os.path.join(commands_dir, "feature.md")
        with open(command_path, "w") as f:
            f.write(command_content)
            
        result = self.validator.validate_commands()
        self.assertTrue(result)
        
    def test_check_hooks(self):
        hooks_dir = os.path.join(self.test_dir, ".claude", "hooks")
        os.makedirs(hooks_dir, exist_ok=True)
        
        hook_scripts = ["auto-format.sh", "command-approval.py", 
                       "intelligent-automation.py", "security-check.py"]
        
        for script in hook_scripts:
            script_path = os.path.join(hooks_dir, script)
            with open(script_path, "w") as f:
                f.write("#!/usr/bin/env python\n# Test hook script")
            os.chmod(script_path, 0o755)
            
        result = self.validator.check_hooks()
        self.assertTrue(result)
        
    def test_validate_documentation(self):
        docs_dirs = ["docs/guides", "docs/ai-context"]
        for dir_path in docs_dirs:
            os.makedirs(os.path.join(self.test_dir, dir_path), exist_ok=True)
            
        claude_md_path = os.path.join(self.test_dir, "CLAUDE.md")
        with open(claude_md_path, "w") as f:
            f.write("# Test Project\n\n## Project Overview\n")
            
        result = self.validator.validate_documentation()
        self.assertTrue(result)
        
    def test_run_full_validation(self):
        report = self.validator.run_full_validation()
        
        self.assertIn("claude_structure", report)
        self.assertIn("agents", report)
        self.assertIn("commands", report)
        self.assertIn("hooks", report)
        self.assertIn("documentation", report)

if __name__ == "__main__":
    unittest.main()