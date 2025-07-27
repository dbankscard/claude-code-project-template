# Getting Started with {{PROJECT_NAME}}

Welcome to {{PROJECT_NAME}}! This guide will help you get up and running quickly.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/{{project_name}}.git
   cd {{project_name}}
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Basic Usage

```python
import {{project_name}}

# Your code here
```

## Development

Run tests:
```bash
pytest
```

Format code:
```bash
black src tests
isort src tests
```

Type checking:
```bash
mypy src
```

## Next Steps

- Check out the [API documentation](../api/)
- See [examples](../examples/) for more usage patterns
- Read about [contributing](../../CONTRIBUTING.md)