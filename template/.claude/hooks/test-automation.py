#!/usr/bin/env python3
"""
Test automation hook - automatically runs relevant tests after code changes
"""
import subprocess
import sys
from pathlib import Path

def find_test_command():
    """Detect the appropriate test command for the project."""
    # Check for common test configurations
    if Path('pyproject.toml').exists():
        # Python project
        if Path('pytest.ini').exists() or 'pytest' in Path('pyproject.toml').read_text():
            return 'pytest'
        return 'python -m pytest'
    
    elif Path('package.json').exists():
        # Node.js project
        try:
            import json
            with open('package.json') as f:
                package = json.load(f)
                if 'scripts' in package and 'test' in package['scripts']:
                    return 'npm test'
        except:
            pass
        return 'npm test'
    
    elif Path('Cargo.toml').exists():
        # Rust project
        return 'cargo test'
    
    elif Path('go.mod').exists():
        # Go project
        return 'go test ./...'
    
    return None

def find_related_tests(changed_file):
    """Find test files related to a changed source file."""
    file_path = Path(changed_file)
    
    # Skip if already a test file
    if 'test' in file_path.name:
        return [changed_file]
    
    # Common test file patterns
    test_patterns = [
        f"test_{file_path.stem}.py",
        f"{file_path.stem}_test.py",
        f"test_{file_path.name}",
        f"{file_path.stem}.test.{file_path.suffix[1:]}",
        f"{file_path.stem}.spec.{file_path.suffix[1:]}"
    ]
    
    # Look for test files
    related_tests = []
    
    # Check in tests directory
    tests_dir = Path('tests')
    if tests_dir.exists():
        for pattern in test_patterns:
            matches = list(tests_dir.rglob(pattern))
            related_tests.extend(str(m) for m in matches)
    
    # Check in same directory
    for pattern in test_patterns:
        test_file = file_path.parent / pattern
        if test_file.exists():
            related_tests.append(str(test_file))
    
    # Check in __tests__ directory (JavaScript convention)
    tests_subdir = file_path.parent / '__tests__'
    if tests_subdir.exists():
        for pattern in test_patterns:
            test_file = tests_subdir / pattern
            if test_file.exists():
                related_tests.append(str(test_file))
    
    return related_tests

def run_tests(test_files=None):
    """Run tests and return results."""
    test_command = find_test_command()
    
    if not test_command:
        return None, "No test framework detected"
    
    if test_files:
        # Run specific test files
        if 'pytest' in test_command:
            cmd = f"{test_command} {' '.join(test_files)}"
        elif 'npm' in test_command:
            # For npm, we might need to use a different approach
            cmd = test_command
        else:
            cmd = test_command
    else:
        # Run all tests
        cmd = test_command
    
    try:
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Tests timed out after 5 minutes"
    except Exception as e:
        return False, f"Error running tests: {e}"

def main():
    """Main hook entry point."""
    # Get changed file if provided
    changed_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    if changed_file and Path(changed_file).suffix in ['.py', '.js', '.ts', '.jsx', '.tsx']:
        # Find related test files
        test_files = find_related_tests(changed_file)
        
        if test_files:
            print(f"\n🧪 Running tests related to {changed_file}...")
            print(f"   Found test files: {', '.join(test_files)}")
        else:
            print(f"\n🧪 No specific tests found for {changed_file}, running all tests...")
            test_files = None
    else:
        print("\n🧪 Running all tests...")
        test_files = None
    
    # Run tests
    success, output = run_tests(test_files)
    
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Test failures detected!")
        print("-" * 50)
        # Show last 20 lines of output for context
        lines = output.split('\n')
        for line in lines[-20:]:
            print(line)
        print("-" * 50)
        print("💡 Tip: Use the test-engineer sub-agent to fix failing tests")

if __name__ == '__main__':
    main()