# /dev:test

Creates comprehensive test suites with unit, integration, and end-to-end tests.

## Usage
`/dev:test [component-or-file]`

## Description
Triggers the Test Engineer agent to create or update tests, ensuring high code coverage and reliability through various testing strategies.

## Test Types

### 1. Unit Tests
- Individual function/method testing
- Mock external dependencies
- Edge case coverage
- Error scenario validation

### 2. Integration Tests
- Component interaction testing
- API endpoint validation
- Database operation verification
- External service integration

### 3. End-to-End Tests
- User workflow validation
- Cross-system functionality
- Performance benchmarks
- Load testing scenarios

## Examples

### Test Entire Module
```
/dev:test src/services/
```

### Test Specific Component
```
/dev:test UserAuthenticationService
```

### Test New Feature
```
/dev:test "user registration flow"
```

### Update Existing Tests
```
/dev:test --update src/api/users.py
```

## Test Generation Strategy

### 1. Analysis Phase
- Identify testable components
- Map dependencies
- Determine test boundaries
- Plan test scenarios

### 2. Test Creation
- Generate test structure
- Implement test cases
- Add fixtures and mocks
- Create test data

### 3. Coverage Validation
- Measure code coverage
- Identify gaps
- Add missing tests
- Verify edge cases

## Output Examples

### Unit Test
```python
class TestUserService:
    def test_create_user_success(self, mock_db):
        """Test successful user creation"""
        service = UserService(mock_db)
        user_data = {"email": "test@example.com", "name": "Test User"}
        
        result = service.create_user(user_data)
        
        assert result.id is not None
        assert result.email == user_data["email"]
        mock_db.save.assert_called_once()
    
    def test_create_user_duplicate_email(self, mock_db):
        """Test duplicate email handling"""
        mock_db.find_by_email.return_value = {"id": 1}
        service = UserService(mock_db)
        
        with pytest.raises(DuplicateEmailError):
            service.create_user({"email": "existing@example.com"})
```

### Integration Test
```python
class TestUserAPI:
    def test_create_user_endpoint(self, client, auth_token):
        """Test POST /users endpoint"""
        response = client.post(
            "/users",
            json={"email": "new@example.com", "name": "New User"},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code == 201
        assert response.json()["email"] == "new@example.com"
```

## Options

- `--type`: Specific test type (unit/integration/e2e)
- `--update`: Update existing tests
- `--coverage`: Include coverage report
- `--performance`: Add performance tests
- `--framework`: Test framework preference

## Coverage Goals

- **Minimum Coverage**: 80%
- **Critical Paths**: 95%
- **New Code**: 90%
- **API Endpoints**: 100%

## Test Best Practices

### 1. Test Structure
- Arrange-Act-Assert pattern
- Descriptive test names
- Isolated test cases
- Proper cleanup

### 2. Mock Strategy
- Mock external services
- Use real objects when possible
- Verify mock interactions
- Avoid over-mocking

### 3. Test Data
- Use factories for test data
- Randomize when appropriate
- Clean up after tests
- Separate test databases

### 4. Performance
- Fast test execution
- Parallel test runs
- Efficient fixtures
- Minimal I/O operations

## Testing Checklist

- [ ] Happy path scenarios
- [ ] Error conditions
- [ ] Edge cases
- [ ] Boundary values
- [ ] Null/empty inputs
- [ ] Concurrent operations
- [ ] Performance limits
- [ ] Security scenarios

## Integration

### CI/CD Pipeline
```yaml
test:
  script:
    - pytest tests/ --cov=src --cov-report=html
    - coverage report --fail-under=80
```

### Pre-push Hook
```bash
#!/bin/bash
claude code "/dev:test --type=unit"
```

## Related Commands

- `/dev:feature` - Implement features with tests
- `/dev:debug` - Debug failing tests
- `/dev:review` - Review test quality
- `/project:status` - Check test coverage