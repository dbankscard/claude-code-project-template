# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

## Features

- Built with Claude Code AI assistance
- Automated testing and code quality checks
- Security-first development approach
- Comprehensive documentation

## Quick Start

### Prerequisites

- Python 3.12 or higher
- Git
- Claude Code CLI

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/{{project_name}}.git
cd {{project_name}}
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest
```

## Development with Claude Code

This project is optimized for development with Claude Code. Start Claude in the project directory:

```bash
claude
```

### Useful Commands

- `/dev:feature <description>` - Implement a new feature
- `/dev:test` - Create or update tests  
- `/dev:review` - Review code quality
- `/security:audit` - Run security audit
- `/git:commit` - Create semantic commit

## Project Structure

```
{{project_name}}/
├── src/
│   └── {{project_name}}/    # Main package
├── tests/                    # Test suite
├── docs/                     # Documentation
├── .claude/                  # Claude Code configuration
│   ├── agents/              # AI sub-agents
│   ├── commands/            # Custom commands
│   └── hooks/              # Automation hooks
└── CLAUDE.md               # AI context file
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Claude Code Project Template](https://github.com/dbankscard/claude-code-project-template)