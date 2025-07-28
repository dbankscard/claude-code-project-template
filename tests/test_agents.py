import unittest
import os
import re
import yaml
from pathlib import Path

class TestAgentDefinitions(unittest.TestCase):
    def setUp(self):
        self.agents_dir = Path(__file__).parent.parent / "template" / ".claude" / "agents"
        self.required_frontmatter = ["name", "description", "tools"]
        self.required_sections = ["## Core Responsibilities", "## Available Sub-Agents", "## Orchestration Patterns"]
        
    def test_all_agents_exist(self):
        expected_agents = [
            "master-orchestrator.md",
            "planning-architect.md",
            "code-reviewer.md",
            "test-engineer.md",
            "security-auditor.md",
            "documentation-specialist.md",
            "performance-optimizer.md"
        ]
        
        for agent in expected_agents:
            agent_path = self.agents_dir / agent
            self.assertTrue(agent_path.exists(), f"Agent {agent} not found")
            
    def test_agent_structure(self):
        for agent_file in self.agents_dir.glob("*.md"):
            with open(agent_file, "r") as f:
                content = f.read()
            
            # Check for YAML frontmatter
            self.assertTrue(content.startswith("---\n"), 
                          f"Missing YAML frontmatter in {agent_file.name}")
            
            # Extract frontmatter
            parts = content.split("---\n", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    for field in self.required_frontmatter:
                        self.assertIn(field, frontmatter,
                                    f"Missing {field} in frontmatter of {agent_file.name}")
                except yaml.YAMLError:
                    self.fail(f"Invalid YAML frontmatter in {agent_file.name}")
            
            # For master-orchestrator, check for required sections
            if agent_file.name == "master-orchestrator.md":
                for section in self.required_sections:
                    self.assertIn(section, content, 
                                f"Missing {section} in {agent_file.name}")
                
    def test_agent_naming_convention(self):
        for agent_file in self.agents_dir.glob("*.md"):
            filename = agent_file.stem
            self.assertTrue(re.match(r"^[a-z-]+$", filename),
                          f"Invalid agent name format: {filename}")
                          
    def test_agent_frontmatter_values(self):
        for agent_file in self.agents_dir.glob("*.md"):
            with open(agent_file, "r") as f:
                content = f.read()
            
            parts = content.split("---\n", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                
                # Check name matches filename
                expected_name = agent_file.stem
                self.assertEqual(frontmatter.get("name"), expected_name,
                               f"Name mismatch in {agent_file.name}")
                
                # Check description is not empty
                self.assertTrue(len(frontmatter.get("description", "")) > 0,
                              f"Empty description in {agent_file.name}")
                
                # Check tools is a string
                self.assertIsInstance(frontmatter.get("tools"), str,
                                    f"Tools should be a string in {agent_file.name}")

if __name__ == "__main__":
    unittest.main()