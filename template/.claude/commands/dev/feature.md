# /dev:feature

Implements a complete feature with planning, coding, testing, and documentation.

## Usage
`/dev:feature <feature-description>`

## Description
This command orchestrates the complete feature development lifecycle by coordinating multiple specialized agents to deliver production-ready code.

## Process

1. **Planning Phase** (Planning Architect)
   - Analyzes requirements
   - Creates technical design
   - Defines API contracts
   - Plans implementation phases

2. **Implementation Phase**
   - Writes feature code
   - Follows project conventions
   - Implements error handling
   - Adds logging and monitoring

3. **Testing Phase** (Test Engineer)
   - Creates unit tests
   - Writes integration tests
   - Ensures edge case coverage
   - Validates performance

4. **Security Review** (Security Auditor)
   - Scans for vulnerabilities
   - Validates input handling
   - Checks authentication/authorization
   - Reviews data protection

5. **Documentation Phase** (Documentation Specialist)
   - Updates API documentation
   - Creates user guides
   - Documents configuration
   - Adds code examples

6. **Final Review** (Code Reviewer)
   - Validates code quality
   - Ensures best practices
   - Checks performance
   - Verifies completeness

## Examples

### Basic Feature
```
/dev:feature Add user profile management with avatar upload
```

### Complex Feature
```
/dev:feature Implement real-time notifications with WebSocket support, message queuing, and mobile push notifications
```

### API Feature
```
/dev:feature Create RESTful API for inventory management with CRUD operations, pagination, and filtering
```

## Options

- `--skip-tests`: Skip test generation (not recommended)
- `--skip-docs`: Skip documentation updates
- `--priority`: Set implementation priority (high/medium/low)
- `--framework`: Specify framework preferences

## Success Criteria

- ✅ All tests passing
- ✅ Security scan clean
- ✅ Documentation updated
- ✅ Code review approved
- ✅ Performance benchmarks met

## Best Practices

1. **Clear Requirements**: Provide detailed feature descriptions
2. **Scope Management**: Break large features into smaller ones
3. **Iterative Development**: Use feedback loops
4. **Quality Gates**: Don't skip automated checks

## Related Commands

- `/dev:test` - Add additional tests
- `/dev:review` - Trigger manual review
- `/project:docs` - Generate comprehensive docs
- `/security:audit` - Deep security analysis