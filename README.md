# Claude Code Project Template

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
- 🎯 **17 Custom Commands** across development, project, git, and security workflows
- 🔧 **Automated Hooks** for quality enforcement and sub-agent triggering
- 🏗️ **Modern Python** project structure with comprehensive tooling
- 🔒 **Security-First** design with built-in compliance checking

## Quick Start

```bash
# 1. Use this template
git clone https://github.com/dbankscard/claude-code-project-template.git my-project
cd my-project

# 2. Initialize your project
python scripts/initialize_project.py my-awesome-app
cd my-awesome-app

# 3. Start Claude Code
claude

# 4. Try your first command
> /dev:feature user authentication with OAuth2
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

- **Auto-Approval System**: Safe commands (ls, git, grep) execute instantly
- **Intelligent Hooks**: Automatic code formatting, quality checks, security scans
- **Context-Aware Triggering**: Right sub-agent for the right task automatically

### 🎯 Custom Commands

- **Development**: `/dev:feature`, `/dev:review`, `/dev:test`, `/dev:debug`, `/dev:refactor`
- **Project**: `/project:plan`, `/project:deploy`, `/project:docs`, `/project:status`
- **Git**: `/git:commit`, `/git:pr`, `/git:release`, `/git:hotfix`
- **Security**: `/security:audit`, `/security:scan`, `/security:compliance`

## Documentation

- [Getting Started Guide](docs/guides/getting-started.md)
- [Complete Usage Guide](docs/guides/usage.md)
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

1. **Initialization**: The template sets up a complete project structure with all necessary configurations
2. **Context Loading**: Claude reads `CLAUDE.md` to understand your project's specific requirements
3. **Command Execution**: Custom commands trigger appropriate workflows and agents
4. **Automation**: Hooks handle repetitive tasks like formatting and security checks
5. **Multi-Agent Coordination**: Complex tasks are automatically broken down and distributed

## Requirements

- Python 3.12+
- Claude Code CLI
- Git
- (Optional) Docker for containerized development

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 📖 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/dbankscard/claude-code-project-template/issues)
- 💬 [Discussions](https://github.com/dbankscard/claude-code-project-template/discussions)

---

Transform your development workflow with AI-coordinated, automated, and consistently high-quality code development.
