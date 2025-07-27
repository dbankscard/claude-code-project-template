import unittest
import os
import re
from pathlib import Path

class TestAgentDefinitions(unittest.TestCase):
    def setUp(self):
        self.agents_dir = Path(__file__).parent.parent / "template" / ".claude" / "agents"
        self.required_sections = ["## Role", "## Expertise", "## Activation Triggers"]
        
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
                
            for section in self.required_sections:
                self.assertIn(section, content, 
                            f"Missing {section} in {agent_file.name}")
                
    def test_agent_naming_convention(self):
        for agent_file in self.agents_dir.glob("*.md"):
            filename = agent_file.stem
            self.assertTrue(re.match(r"^[a-z-]+$", filename),
                          f"Invalid agent name format: {filename}")
                          
    def test_activation_triggers_format(self):
        for agent_file in self.agents_dir.glob("*.md"):
            with open(agent_file, "r") as f:
                content = f.read()
                
            triggers_match = re.search(r"## Activation Triggers\n((?:- .+\n?)+)", content)
            self.assertIsNotNone(triggers_match, 
                               f"No activation triggers found in {agent_file.name}")
            
            triggers = triggers_match.group(1).strip().split("\n")
            self.assertGreater(len(triggers), 0,
                             f"Empty activation triggers in {agent_file.name}")

if __name__ == "__main__":
    unittest.main()