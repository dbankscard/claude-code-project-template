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
        
    def test_sanitize_project_name_valid(self):
        options = {}
        initializer = ProjectInitializer("valid-project-name", options)
        self.assertEqual(initializer.project_name, "valid_project_name")
        
    def test_sanitize_project_name_invalid(self):
        test_cases = [
            ("project with spaces", "project_with_spaces"),
            ("project@special#chars", "projectspecialchars"),
            ("123project", "project_123project")
        ]
        for input_name, expected_name in test_cases:
            options = {}
            initializer = ProjectInitializer(input_name, options)
            self.assertEqual(initializer.project_name, expected_name)
                
    def test_copy_template_structure(self):
        # Create a minimal template structure for testing
        template_dir = Path(self.test_dir) / "template"
        os.makedirs(template_dir / ".claude" / "agents")
        os.makedirs(template_dir / ".claude" / "hooks")
        os.makedirs(template_dir / "src" / "project_name")
        
        # Create some template files
        (template_dir / "CLAUDE.md.template").write_text("# {{PROJECT_NAME}}")
        (template_dir / "pyproject.toml.template").write_text("name = \"{{project_name}}\"")
        
        options = {"force": True}
        initializer = ProjectInitializer(self.project_name, options)
        initializer.template_dir = template_dir
        initializer.project_dir = Path(self.test_dir) / self.project_name
        
        # Create project directory and copy files
        initializer.create_project_directory()
        initializer.copy_template_files()
        
        # Check if files were copied
        self.assertTrue((initializer.project_dir / "CLAUDE.md").exists())
        self.assertTrue((initializer.project_dir / "pyproject.toml").exists())
            
    def test_customize_templates(self):
        project_path = Path(self.test_dir) / self.project_name
        os.makedirs(project_path)
        
        # Create test files
        (project_path / "CLAUDE.md").write_text("Project: {{PROJECT_NAME}}\nName: {{project_name}}")
        (project_path / "pyproject.toml").write_text("name = \"{{project_name}}\"")
        
        options = {"description": "Test Project"}
        initializer = ProjectInitializer(self.project_name, options)
        initializer.project_dir = project_path
        
        initializer.customize_files()
        
        # Check if placeholders were replaced
        claude_content = (project_path / "CLAUDE.md").read_text()
        self.assertIn("Test Project", claude_content)
        self.assertIn("test_project", claude_content)
        
        pyproject_content = (project_path / "pyproject.toml").read_text()
        self.assertIn("test_project", pyproject_content)
            
    def test_init_git_repository(self):
        project_path = Path(self.test_dir) / self.project_name
        os.makedirs(project_path)
        
        # Create a file to commit
        (project_path / "README.md").write_text("# Test Project")
        
        options = {}
        initializer = ProjectInitializer(self.project_name, options)
        initializer.project_dir = project_path
        
        # Mock subprocess to avoid actual git operations in CI
        import subprocess
        original_run = subprocess.run
        
        def mock_run(cmd, *args, **kwargs):
            if cmd[0] == 'git' and cmd[1] == 'init':
                # Create .git directory to simulate git init
                os.makedirs(project_path / ".git", exist_ok=True)
                return subprocess.CompletedProcess(cmd, 0)
            elif cmd[0] == 'git':
                # Mock other git commands
                return subprocess.CompletedProcess(cmd, 0)
            return original_run(cmd, *args, **kwargs)
        
        subprocess.run = mock_run
        try:
            initializer.init_git_repo()
        finally:
            subprocess.run = original_run
        
        git_dir = project_path / ".git"
        self.assertTrue(git_dir.exists())
        
    def test_dry_run_mode(self):
        # Dry run is handled by argparse in main(), not in the class
        # Test that we can create an initializer with dry_run option
        options = {"dry_run": True}
        initializer = ProjectInitializer(self.project_name, options)
        self.assertEqual(initializer.project_name, "test_project")
        self.assertTrue(initializer.options.get("dry_run"))

if __name__ == "__main__":
    unittest.main()