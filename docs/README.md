# Claude Code Project Template Documentation

## Quick Links

### Getting Started
- [Getting Started Guide](guides/getting-started.md) - Set up your first Claude Code project
- [Usage Guide](guides/usage.md) - Learn how to use sub-agents and commands
- [Customization Guide](guides/customization.md) - Customize the template for your needs
- [Troubleshooting](guides/troubleshooting.md) - Common issues and solutions

### AI Context Documentation
- [Project Structure](ai-context/project-structure.md) - Complete project organization
- [Development Patterns](ai-context/development-patterns.md) - Best practices and patterns
- [MCP Integration](ai-context/mcp-integration.md) - External tool integration

### Examples
- [Basic API](examples/basic-api/) - Simple REST API example
- [Microservice](examples/microservice/) - Microservice architecture example
- [Web App](examples/web-app/) - Full-stack web application example

## Documentation Structure

```
docs/
├── guides/                    # User-facing guides
│   ├── getting-started.md    # Initial setup and basics
│   ├── usage.md             # Using agents and commands
│   ├── customization.md     # Customizing the template
│   └── troubleshooting.md   # Common issues
├── ai-context/              # AI assistant documentation
│   ├── project-structure.md # Project organization
│   ├── development-patterns.md # Patterns and practices
│   └── mcp-integration.md   # MCP server integration
└── examples/                # Example implementations
    ├── basic-api/          # REST API example
    ├── microservice/       # Microservice example
    └── web-app/           # Web app example
```

## Contributing to Documentation

When adding new documentation:

1. **User Guides** go in `guides/` - focused on how-to and tutorials
2. **AI Context** goes in `ai-context/` - technical details for AI assistants
3. **Examples** go in `examples/` - complete working examples

### Documentation Standards

- Use clear, concise language
- Include code examples where helpful
- Add navigation links between related docs
- Keep AI context docs technical and comprehensive
- Keep user guides practical and task-focused

## Quick Start

```bash
# Clone the template
git clone https://github.com/dbankscard/claude-code-project-template.git
cd claude-code-project-template

# Initialize a new project
python scripts/initialize_project.py my-awesome-project

# Navigate to your project
cd ../my-awesome-project

# Start using Claude Code!
claude-code
```

## Need Help?

- Check the [Troubleshooting Guide](guides/troubleshooting.md)
- Review the [Usage Examples](guides/usage.md#examples)
- Consult the [AI Context Documentation](ai-context/) for technical details