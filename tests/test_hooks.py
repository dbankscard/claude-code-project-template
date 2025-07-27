import unittest
import os
import stat
import subprocess
from pathlib import Path

class TestHookScripts(unittest.TestCase):
    def setUp(self):
        self.hooks_dir = Path(__file__).parent.parent / "template" / ".claude" / "hooks"
        self.expected_hooks = [
            "auto-format.sh",
            "command-approval.py",
            "intelligent-automation.py",
            "security-check.py"
        ]
        
    def test_all_hooks_exist(self):
        for hook in self.expected_hooks:
            hook_path = self.hooks_dir / hook
            self.assertTrue(hook_path.exists(), f"Hook {hook} not found")
            
    def test_hooks_are_executable(self):
        for hook in self.expected_hooks:
            hook_path = self.hooks_dir / hook
            if hook_path.exists():
                file_stat = os.stat(hook_path)
                is_executable = bool(file_stat.st_mode & stat.S_IXUSR)
                self.assertTrue(is_executable, f"Hook {hook} is not executable")
                
    def test_python_hooks_syntax(self):
        python_hooks = [h for h in self.expected_hooks if h.endswith('.py')]
        
        for hook in python_hooks:
            hook_path = self.hooks_dir / hook
            if hook_path.exists():
                result = subprocess.run(
                    ["python", "-m", "py_compile", str(hook_path)],
                    capture_output=True,
                    text=True
                )
                self.assertEqual(result.returncode, 0,
                               f"Syntax error in {hook}: {result.stderr}")
                               
    def test_bash_hooks_syntax(self):
        bash_hooks = [h for h in self.expected_hooks if h.endswith('.sh')]
        
        for hook in bash_hooks:
            hook_path = self.hooks_dir / hook
            if hook_path.exists():
                result = subprocess.run(
                    ["bash", "-n", str(hook_path)],
                    capture_output=True,
                    text=True
                )
                self.assertEqual(result.returncode, 0,
                               f"Syntax error in {hook}: {result.stderr}")
                               
    def test_hooks_have_shebang(self):
        for hook in self.expected_hooks:
            hook_path = self.hooks_dir / hook
            if hook_path.exists():
                with open(hook_path, "r") as f:
                    first_line = f.readline().strip()
                    
                self.assertTrue(first_line.startswith("#!"),
                              f"Hook {hook} missing shebang")
                              
    def test_command_approval_hook_logic(self):
        hook_path = self.hooks_dir / "command-approval.py"
        if hook_path.exists():
            with open(hook_path, "r") as f:
                content = f.read()
                
            self.assertIn("SAFE_COMMANDS", content)
            self.assertIn("needs_approval", content)
            self.assertIn("sys.exit", content)

if __name__ == "__main__":
    unittest.main()