import unittest
import os
import re
from pathlib import Path

class TestCommandDefinitions(unittest.TestCase):
    def setUp(self):
        self.commands_dir = Path(__file__).parent.parent / "template" / ".claude" / "commands"
        self.required_sections = ["## Usage", "## Description", "## Examples"]
        
    def test_all_command_categories_exist(self):
        expected_categories = ["dev", "project", "git", "security"]
        
        for category in expected_categories:
            category_path = self.commands_dir / category
            self.assertTrue(category_path.exists(), f"Category {category} not found")
            self.assertTrue(category_path.is_dir(), f"{category} is not a directory")
            
    def test_expected_commands_exist(self):
        expected_commands = {
            "dev": ["feature.md", "review.md", "test.md", "debug.md", "refactor.md"],
            "project": ["plan.md", "deploy.md", "docs.md", "status.md"],
            "git": ["commit.md", "pr.md", "release.md", "hotfix.md"],
            "security": ["audit.md", "scan.md", "compliance.md"]
        }
        
        for category, commands in expected_commands.items():
            category_path = self.commands_dir / category
            for command in commands:
                command_path = category_path / command
                self.assertTrue(command_path.exists(), 
                              f"Command {category}/{command} not found")
                              
    def test_command_structure(self):
        for category_dir in self.commands_dir.iterdir():
            if category_dir.is_dir():
                for command_file in category_dir.glob("*.md"):
                    with open(command_file, "r") as f:
                        content = f.read()
                        
                    for section in self.required_sections:
                        self.assertIn(section, content,
                                    f"Missing {section} in {command_file}")
                                    
    def test_command_header_format(self):
        for category_dir in self.commands_dir.iterdir():
            if category_dir.is_dir():
                category_name = category_dir.name
                for command_file in category_dir.glob("*.md"):
                    command_name = command_file.stem
                    expected_header = f"# /{category_name}:{command_name}"
                    
                    with open(command_file, "r") as f:
                        first_line = f.readline().strip()
                        
                    self.assertEqual(first_line, expected_header,
                                   f"Invalid header in {command_file}")
                                   
    def test_usage_format(self):
        for category_dir in self.commands_dir.iterdir():
            if category_dir.is_dir():
                for command_file in category_dir.glob("*.md"):
                    with open(command_file, "r") as f:
                        content = f.read()
                        
                    usage_match = re.search(r"## Usage\n(.+)", content)
                    self.assertIsNotNone(usage_match,
                                       f"No usage found in {command_file}")
                                       
                    usage = usage_match.group(1).strip()
                    self.assertTrue(usage.startswith("/"),
                                  f"Usage doesn't start with / in {command_file}")

if __name__ == "__main__":
    unittest.main()