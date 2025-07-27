# MCP (Model Context Protocol) Integration Guide

## Overview
This document describes how to integrate and use MCP servers with the Claude Code project template.

## What is MCP?
Model Context Protocol (MCP) is a protocol for connecting AI assistants to external tools and data sources. It enables Claude to interact with databases, APIs, file systems, and other services through a standardized interface.

## Available MCP Servers

### 1. Gemini Consultation Server
**Purpose**: Get expert second opinions on complex coding problems

**Key Features**:
- Deep code analysis and architecture review
- Performance optimization suggestions
- Security vulnerability detection
- Multi-file context understanding

**Usage**:
```python
# Consult on architecture decisions
mcp__gemini__consult_gemini(
    specific_question="Should I use dependency injection here?",
    problem_description="Need to make database configurable",
    code_context="Current implementation uses hard-coded connection",
    attached_files=["src/database.py", "src/config.py"]
)
```

### 2. Context7 Documentation Server
**Purpose**: Access up-to-date documentation for external libraries

**Key Features**:
- Current documentation beyond training cutoff
- Topic-focused retrieval
- Version-specific documentation
- Integration examples

**Usage**:
```python
# Get React hooks documentation
mcp__context7__resolve_library_id(libraryName="react")
mcp__context7__get_library_docs(
    context7CompatibleLibraryID="/facebook/react",
    topic="hooks",
    tokens=8000
)
```

## Setting Up MCP Servers

### Installation
1. Install the MCP server package:
```bash
npm install -g @anthropic/mcp
```

2. Configure servers in `.mcp.json`:
```json
{
  "servers": {
    "gemini": {
      "command": "npx",
      "args": ["@upstash/mcp-server-gemini"],
      "env": {
        "GOOGLE_GENERATIVE_AI_API_KEY": "${GEMINI_API_KEY}"
      }
    },
    "context7": {
      "command": "npx", 
      "args": ["@context7/mcp-server"]
    }
  }
}
```

3. Set environment variables:
```bash
export GEMINI_API_KEY="your-api-key"
```

## Custom MCP Server Development

### Basic Server Structure
```python
from mcp import Server, Tool, Resource

class CustomMCPServer(Server):
    def __init__(self):
        super().__init__("custom-server")
        
    @Tool("analyze_code")
    async def analyze_code(self, file_path: str) -> dict:
        """Analyze code and return insights."""
        # Implementation
        return {"insights": [...]}
        
    @Resource("config")
    async def get_config(self) -> dict:
        """Provide configuration data."""
        return {"settings": {...}}
```

### Integration with Claude Code

1. Add server to `.mcp.json`
2. Create wrapper commands in `.claude/commands/`
3. Add intelligent triggers in hooks

Example command wrapper:
```markdown
# /dev:analyze

## Usage
/dev:analyze <file-path>

## Description
Analyzes code using custom MCP server for insights.

## Process
1. Invoke mcp__custom__analyze_code
2. Process insights
3. Generate recommendations
4. Apply improvements
```

## Best Practices

### 1. Context Management
- Include relevant files when consulting external services
- Use session IDs for multi-turn conversations
- Cache responses when appropriate

### 2. Security
- Never send sensitive data to external services
- Validate all responses before applying changes
- Use environment variables for API keys

### 3. Performance
- Batch requests when possible
- Use appropriate token limits
- Cache documentation lookups

### 4. Error Handling
```python
try:
    result = await mcp__service__operation(params)
except MCPError as e:
    logger.error(f"MCP operation failed: {e}")
    # Fallback to local processing
    result = local_fallback(params)
```

## Common Use Cases

### 1. Architecture Review
Before implementing major features, consult Gemini:
```python
# Get architecture feedback
response = mcp__gemini__consult_gemini(
    specific_question="Best pattern for this feature?",
    problem_description="Need real-time updates across clients",
    preferred_approach="review"
)
```

### 2. Library Integration
When using new libraries, fetch current docs:
```python
# Get FastAPI documentation
mcp__context7__get_library_docs(
    context7CompatibleLibraryID="/tiangolo/fastapi",
    topic="dependency-injection"
)
```

### 3. Code Quality Checks
Automated quality analysis in hooks:
```python
# In intelligent-automation.py
if "complex_function" in changes:
    mcp__gemini__consult_gemini(
        specific_question="Simplification suggestions?",
        code_context=function_code,
        preferred_approach="optimize"
    )
```

## Troubleshooting

### Common Issues
1. **Connection timeout**: Check network and API keys
2. **Rate limits**: Implement backoff and caching
3. **Context too large**: Split into smaller chunks
4. **Inconsistent responses**: Use specific questions

### Debug Mode
Enable MCP debugging in settings:
```json
{
  "mcp": {
    "debug": true,
    "log_level": "verbose"
  }
}
```