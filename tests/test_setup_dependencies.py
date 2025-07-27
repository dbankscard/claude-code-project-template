import unittest
import tempfile
import shutil
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from setup_dependencies import DependencyManager

class TestDependencyManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.manager = DependencyManager(self.test_dir)
        
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
    def test_detect_project_type_python(self):
        pyproject_path = os.path.join(self.test_dir, "pyproject.toml")
        with open(pyproject_path, "w") as f:
            f.write("[tool.poetry]\nname = 'test'\n")
            
        project_type = self.manager.detect_project_type()
        self.assertEqual(project_type, "python")
        
    def test_detect_project_type_node(self):
        package_json_path = os.path.join(self.test_dir, "package.json")
        with open(package_json_path, "w") as f:
            json.dump({"name": "test", "version": "1.0.0"}, f)
            
        project_type = self.manager.detect_project_type()
        self.assertEqual(project_type, "node")
        
    def test_install_python_dependencies(self):
        requirements_path = os.path.join(self.test_dir, "requirements.txt")
        with open(requirements_path, "w") as f:
            f.write("# test requirements\n")
            
        success = self.manager.install_python_dependencies()
        self.assertTrue(success)
        
    def test_install_node_dependencies(self):
        package_json_path = os.path.join(self.test_dir, "package.json")
        with open(package_json_path, "w") as f:
            json.dump({"name": "test", "version": "1.0.0", "dependencies": {}}, f)
            
        success = self.manager.install_node_dependencies()
        self.assertTrue(success)
        
    def test_setup_dev_tools(self):
        success = self.manager.setup_dev_tools("python")
        self.assertTrue(success)
        
    def test_verify_installation_python(self):
        success = self.manager.verify_installation("python")
        self.assertTrue(success)

if __name__ == "__main__":
    unittest.main()