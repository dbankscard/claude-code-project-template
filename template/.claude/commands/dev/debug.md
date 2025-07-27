# /dev:debug

Intelligent debugging assistance for identifying and fixing issues.

## Usage
`/dev:debug <issue-description>`

## Description
Provides comprehensive debugging support by analyzing error messages, tracing execution flow, identifying root causes, and implementing fixes.

## Debugging Process

### 1. Issue Analysis
- Parse error messages
- Identify affected components
- Trace execution path
- Collect relevant logs

### 2. Root Cause Investigation
- Analyze stack traces
- Check recent changes
- Review dependencies
- Examine data flow

### 3. Solution Development
- Identify fix options
- Implement solution
- Add error handling
- Prevent recurrence

### 4. Verification
- Test the fix
- Verify side effects
- Update tests
- Document solution

## Examples

### Debug Error Message
```
/dev:debug "TypeError: Cannot read property 'id' of undefined at UserService.getProfile"
```

### Debug API Issue
```
/dev:debug "API returns 500 error when creating orders with multiple items"
```

### Debug Performance Issue
```
/dev:debug "Application freezes when loading user dashboard with >1000 records"
```

### Debug Test Failure
```
/dev:debug "Integration tests failing after database migration"
```

## Debugging Strategies

### 1. Error Analysis
```python
# Enhanced error logging
try:
    result = process_order(order_data)
except Exception as e:
    logger.error(
        "Order processing failed",
        extra={
            "order_id": order_data.get("id"),
            "error_type": type(e).__name__,
            "error_message": str(e),
            "stack_trace": traceback.format_exc(),
            "order_data": order_data
        }
    )
    raise
```

### 2. Execution Tracing
```python
# Debug decorator
def debug_trace(func):
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering {func.__name__}")
        logger.debug(f"Args: {args}, Kwargs: {kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Exiting {func.__name__} with result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    
    return wrapper
```

### 3. State Inspection
```python
# Debug checkpoint
def debug_checkpoint(label, **variables):
    """Log current state at checkpoint"""
    logger.debug(f"=== Checkpoint: {label} ===")
    for name, value in variables.items():
        logger.debug(f"{name}: {value}")
        logger.debug(f"{name} type: {type(value)}")
```

## Common Issues and Solutions

### 1. Null/Undefined Errors
**Symptoms**: `TypeError`, `AttributeError`
**Investigation**:
- Check data source
- Validate inputs
- Add null checks
- Review data flow

**Fix Pattern**:
```python
# Before
user_name = user.profile.name

# After
user_name = user.profile.name if user and user.profile else "Unknown"
```

### 2. Race Conditions
**Symptoms**: Intermittent failures, inconsistent state
**Investigation**:
- Check concurrent operations
- Review async code
- Analyze timing
- Add logging

**Fix Pattern**:
```python
# Add proper locking
import threading

lock = threading.Lock()

def update_shared_resource(data):
    with lock:
        # Critical section
        shared_resource.update(data)
```

### 3. Memory Leaks
**Symptoms**: Increasing memory usage, OOM errors
**Investigation**:
- Profile memory usage
- Check object references
- Review caches
- Analyze loops

**Fix Pattern**:
```python
# Clear references
def process_large_dataset(data):
    results = []
    for chunk in data:
        result = process_chunk(chunk)
        results.append(result)
        # Clear chunk reference
        del chunk
    return results
```

## Debug Output Format

```markdown
# Debug Report: [Issue Description]

## Issue Summary
- **Error Type**: TypeError
- **Location**: UserService.getProfile (line 145)
- **Frequency**: Consistent
- **Impact**: User profile page crashes

## Root Cause
The error occurs when a user without a profile attempts to access their profile page. The code assumes all users have profiles, but this is not enforced.

## Execution Trace
1. UserController.showProfile() called
2. UserService.getProfile(userId=123) called
3. Database returns User object without profile relation
4. Attempting to access user.profile.settings fails

## Solution Implemented
Added null checking and default profile creation:
```python
def get_profile(self, user_id):
    user = self.user_repo.get(user_id)
    if not user:
        raise UserNotFoundError(f"User {user_id} not found")
    
    if not user.profile:
        # Create default profile
        user.profile = self.create_default_profile(user)
        self.user_repo.save(user)
    
    return user.profile
```

## Verification
- ✅ Error no longer occurs
- ✅ Added unit test for edge case
- ✅ Updated integration tests
- ✅ No performance impact

## Prevention
- Added database constraint
- Updated user creation to include profile
- Added monitoring alert
```

## Options

- `--verbose`: Detailed execution trace
- `--profile`: Include performance profiling
- `--compare`: Compare with working version
- `--interactive`: Step-through debugging

## Debug Tools Integration

### Logging Enhancement
```python
# Configure detailed logging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

### Remote Debugging
```python
# Enable remote debugging
import pdb
import sys

def enable_remote_debug():
    import pydevd_pycharm
    pydevd_pycharm.settrace(
        'localhost', 
        port=5678, 
        stdoutToServer=True, 
        stderrToServer=True
    )
```

## Related Commands

- `/dev:test` - Add tests for bug fixes
- `/dev:review` - Review debugging changes
- `/project:status` - Check system health
- `/dev:refactor` - Refactor problematic code