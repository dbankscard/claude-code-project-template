import unittest
import tempfile
import shutil
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from initialize_project import ProjectInitializer

class TestProjectInitializer(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.project_name = "test-project"
        
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
    def test_validate_project_name_valid(self):
        initializer = ProjectInitializer("valid-project-name")
        initializer.validate_project_name()
        
    def test_validate_project_name_invalid(self):
        invalid_names = ["project with spaces", "project@special", "123project"]
        for name in invalid_names:
            with self.assertRaises(ValueError):
                initializer = ProjectInitializer(name)
                initializer.validate_project_name()
                
    def test_copy_template_structure(self):
        project_path = os.path.join(self.test_dir, self.project_name)
        initializer = ProjectInitializer(self.project_name, base_dir=self.test_dir)
        initializer.copy_template_structure(project_path)
        
        expected_dirs = [
            ".claude/agents",
            ".claude/commands/dev",
            ".claude/commands/project",
            ".claude/commands/git",
            ".claude/commands/security",
            ".claude/hooks",
            "src",
            "tests",
            "docs/guides",
            "docs/ai-context",
            ".github/workflows"
        ]
        
        for dir_path in expected_dirs:
            full_path = os.path.join(project_path, dir_path)
            self.assertTrue(os.path.exists(full_path), f"Directory {dir_path} not created")
            
    def test_customize_templates(self):
        project_path = os.path.join(self.test_dir, self.project_name)
        initializer = ProjectInitializer(self.project_name, base_dir=self.test_dir)
        
        os.makedirs(project_path, exist_ok=True)
        
        test_template = os.path.join(project_path, "test.template")
        with open(test_template, "w") as f:
            f.write("Project: {{PROJECT_NAME}}\nType: {{PROJECT_TYPE}}")
            
        initializer.customize_templates(project_path)
        
        output_file = os.path.join(project_path, "test")
        self.assertTrue(os.path.exists(output_file))
        
        with open(output_file, "r") as f:
            content = f.read()
            self.assertIn(self.project_name, content)
            self.assertIn("python", content)
            
    def test_setup_git_repository(self):
        project_path = os.path.join(self.test_dir, self.project_name)
        os.makedirs(project_path, exist_ok=True)
        
        initializer = ProjectInitializer(self.project_name, base_dir=self.test_dir)
        initializer.setup_git_repository(project_path)
        
        git_dir = os.path.join(project_path, ".git")
        self.assertTrue(os.path.exists(git_dir))
        
    def test_dry_run_mode(self):
        initializer = ProjectInitializer(self.project_name, base_dir=self.test_dir, dry_run=True)
        project_path = initializer.initialize()
        
        self.assertFalse(os.path.exists(project_path))

if __name__ == "__main__":
    unittest.main()