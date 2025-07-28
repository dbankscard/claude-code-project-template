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
        self.validator = SetupValidator(Path(self.test_dir))
        
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
        
        # Create all required agents
        required_agents = [
            'master-orchestrator.md',
            'planning-architect.md',
            'code-reviewer.md',
            'test-engineer.md',
            'security-auditor.md',
            'documentation-specialist.md',
            'performance-optimizer.md'
        ]
        
        for agent in required_agents:
            agent_path = os.path.join(agents_dir, agent)
            with open(agent_path, "w") as f:
                f.write("# Test Agent\n\nTest content")
            
        result = self.validator.validate_agents()
        self.assertTrue(result)
        
    def test_validate_commands(self):
        # Create all required command categories
        command_categories = ['dev', 'project', 'git', 'security']
        for category in command_categories:
            commands_dir = os.path.join(self.test_dir, ".claude", "commands", category)
            os.makedirs(commands_dir, exist_ok=True)
            
            # Create a test command file for each category
            command_content = f"""# /{category}:test

## Usage
/{category}:test <args>

## Description
Test command for {category} category.

## Examples
/{category}:test example
"""
            
            command_path = os.path.join(commands_dir, "test.md")
            with open(command_path, "w") as f:
                f.write(command_content)
            
        result = self.validator.validate_commands()
        self.assertTrue(result)
        
    def test_check_hooks(self):
        hooks_dir = os.path.join(self.test_dir, ".claude", "hooks")
        os.makedirs(hooks_dir, exist_ok=True)
        
        hook_scripts = ["auto-format.sh", "intelligent-automation.py", 
                       "security-check.py", "test-automation.py"]
        
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