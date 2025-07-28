# Claude Code Project Template

[![Test Template](https://github.com/dbankscard/claude-code-project-template/actions/workflows/test-template.yml/badge.svg)](https://github.com/dbankscard/claude-code-project-template/actions/workflows/test-template.yml)
[![Validate Agents](https://github.com/dbankscard/claude-code-project-template/actions/workflows/validate-agents.yml/badge.svg)](https://github.com/dbankscard/claude-code-project-template/actions/workflows/validate-agents.yml)

A comprehensive, production-ready template for Claude Code projects, meticulously designed based on Anthropic's knowledge base and best practices for AI-assisted development.

## Why This Template?

This template was specifically built to maximize Claude Code's capabilities by incorporating patterns and structures that align with how Claude understands and processes code. Every design decision is intentional:

### 🧠 **AI-First Architecture**
- **Structured Context**: The CLAUDE.md file and project structure provide immediate context that Claude can parse efficiently
- **Clear Hierarchies**: Directory structures mirror how Claude organizes information internally
- **Semantic Naming**: All files and commands use patterns that Claude recognizes instantly

### 🤖 **Multi-Agent System** 
- **Specialized Expertise**: 7 agents mirror Claude's own capability domains (architecture, security, testing, etc.)
- **Orchestrated Workflows**: Master orchestrator prevents context switching overhead
- **Clear Boundaries**: Each agent has well-defined triggers based on Anthropic's task categorization

### ⚡ **Smart Automation**
- **Confidence-Based Approval**: Auto-approval for commands Claude knows are safe (based on Anthropic's safety research)
- **Context-Aware Hooks**: Automation triggers align with Claude's decision-making patterns
- **Progressive Disclosure**: Complex tasks automatically invoke appropriate specialists

### 🔒 **Security & Best Practices**
- **Built-in Guardrails**: Security patterns from Anthropic's AI safety principles
- **Defensive Coding**: Every template follows secure-by-default practices
- **Audit Trails**: Comprehensive logging for AI-assisted development transparency

## Key Features

- 🤖 **7 Specialized Sub-Agents** with master orchestrator coordination
- ⚡ **Smart Auto-Approval** for 90%+ of development commands  
- 🎯 **Custom Slash Commands** organized by namespace (dev, project, git, security)
- 🔧 **4 Automated Hooks** for formatting, security, testing, and agent recommendations
- 🏗️ **Modern Python 3.12+** with type hints, async support, and comprehensive tooling
- 🔒 **Security-First** design with automated vulnerability scanning
- 🌐 **MCP Server Integration** for enhanced Claude capabilities
- 📝 **Cascading Context System** for flexible configuration inheritance

## Quick Start

```bash
# 1. Use this template
git clone https://github.com/dbankscard/claude-code-project-template.git my-project
cd my-project

# 2. Initialize your project (with interactive MCP setup)
python scripts/initialize_project.py my-awesome-app
cd my-awesome-app

# 3. Start Claude Code
claude

# 4. Try the master orchestrator
> Use the master-orchestrator to create a user authentication feature with OAuth2
```

## Features

### 🤖 Sub-Agent Ecosystem

- **Master Orchestrator**: Coordinates complex multi-agent workflows
- **Planning Architect**: Technical design and architecture planning
- **Code Reviewer**: Quality assurance and best practices enforcement
- **Test Engineer**: Comprehensive testing strategy and automation
- **Security Auditor**: Security compliance and vulnerability assessment
- **Documentation Specialist**: Technical documentation and API docs
- **Performance Optimizer**: Performance analysis and optimization

### ⚡ Smart Automation

- **Auto-Approval System**: Safe commands execute instantly based on patterns
- **Intelligent Hooks**:
  - `auto-format.sh`: Formats Python/JS/JSON/Markdown files on edit
  - `intelligent-automation.py`: Recommends relevant sub-agents based on changes
  - `security-check.py`: Validates for secrets and dangerous patterns
  - `test-automation.py`: Runs related tests after code changes
- **Context-Aware Triggering**: Automatic sub-agent recommendations

### 🎯 Custom Commands

- **Development**: 
  - `/dev:feature` - Create new features with full workflow
  - `/dev:review` - Comprehensive code review
  - `/dev:test` - Testing workflow with coverage
- **Project**: 
  - `/project:plan` - Architecture and planning
- **Git**: 
  - `/git:commit` - Smart conventional commits
- **Security**: 
  - `/security:audit` - Full security analysis

### 🌐 MCP Server Integration

- **Auto-Detection**: Automatically detects installed MCP servers during setup
- **Interactive Configuration**: Choose which servers to enable for your project
- **Built-in Servers**: Filesystem, Git, GitHub integration
- **Database Support**: PostgreSQL, SQLite, Redis connections
- **External Services**: Slack, Google Drive, AWS integrations
- **Gemini Consultation**: Deep code analysis and architecture discussions
- **Context7 Documentation**: Access to up-to-date library documentation
- **Agent-Specific Configs**: Each agent has tailored MCP server access

## Documentation

- [Getting Started Guide](docs/guides/getting-started.md)
- [Complete Usage Guide](docs/guides/usage.md)
- [MCP Configuration Guide](docs/guides/mcp-configuration.md)
- [Customization Instructions](docs/guides/customization.md)
- [Troubleshooting](docs/guides/troubleshooting.md)

### Examples

- [Basic API Project](docs/examples/basic-api/)
- [Web Application](docs/examples/web-app/)
- [Microservice Architecture](docs/examples/microservice/)

## Design Philosophy

### 1. **Context is King**
The `CLAUDE.md` file acts as a persistent context that Claude reads at the start of every session. This design:
- Eliminates repetitive explanations about project structure
- Provides consistent coding standards across sessions
- Enables Claude to make informed decisions immediately

### 2. **Specialized Over General**
Rather than one general-purpose agent, we use 7 specialized agents because:
- Claude performs better with focused, domain-specific tasks
- Parallel processing of different aspects (security, tests, docs)
- Reduced chance of context confusion or feature creep

### 3. **Progressive Enhancement**
The template starts simple but scales intelligently:
- Basic commands work immediately out of the box
- Complex workflows automatically invoke multiple agents
- Hooks add automation without overwhelming beginners

### 4. **Security by Design**
Every aspect incorporates security best practices:
- Automated security scanning on every change
- Command approval system prevents accidental damage
- Audit logging for compliance requirements

### 5. **Developer Experience First**
The template optimizes for both human and AI developers:
- Clear, semantic naming conventions
- Comprehensive documentation at multiple levels
- Intelligent defaults that can be overridden

## How It Works

1. **Initialization**: The template sets up a complete project structure with `.claude/` directory
2. **Context Loading**: Claude reads `CLAUDE.md` and automatically injects context to sub-agents
3. **Command Execution**: Custom commands or direct agent invocation trigger workflows
4. **Hook Automation**: Pre/post tool use hooks handle security, formatting, and testing
5. **Multi-Agent Orchestration**: Master orchestrator coordinates specialist agents:
   - Planning → Implementation → Review → Testing → Documentation → Optimization
6. **MCP Integration**: Enhanced capabilities through external server connections

## Requirements

- Python 3.12+
- Claude Code CLI
- Git
- (Optional) Docker for containerized development
- (Optional) MCP servers for enhanced features

## Project Structure

```
my-project/
├── .claude/
│   ├── agents/          # 7 specialized sub-agents
│   ├── commands/        # Custom slash commands
│   ├── hooks/           # Automation scripts
│   └── settings.json    # Claude configuration
├── src/                 # Source code
├── tests/               # Test suite
├── docs/                # Documentation
├── CLAUDE.md           # Main AI context file
├── .mcp.json           # MCP server configuration
└── pyproject.toml      # Python project config
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 📖 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/dbankscard/claude-code-project-template/issues)
- 💬 [Discussions](https://github.com/dbankscard/claude-code-project-template/discussions)

---

## Example Workflows

### Creating a New Feature
```bash
# Using master orchestrator (recommended for complex features)
> Use the master-orchestrator to create a user authentication system

# Or using slash command
> /dev:feature user-auth --description "JWT-based authentication"
```

### Running Security Audit
```bash
# Direct agent invocation
> Use the security-auditor to check for vulnerabilities

# Or slash command
> /security:audit --scope full --level paranoid
```

### Code Review
```bash
# After making changes
> Use the code-reviewer to review my recent changes

# The intelligent-automation hook will also suggest this automatically!
```

---

**Built with Claude in mind, for Claude to excel.** Transform your development workflow with AI-coordinated, automated, and consistently high-quality code development.
