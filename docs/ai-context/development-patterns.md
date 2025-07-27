# Development Patterns

## Overview
This document outlines the key development patterns and best practices used in this Claude Code project.

## Architectural Patterns

### Multi-Agent Architecture
- **Pattern**: Specialized agents for different domains
- **Implementation**: Each agent has specific expertise and activation triggers
- **Benefits**: Focused expertise, better code quality, parallel processing

### Command-Driven Development
- **Pattern**: Slash commands for common workflows
- **Implementation**: Organized by category (dev, project, git, security)
- **Benefits**: Consistent workflows, reduced errors, faster development

### Hook-Based Automation
- **Pattern**: Automated scripts triggered by events
- **Implementation**: Pre/post hooks for various operations
- **Benefits**: Automatic code quality, security scanning, smart assistance

## Code Patterns

### Error Handling
```python
from typing import Optional, Union

def safe_operation(data: str) -> Union[dict, None]:
    """Safely parse JSON data with proper error handling."""
    try:
        result = json.loads(data)
        logger.info(f"Successfully parsed data")
        return result
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
```

### State Management
```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AppState:
    """Centralized application state."""
    session_id: str
    user_data: Dict[str, Any]
    config: Dict[str, Any]
    
    def update(self, **kwargs) -> None:
        """Update state with validation."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid state key: {key}")
```

### Dependency Injection
```python
from typing import Protocol

class DatabaseProtocol(Protocol):
    """Database interface for dependency injection."""
    def query(self, sql: str) -> list:
        ...

class Service:
    def __init__(self, db: DatabaseProtocol):
        self.db = db
        
    def get_users(self) -> list:
        return self.db.query("SELECT * FROM users")
```

## Testing Patterns

### Test Organization
- Unit tests for individual functions
- Integration tests for workflows
- End-to-end tests for commands
- Property-based testing for complex logic

### Test Structure
```python
class TestFeature:
    def setup_method(self):
        """Set up test fixtures."""
        self.test_data = create_test_data()
        
    def teardown_method(self):
        """Clean up after tests."""
        cleanup_test_data()
        
    def test_happy_path(self):
        """Test normal operation."""
        result = function_under_test(self.test_data)
        assert result.status == "success"
        
    def test_error_handling(self):
        """Test error conditions."""
        with pytest.raises(ValueError):
            function_under_test(invalid_data)
```

## Security Patterns

### Input Validation
```python
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    username: str
    email: str
    
    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
        
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v
```

### Secure Configuration
```python
import os
from typing import Optional

class SecureConfig:
    @staticmethod
    def get_secret(key: str) -> Optional[str]:
        """Get secret from environment, never from code."""
        value = os.getenv(key)
        if not value:
            logger.warning(f"Secret {key} not found in environment")
        return value
```

## Performance Patterns

### Lazy Loading
```python
from functools import lru_cache

class DataLoader:
    @property
    @lru_cache(maxsize=1)
    def large_dataset(self):
        """Load large dataset only when accessed."""
        return self._load_dataset()
```

### Async Operations
```python
import asyncio
from typing import List

async def process_batch(items: List[str]) -> List[dict]:
    """Process items concurrently."""
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)
```

## Documentation Patterns

### Self-Documenting Code
- Clear variable names
- Type hints everywhere
- Docstrings for all public functions
- Comments for complex logic only

### API Documentation
```python
from typing import Dict, Any

async def api_endpoint(
    user_id: str,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Retrieve user data with optional filters.
    
    Args:
        user_id: Unique user identifier
        filters: Optional query filters
        
    Returns:
        User data matching the filters
        
    Raises:
        ValueError: If user_id is invalid
        PermissionError: If access is denied
    """
    pass
```