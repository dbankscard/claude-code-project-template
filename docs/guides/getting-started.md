# Getting Started Guide

Welcome to the Claude Code Project Template! This guide will walk you through setting up your first AI-powered development project with our comprehensive template featuring specialized sub-agents, smart automation, and custom commands.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+** - Required for running the template and its tools
- **Claude Code CLI** - The AI assistant that powers your development workflow
- **Git** - For version control and project management
- **Node.js/npm** (Recommended) - For MCP server support
- **Docker** (Optional) - For containerized development environments

## Installation

### Step 1: Clone the Template

```bash
git clone https://github.com/dbankscard/claude-code-project-template.git my-project
cd my-project
```

### Step 2: Initialize Your Project

Run the initialization script with your project name:

```bash
python scripts/initialize_project.py my-awesome-app
cd my-awesome-app
```

This will:
- Create a new project directory with your chosen name
- Set up the complete project structure
- Configure all sub-agents and automation hooks
- **Detect and configure MCP servers interactively**
- Initialize git repository
- Create virtual environment

### Step 3: Activate Virtual Environment

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -e ".[dev]"
```

## First Steps with Claude Code

### 1. Start Claude Code

```bash
claude
```

### 2. Try Your First Command

The template includes custom commands and the master orchestrator. Here's a simple example:

```bash
> Use the master-orchestrator to create a user authentication feature with OAuth2
```

This command will:
- Trigger the Planning Architect sub-agent to design the feature
- Implement the authentication system
- Create tests automatically
- Run security checks
- Generate documentation

### 3. Review the Generated Code

Claude Code will create files in the appropriate directories:
- `src/` - Source code implementation
- `tests/` - Automated tests
- `docs/` - Generated documentation

## Understanding the Sub-Agent System

Your project comes with 7 specialized sub-agents:

1. **Master Orchestrator** - Coordinates complex workflows
2. **Planning Architect** - Designs technical solutions
3. **Code Reviewer** - Ensures code quality
4. **Test Engineer** - Creates comprehensive tests
5. **Security Auditor** - Checks for vulnerabilities
6. **Documentation Specialist** - Maintains documentation
7. **Performance Optimizer** - Improves code efficiency

## Quick Command Reference

### Development Commands
- `/dev:feature <description>` - Implement new features
- `/dev:review` - Review current code
- `/dev:test` - Create or update tests

### Project Commands
- `/project:plan <description>` - Plan project architecture

### Git Commands
- `/git:commit` - Smart commit with message

### Security Commands
- `/security:audit` - Run security analysis

## MCP Server Integration

During project initialization, the template automatically detects available MCP servers on your system and prompts you to configure them. You can connect to various external tools including:

- **File Systems**: Local filesystem, Google Drive
- **Version Control**: GitHub, GitLab
- **Communication**: Slack, email
- **AI Services**: Gemini consultation, Context7 documentation
- **Automation**: Puppeteer, web scraping
- **And more**: Memory persistence, search, maps

To reconfigure MCP servers after initialization:
```bash
python scripts/detect_mcp_servers.py
```

See the [MCP Configuration Guide](mcp-configuration.md) for details.

## Next Steps

1. **Explore Examples**: Check out the `docs/examples/` directory for:
   - Basic API project
   - Web application
   - Microservice architecture

2. **Customize Your Setup**: See the [Customization Guide](customization.md) to:
   - Add new sub-agents
   - Create custom commands
   - Configure automation hooks

3. **Read the Usage Guide**: The [Complete Usage Guide](usage.md) covers:
   - Advanced workflows
   - Best practices
   - Integration options

## Getting Help

- **Documentation**: Check the `docs/` directory
- **Troubleshooting**: See the [Troubleshooting Guide](troubleshooting.md)
- **Issues**: Report problems at [GitHub Issues](https://github.com/dbankscard/claude-code-project-template/issues)
- **Community**: Join discussions at [GitHub Discussions](https://github.com/dbankscard/claude-code-project-template/discussions)

## Tips for Success

1. **Use Custom Commands**: They trigger specialized sub-agents for better results
2. **Let Auto-Approval Work**: Common commands execute instantly
3. **Trust the Hooks**: They maintain code quality automatically
4. **Review Sub-Agent Output**: Each agent provides detailed explanations
5. **Iterate Quickly**: The template encourages rapid development

Ready to revolutionize your development workflow? Start with a simple feature and watch the AI-powered system bring your ideas to life!