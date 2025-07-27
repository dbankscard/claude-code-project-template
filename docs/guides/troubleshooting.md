# Troubleshooting Guide

This comprehensive guide helps you resolve common issues with the Claude Code Project Template, from setup problems to runtime errors and integration challenges.

## Table of Contents

1. [Setup Issues](#setup-issues)
2. [Command Execution Problems](#command-execution-problems)
3. [Sub-Agent Issues](#sub-agent-issues)
4. [Hook and Automation Problems](#hook-and-automation-problems)
5. [Integration Issues](#integration-issues)
6. [Performance Problems](#performance-problems)
7. [Security and Permissions](#security-and-permissions)
8. [Common Error Messages](#common-error-messages)
9. [Debug Mode and Logging](#debug-mode-and-logging)
10. [Getting Help](#getting-help)

## Setup Issues

### Problem: Project initialization fails

**Symptoms:**
- `initialize_project.py` script errors out
- Project structure not created correctly
- Missing dependencies

**Solutions:**

1. **Check Python version:**
   ```bash
   python --version
   # Should be 3.12 or higher
   ```

2. **Verify pip is up to date:**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Run initialization with verbose output:**
   ```bash
   python scripts/initialize_project.py my-project --verbose
   ```

4. **Manual initialization if script fails:**
   ```bash
   # Create project directory
   mkdir my-project && cd my-project
   
   # Copy template files
   cp -r ../template/* .
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -e ".[dev]"
   ```

### Problem: Claude Code CLI not recognized

**Symptoms:**
- `claude: command not found`
- CLI not starting properly

**Solutions:**

1. **Ensure Claude Code is installed:**
   ```bash
   # Check if installed
   which claude
   
   # If not found, install/reinstall
   pip install claude-code-cli
   ```

2. **Add to PATH if needed:**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export PATH="$HOME/.local/bin:$PATH"
   ```

3. **Verify installation:**
   ```bash
   claude --version
   ```

### Problem: Virtual environment issues

**Symptoms:**
- Import errors
- Missing packages
- Wrong Python version

**Solutions:**

1. **Recreate virtual environment:**
   ```bash
   deactivate  # If currently activated
   rm -rf venv
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -e ".[dev]"
   ```

2. **Verify correct activation:**
   ```bash
   which python
   # Should point to venv/bin/python
   ```

## Command Execution Problems

### Problem: Custom commands not working

**Symptoms:**
- `Unknown command` error
- Commands not triggering expected behavior
- Sub-agents not responding

**Solutions:**

1. **Check command syntax:**
   ```bash
   # Correct format
   /dev:feature user authentication
   
   # Common mistakes
   /dev-feature  # Wrong separator
   dev:feature   # Missing leading slash
   ```

2. **Verify command files exist:**
   ```bash
   ls commands/dev/
   # Should show feature.md, review.md, etc.
   ```

3. **Validate command file format:**
   ```markdown
   # commands/dev/feature.md should have:
   # /dev:feature
   [Description and implementation details]
   ```

4. **Check CLAUDE.md is present:**
   ```bash
   # CLAUDE.md must exist in project root
   cat CLAUDE.md
   ```

### Problem: Auto-approval not working

**Symptoms:**
- Safe commands still requiring confirmation
- Slow development workflow

**Solutions:**

1. **Check auto-approval configuration:**
   ```bash
   # In .claude/config.yaml
   auto_approval:
     enabled: true
     commands:
       - ls
       - pwd
       - git status
   ```

2. **Verify hook permissions:**
   ```bash
   chmod +x hooks/auto-approval.sh
   ```

3. **Test with simple command:**
   ```bash
   # This should execute without confirmation
   > ls
   ```

### Problem: Commands timing out

**Symptoms:**
- Long-running commands fail
- Partial execution

**Solutions:**

1. **Increase timeout settings:**
   ```yaml
   # .claude/config.yaml
   command_timeout: 300  # 5 minutes
   ```

2. **Break down complex commands:**
   ```bash
   # Instead of
   > /dev:feature complete authentication system
   
   # Use
   > /dev:feature user registration
   > /dev:feature login functionality
   > /dev:feature password reset
   ```

## Sub-Agent Issues

### Problem: Sub-agents not triggering

**Symptoms:**
- Expected agents don't activate
- Missing agent responses
- Workflow interruptions

**Solutions:**

1. **Check agent registration:**
   ```python
   # src/agents/__init__.py
   AVAILABLE_AGENTS = {
       "planning_architect": PlanningArchitect,
       "code_reviewer": CodeReviewer,
       # ... all agents should be listed
   }
   ```

2. **Verify agent implementation:**
   ```python
   # Each agent should implement required methods
   class CustomAgent(BaseAgent):
       async def analyze(self, context: dict) -> dict:
           # Implementation required
       
       async def execute(self, task: dict) -> dict:
           # Implementation required
   ```

3. **Test agent directly:**
   ```python
   # Debug script
   from src.agents import get_agent
   
   agent = get_agent("planning_architect")
   result = await agent.analyze({"test": "data"})
   print(result)
   ```

### Problem: Agent coordination failures

**Symptoms:**
- Agents not communicating
- Duplicate work
- Missed handoffs

**Solutions:**

1. **Check orchestrator configuration:**
   ```yaml
   # .claude/orchestrator.yaml
   coordination:
     mode: "sequential"  # or "parallel"
     timeout: 60
     retry_on_failure: true
   ```

2. **Verify message passing:**
   ```python
   # Ensure agents return proper format
   return {
       "status": "success",
       "data": result_data,
       "next_agent": "test_engineer"
   }
   ```

## Hook and Automation Problems

### Problem: Hooks not executing

**Symptoms:**
- Pre/post command hooks not running
- Quality checks skipped
- No automatic formatting

**Solutions:**

1. **Check hook permissions:**
   ```bash
   chmod +x hooks/*.sh
   chmod +x hooks/*.py
   ```

2. **Verify hook configuration:**
   ```yaml
   # .claude/hooks.yaml
   hooks:
     pre_command:
       - trigger: "/dev:feature"
         script: "hooks/pre-feature.sh"
   ```

3. **Test hooks manually:**
   ```bash
   ./hooks/pre-commit.sh
   # Should run without errors
   ```

4. **Check hook logs:**
   ```bash
   tail -f .claude/logs/hooks.log
   ```

### Problem: Hook failures blocking workflow

**Symptoms:**
- Commands fail due to hook errors
- Development blocked

**Solutions:**

1. **Temporarily disable problematic hook:**
   ```yaml
   # .claude/hooks.yaml
   hooks:
     pre_command:
       - trigger: "/dev:feature"
         script: "hooks/problem-hook.sh"
         enabled: false  # Temporarily disable
   ```

2. **Add error handling to hooks:**
   ```bash
   #!/bin/bash
   set -e  # Exit on error
   
   # Add try-catch equivalent
   {
       # Hook logic here
   } || {
       echo "Warning: Hook failed but continuing"
       exit 0  # Don't block workflow
   }
   ```

## Integration Issues

### Problem: Git integration not working

**Symptoms:**
- `/git:commit` fails
- Pull requests not created
- Branch management issues

**Solutions:**

1. **Verify git configuration:**
   ```bash
   git config --list
   # Ensure user.name and user.email are set
   ```

2. **Check remote repository:**
   ```bash
   git remote -v
   # Should show origin URLs
   ```

3. **Test git access:**
   ```bash
   git fetch origin
   # Should complete without errors
   ```

4. **Fix authentication:**
   ```bash
   # For HTTPS
   git config credential.helper store
   
   # For SSH
   ssh-add ~/.ssh/id_rsa
   ```

### Problem: CI/CD pipeline failures

**Symptoms:**
- GitHub Actions failing
- Deployment issues
- Test failures in CI

**Solutions:**

1. **Check workflow syntax:**
   ```yaml
   # Validate YAML syntax
   yamllint .github/workflows/ci.yml
   ```

2. **Verify secrets:**
   ```bash
   # In GitHub settings, ensure secrets are set:
   # - CLAUDE_API_KEY
   # - Other required tokens
   ```

3. **Test locally first:**
   ```bash
   # Run same commands as CI
   npm test
   npm run build
   ```

## Performance Problems

### Problem: Slow command execution

**Symptoms:**
- Commands take too long
- Timeouts
- High CPU/memory usage

**Solutions:**

1. **Profile performance:**
   ```python
   # Add profiling to identify bottlenecks
   import cProfile
   
   cProfile.run('your_slow_function()')
   ```

2. **Optimize file operations:**
   ```python
   # Use batch operations
   # Instead of multiple reads
   files = glob.glob("src/**/*.py")
   contents = [read_file(f) for f in files]
   ```

3. **Limit scope:**
   ```bash
   # Be specific with paths
   > /dev:review src/api/  # Not entire src/
   ```

### Problem: Memory issues with large projects

**Symptoms:**
- Out of memory errors
- Crashes on large codebases

**Solutions:**

1. **Increase memory limits:**
   ```bash
   # Set environment variable
   export CLAUDE_MAX_MEMORY=4G
   ```

2. **Use streaming for large files:**
   ```python
   # Process files in chunks
   def process_large_file(filepath):
       with open(filepath, 'r') as f:
           for chunk in iter(lambda: f.read(4096), ''):
               process_chunk(chunk)
   ```

## Security and Permissions

### Problem: Permission denied errors

**Symptoms:**
- Cannot read/write files
- Hook execution failures
- Command access denied

**Solutions:**

1. **Fix file permissions:**
   ```bash
   # Make scripts executable
   chmod +x scripts/*.py
   chmod +x hooks/*.sh
   
   # Fix directory permissions
   chmod 755 src/ tests/ docs/
   ```

2. **Check user permissions:**
   ```bash
   # Verify ownership
   ls -la
   
   # Fix if needed
   chown -R $(whoami) .
   ```

### Problem: Security scan failures

**Symptoms:**
- `/security:audit` reports issues
- Vulnerability warnings
- Compliance failures

**Solutions:**

1. **Update dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Fix common vulnerabilities:**
   ```python
   # Use parameterized queries
   # Bad
   query = f"SELECT * FROM users WHERE id = {user_id}"
   
   # Good
   query = "SELECT * FROM users WHERE id = ?"
   cursor.execute(query, (user_id,))
   ```

3. **Configure security exceptions:**
   ```yaml
   # .security-ignore
   # Known false positives
   - rule: B105  # Hardcoded password check
     path: tests/fixtures.py
   ```

## Common Error Messages

### "CLAUDE.md not found"

**Solution:**
```bash
# Create basic CLAUDE.md
cat > CLAUDE.md << EOF
# Project Name - AI Context

## 1. Project Overview
- **Vision:** Your project description
- **Current Phase:** Development
- **Key Architecture:** Monolithic/Microservices
EOF
```

### "Agent not available: [agent_name]"

**Solution:**
```python
# Check agent is registered
# In src/agents/__init__.py
AVAILABLE_AGENTS = {
    "agent_name": YourAgentClass,
}
```

### "Hook failed: [hook_name]"

**Solution:**
```bash
# Debug hook
bash -x hooks/hook_name.sh
# Shows each command as it executes
```

### "Command timeout"

**Solution:**
```yaml
# Increase timeout in .claude/config.yaml
timeouts:
  command: 300
  agent: 600
```

## Debug Mode and Logging

### Enable debug mode

```bash
# Set environment variable
export CLAUDE_DEBUG=true

# Or in .env file
CLAUDE_DEBUG=true
```

### Check logs

```bash
# View all logs
tail -f .claude/logs/claude.log

# Filter by component
grep "agent:" .claude/logs/claude.log
grep "hook:" .claude/logs/claude.log
grep "ERROR" .claude/logs/claude.log
```

### Verbose output

```bash
# Run with verbose flag
claude --verbose

# Or set in config
# .claude/config.yaml
logging:
  level: DEBUG
```

### Create diagnostic report

```bash
# Generate full diagnostic
python scripts/diagnostic.py > diagnostic_report.txt

# Share when reporting issues
```

## Getting Help

### Self-Help Resources

1. **Check documentation:**
   - README.md
   - docs/guides/
   - Command help: `/help <command>`

2. **Search existing issues:**
   - [GitHub Issues](https://github.com/dbankscard/claude-code-project-template/issues)
   - Look for similar problems

3. **Community resources:**
   - [GitHub Discussions](https://github.com/dbankscard/claude-code-project-template/discussions)
   - Stack Overflow tags: `claude-code`

### Reporting Issues

When reporting issues, include:

1. **Environment details:**
   ```bash
   claude --version
   python --version
   pip list
   ```

2. **Steps to reproduce:**
   - Exact commands run
   - Expected behavior
   - Actual behavior

3. **Error messages:**
   - Full error output
   - Relevant log entries
   - Stack traces

4. **Minimal reproduction:**
   - Simplest case that shows the problem
   - Remove unrelated code

### Template for Issue Reports

```markdown
## Description
Brief description of the issue

## Environment
- Claude Code version: X.Y.Z
- Python version: 3.12.X
- OS: macOS/Linux/Windows
- Project type: API/Web/CLI

## Steps to Reproduce
1. Run command X
2. See error Y

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Error Output
```
Full error message here
```

## Additional Context
Any other relevant information
```

## Quick Reference Card

### Most Common Fixes

| Issue | Quick Fix |
|-------|-----------|
| Command not found | Check syntax: `/dev:feature` not `dev:feature` |
| Hooks not running | `chmod +x hooks/*.sh` |
| Import errors | Activate venv: `source venv/bin/activate` |
| Git issues | Set remote: `git remote add origin <url>` |
| Slow performance | Be specific: `/dev:review src/api/` |
| Permission denied | Fix permissions: `chmod -R 755 .` |

### Emergency Recovery

```bash
# Reset to clean state
git stash
git checkout main
git pull origin main

# Reinstall dependencies
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Clear Claude cache
rm -rf .claude/cache/

# Restart Claude
claude restart
```

Remember: Most issues have simple solutions. Check the basics first before diving deep into debugging.