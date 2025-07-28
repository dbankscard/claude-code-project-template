import unittest
import os
import re
import yaml
from pathlib import Path

class TestCommandDefinitions(unittest.TestCase):
    def setUp(self):
        self.commands_dir = Path(__file__).parent.parent / "template" / ".claude" / "commands"
        self.required_frontmatter = ["name", "namespace", "description"]
        self.required_sections = ["## Usage"]
        
    def test_all_command_categories_exist(self):
        expected_categories = ["dev", "project", "git", "security"]
        
        for category in expected_categories:
            category_path = self.commands_dir / category
            self.assertTrue(category_path.exists(), f"Category {category} not found")
            self.assertTrue(category_path.is_dir(), f"{category} is not a directory")
            
    def test_expected_commands_exist(self):
        expected_commands = {
            "dev": ["feature.md", "review.md", "test.md"],
            "project": ["plan.md"],
            "git": ["commit.md"],
            "security": ["audit.md"]
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
                    
                    # Check for YAML frontmatter
                    self.assertTrue(content.startswith("---\n"), 
                                  f"Missing YAML frontmatter in {command_file}")
                    
                    # Extract and validate frontmatter
                    parts = content.split("---\n", 2)
                    if len(parts) >= 3:
                        try:
                            frontmatter = yaml.safe_load(parts[1])
                            for field in self.required_frontmatter:
                                self.assertIn(field, frontmatter,
                                            f"Missing {field} in frontmatter of {command_file}")
                        except yaml.YAMLError:
                            self.fail(f"Invalid YAML frontmatter in {command_file}")
                    
                    # Check for required sections
                    for section in self.required_sections:
                        self.assertIn(section, content,
                                    f"Missing {section} in {command_file}")
                                    
    def test_command_frontmatter_values(self):
        for category_dir in self.commands_dir.iterdir():
            if category_dir.is_dir():
                category_name = category_dir.name
                for command_file in category_dir.glob("*.md"):
                    command_name = command_file.stem
                    
                    with open(command_file, "r") as f:
                        content = f.read()
                    
                    parts = content.split("---\n", 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])
                        
                        # Check namespace matches directory
                        self.assertEqual(frontmatter.get("namespace"), category_name,
                                       f"Namespace mismatch in {command_file}")
                        
                        # Check name matches filename
                        self.assertEqual(frontmatter.get("name"), command_name,
                                       f"Name mismatch in {command_file}")
                                   
    def test_usage_format(self):
        for category_dir in self.commands_dir.iterdir():
            if category_dir.is_dir():
                for command_file in category_dir.glob("*.md"):
                    with open(command_file, "r") as f:
                        content = f.read()
                    
                    # Look for usage section - it might be in a code block
                    usage_match = re.search(r"## Usage\n(?:```\n)?(.+?)(?:\n```|\n\n)", content, re.DOTALL)
                    self.assertIsNotNone(usage_match,
                                       f"No usage found in {command_file}")
                    
                    usage = usage_match.group(1).strip()
                    # Check if usage contains the namespace
                    category_name = category_dir.name
                    self.assertIn(f"/{category_name}:", usage,
                                f"Usage doesn't contain namespace in {command_file}")

if __name__ == "__main__":
    unittest.main()