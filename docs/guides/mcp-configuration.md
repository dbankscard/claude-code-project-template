# MCP Server Configuration Guide

The Model Context Protocol (MCP) extends Claude's capabilities by connecting to external tools and data sources. This guide explains how to configure MCP servers for your project.

## Overview

MCP servers can provide Claude with access to:
- File systems
- Databases (PostgreSQL, SQLite, Redis)
- Version control (Git, GitHub)
- External services (Slack, Google Drive, AWS)
- Custom tools and APIs

## Automatic Configuration

When you initialize a new project, the template automatically:

1. **Detects installed MCP servers** on your system
2. **Prompts you to select** which servers to enable
3. **Generates `.mcp.json`** with proper configuration
4. **Creates `.env.example`** for required environment variables

```bash
python scripts/initialize_project.py my-project

# During setup:
🔍 Detecting installed MCP servers...
✅ filesystem: Installed globally
📦 git: Available via npx
📦 github: Available via npx
❌ postgres: Not found

📋 Available MCP servers:
1. ✅ filesystem: File system access with extension filtering
2. 📦 git: Git repository operations
3. 📦 github: GitHub API integration

Which servers would you like to enable?
Enter numbers separated by commas (e.g., 1,3,5) or 'all' for all servers:
> 1,2,3
```

## Manual Configuration

### Reconfigure MCP Servers

To reconfigure MCP servers after project creation:

```bash
cd your-project
python scripts/detect_mcp_servers.py
```

### Edit `.mcp.json` Directly

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "settings": {
        "extensions": [".py", ".js", ".ts", ".json", ".yaml", ".md"],
        "ignore": ["node_modules", "__pycache__", ".git", "venv"]
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## Common MCP Servers

### Core Servers

#### Filesystem
Provides file system access with filtering:
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
    "settings": {
      "extensions": [".py", ".js", ".ts", ".json", ".yaml", ".md"],
      "ignore": ["node_modules", "__pycache__", ".git", "venv"]
    }
  }
}
```

#### Git
Git repository operations:
```json
{
  "git": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-git", "."]
  }
}
```

#### GitHub
GitHub API integration:
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_TOKEN": "${GITHUB_TOKEN}"
    }
  }
}
```

### Database Servers

#### PostgreSQL
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "DATABASE_URL": "${DATABASE_URL}"
    }
  }
}
```

#### SQLite (Python)
```json
{
  "sqlite": {
    "command": "uv",
    "args": ["run", "mcp-server-sqlite", "--db-path", "./data.db"]
  }
}
```

### External Services

#### Slack
```json
{
  "slack": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-slack"],
    "env": {
      "SLACK_TOKEN": "${SLACK_TOKEN}"
    }
  }
}
```

#### Google Drive
```json
{
  "google-drive": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-google-drive"],
    "env": {
      "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
      "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
    }
  }
}
```

## Environment Variables

### Setting Up `.env`

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in your credentials:
   ```bash
   # .env
   GITHUB_TOKEN=ghp_your_github_personal_access_token
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   SLACK_TOKEN=xoxb-your-slack-bot-token
   ```

3. **Never commit `.env` to version control!**

### Getting Tokens

- **GitHub**: Create at https://github.com/settings/tokens
- **Slack**: Create app at https://api.slack.com/apps
- **Google**: Set up OAuth at https://console.cloud.google.com

## Agent-Specific Configuration

Different agents have access to different servers:

```json
{
  "agentConfigs": {
    "master-orchestrator": {
      "servers": ["filesystem", "git", "github", "postgres"]
    },
    "code-reviewer": {
      "servers": ["filesystem", "git"]
    },
    "security-auditor": {
      "servers": ["filesystem"]
    }
  }
}
```

## Installing MCP Servers

### NPM-based Servers

Install globally:
```bash
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-git
npm install -g @modelcontextprotocol/server-github
```

Or use `npx` (recommended) - no installation needed!

### Python-based Servers

Install with pip:
```bash
pip install mcp-server-sqlite
pip install mcp-server-aws
```

Or use `uv` for better dependency management.

## Troubleshooting

### Server Not Detected

1. Check if installed:
   ```bash
   npm list -g @modelcontextprotocol/server-name
   ```

2. Test with npx:
   ```bash
   npx -y @modelcontextprotocol/server-name --help
   ```

### Connection Issues

1. Check logs:
   ```bash
   # macOS/Linux
   tail -f ~/Library/Logs/Claude/mcp*.log
   
   # Windows
   Get-Content "$env:APPDATA\Claude\Logs\mcp*.log" -Tail 20 -Wait
   ```

2. Verify environment variables:
   ```bash
   echo $GITHUB_TOKEN
   ```

3. Test server directly:
   ```bash
   npx @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem .
   ```

### Permission Errors

Ensure Claude has access to:
- Project directory
- Node.js/npm executables
- Environment variables

## Best Practices

1. **Start Simple**: Begin with filesystem and git servers
2. **Add Gradually**: Enable additional servers as needed
3. **Secure Credentials**: Use environment variables, never hardcode
4. **Test First**: Verify servers work before relying on them
5. **Document Requirements**: Note which servers your project needs

## Security Considerations

1. **Limit Access**: Only enable servers you need
2. **Scope Permissions**: Use minimal required permissions for tokens
3. **Review Settings**: Check file extensions and ignore patterns
4. **Audit Regularly**: Review which servers have access to what
5. **Rotate Credentials**: Update tokens and passwords periodically

## Next Steps

- Review available servers at [MCP Server Directory](https://mcp-server.directory)
- Create custom servers for your specific needs
- Configure agent-specific server access
- Set up remote MCP servers for team collaboration

For more information, see the [official MCP documentation](https://modelcontextprotocol.io).