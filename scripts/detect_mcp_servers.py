#!/usr/bin/env python3
"""
MCP Server Detection and Configuration Script

This script detects installed MCP servers and helps configure them for a project.
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Common MCP servers and their configurations
KNOWN_MCP_SERVERS = {
    # Core MCP servers
    "@modelcontextprotocol/server-filesystem": {
        "name": "filesystem",
        "description": "File system access with extension filtering",
        "config_template": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
            "settings": {
                "extensions": [".py", ".js", ".ts", ".json", ".yaml", ".md"],
                "ignore": ["node_modules", "__pycache__", ".git", "venv"]
            }
        }
    },
    "@modelcontextprotocol/server-git": {
        "name": "git",
        "description": "Git repository operations",
        "config_template": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-git", "."]
        }
    },
    "@modelcontextprotocol/server-github": {
        "name": "github",
        "description": "GitHub API integration",
        "config_template": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {
                "GITHUB_TOKEN": "${GITHUB_TOKEN}"
            }
        },
        "requires_env": ["GITHUB_TOKEN"]
    },
    "@modelcontextprotocol/server-memory": {
        "name": "memory",
        "description": "In-memory key-value storage",
        "config_template": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-memory"]
        }
    },
    "@modelcontextprotocol/server-postgres": {
        "name": "postgres",
        "description": "PostgreSQL database access",
        "config_template": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres"],
            "env": {
                "DATABASE_URL": "${DATABASE_URL}"
            }
        },
        "requires_env": ["DATABASE_URL"]
    },
    "@modelcontextprotocol/server-slack": {
        "name": "slack",
        "description": "Slack workspace integration",
        "config_template": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-slack"],
            "env": {
                "SLACK_TOKEN": "${SLACK_TOKEN}"
            }
        },
        "requires_env": ["SLACK_TOKEN"]
    },
    "@modelcontextprotocol/server-google-drive": {
        "name": "google-drive",
        "description": "Google Drive integration",
        "config_template": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-google-drive"],
            "env": {
                "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
                "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
            }
        },
        "requires_env": ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"]
    },
    # Python-based MCP servers
    "mcp-server-sqlite": {
        "name": "sqlite",
        "description": "SQLite database access",
        "language": "python",
        "config_template": {
            "command": "uv",
            "args": ["run", "mcp-server-sqlite", "--db-path", "./data.db"]
        }
    }
}

# Additional community MCP servers to check
COMMUNITY_SERVERS = {
    "mcp-server-aws": "AWS services integration",
    "mcp-server-docker": "Docker container management",
    "mcp-server-kubernetes": "Kubernetes cluster operations",
    "mcp-server-redis": "Redis database access",
    "mcp-server-elasticsearch": "Elasticsearch integration",
    "mcp-server-jira": "Jira issue tracking",
    "mcp-server-confluence": "Confluence documentation",
    "mcp-server-datadog": "Datadog monitoring",
    "mcp-server-sentry": "Sentry error tracking"
}


def check_command_exists(command: str) -> bool:
    """Check if a command exists in the system PATH."""
    try:
        subprocess.run(
            [command, "--version"],
            capture_output=True,
            check=False
        )
        return True
    except FileNotFoundError:
        return False


def detect_npm_package(package_name: str) -> bool:
    """Check if an npm package is installed globally."""
    try:
        result = subprocess.run(
            ["npm", "list", "-g", "--depth=0", package_name],
            capture_output=True,
            text=True,
            check=False
        )
        return package_name in result.stdout
    except FileNotFoundError:
        return False


def detect_python_package(package_name: str) -> bool:
    """Check if a Python package is installed."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            check=False
        )
        return result.returncode == 0
    except:
        return False


def check_npx_availability(package_name: str) -> bool:
    """Check if a package is available via npx."""
    try:
        result = subprocess.run(
            ["npx", "-y", "--loglevel", "error", package_name, "--help"],
            capture_output=True,
            timeout=10,
            check=False
        )
        return result.returncode == 0
    except:
        return False


def detect_installed_servers() -> Dict[str, Dict]:
    """Detect which MCP servers are installed or available."""
    print("🔍 Detecting installed MCP servers...")
    
    installed_servers = {}
    
    # Check for npm/npx
    has_npm = check_command_exists("npm")
    has_npx = check_command_exists("npx")
    
    if not has_npx:
        print("⚠️  npx not found. Install Node.js to use npm-based MCP servers.")
    
    # Check known MCP servers
    for package, info in KNOWN_MCP_SERVERS.items():
        language = info.get("language", "node")
        
        if language == "node" and has_npx:
            # For npm packages, check if globally installed or available via npx
            if detect_npm_package(package):
                installed_servers[package] = {**info, "status": "installed"}
                print(f"✅ {info['name']}: Installed globally")
            elif check_npx_availability(package):
                installed_servers[package] = {**info, "status": "available"}
                print(f"📦 {info['name']}: Available via npx")
            else:
                print(f"❌ {info['name']}: Not found")
        
        elif language == "python":
            # For Python packages
            if detect_python_package(package):
                installed_servers[package] = {**info, "status": "installed"}
                print(f"✅ {info['name']}: Installed (Python)")
            else:
                print(f"❌ {info['name']}: Not found (Python)")
    
    return installed_servers


def check_environment_variables(requires_env: List[str]) -> Tuple[bool, List[str]]:
    """Check if required environment variables are set."""
    missing = []
    for env_var in requires_env:
        if not os.environ.get(env_var):
            missing.append(env_var)
    return len(missing) == 0, missing


def prompt_user_selection(available_servers: Dict[str, Dict]) -> List[str]:
    """Prompt user to select which servers to enable."""
    print("\n📋 Available MCP servers:")
    server_list = list(available_servers.items())
    
    for i, (package, info) in enumerate(server_list):
        status = "✅" if info.get("status") == "installed" else "📦"
        print(f"{i+1}. {status} {info['name']}: {info['description']}")
    
    print("\nWhich servers would you like to enable?")
    print("Enter numbers separated by commas (e.g., 1,3,5) or 'all' for all servers:")
    
    selection = input("> ").strip()
    
    if selection.lower() == "all":
        return [package for package, _ in server_list]
    
    try:
        indices = [int(x.strip()) - 1 for x in selection.split(",")]
        selected = []
        for i in indices:
            if 0 <= i < len(server_list):
                selected.append(server_list[i][0])
        return selected
    except:
        print("Invalid selection. Using default servers (filesystem, git).")
        return ["@modelcontextprotocol/server-filesystem", "@modelcontextprotocol/server-git"]


def generate_mcp_config(selected_servers: List[str], available_servers: Dict[str, Dict]) -> Dict:
    """Generate MCP configuration for selected servers."""
    config = {"servers": {}}
    
    for package in selected_servers:
        if package in available_servers:
            server_info = available_servers[package]
            server_name = server_info["name"]
            
            # Check environment variables if required
            if "requires_env" in server_info:
                has_env, missing = check_environment_variables(server_info["requires_env"])
                if not has_env:
                    print(f"\n⚠️  {server_name} requires environment variables: {', '.join(missing)}")
                    print("Add these to your .env file or skip this server.")
                    skip = input("Skip this server? (y/n): ").lower() == "y"
                    if skip:
                        continue
            
            config["servers"][server_name] = server_info["config_template"].copy()
    
    # Add agent-specific configurations if certain servers are selected
    if any(s in selected_servers for s in ["@modelcontextprotocol/server-filesystem", "@modelcontextprotocol/server-git"]):
        config["agentConfigs"] = generate_agent_configs(config["servers"])
    
    config["globalSettings"] = {
        "timeout": 30000,
        "retries": 3,
        "concurrentRequests": 5
    }
    
    return config


def generate_agent_configs(servers: Dict) -> Dict:
    """Generate agent-specific server configurations."""
    return {
        "planning-architect": {
            "servers": ["filesystem", "git", "github"] if "github" in servers else ["filesystem", "git"]
        },
        "code-reviewer": {
            "servers": ["filesystem", "git"]
        },
        "test-engineer": {
            "servers": ["filesystem", "git"]
        },
        "security-auditor": {
            "servers": ["filesystem"]
        },
        "documentation-specialist": {
            "servers": ["filesystem", "git"]
        },
        "performance-optimizer": {
            "servers": ["filesystem"]
        },
        "master-orchestrator": {
            "servers": list(servers.keys())  # Give orchestrator access to all servers
        }
    }


def save_mcp_config(config: Dict, project_path: Path) -> None:
    """Save MCP configuration to .mcp.json."""
    mcp_file = project_path / ".mcp.json"
    
    with open(mcp_file, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ MCP configuration saved to {mcp_file}")


def create_env_template(config: Dict, project_path: Path) -> None:
    """Create .env.example file with required environment variables."""
    env_vars = set()
    
    # Extract all environment variables from config
    for server_config in config.get("servers", {}).values():
        if "env" in server_config:
            for var in server_config["env"].keys():
                if var.startswith("${") and var.endswith("}"):
                    env_vars.add(var[2:-1])
    
    if env_vars:
        env_example = project_path / ".env.example"
        with open(env_example, "w") as f:
            f.write("# MCP Server Environment Variables\n")
            f.write("# Copy this file to .env and fill in your values\n\n")
            for var in sorted(env_vars):
                f.write(f"{var}=your_{var.lower()}_here\n")
        
        print(f"📝 Created {env_example} with required environment variables")


def interactive_mcp_setup(project_path: Path) -> Optional[Dict]:
    """Run interactive MCP server setup."""
    print("\n🚀 MCP Server Configuration")
    print("=" * 50)
    
    # Detect installed servers
    available_servers = detect_installed_servers()
    
    if not available_servers:
        print("\n❌ No MCP servers detected.")
        print("Install MCP servers using:")
        print("  npm install -g @modelcontextprotocol/server-filesystem")
        print("  npm install -g @modelcontextprotocol/server-git")
        return None
    
    # Ask if user wants to configure MCP
    print("\nWould you like to configure MCP servers for this project? (y/n)")
    if input("> ").lower() != "y":
        return None
    
    # Let user select servers
    selected = prompt_user_selection(available_servers)
    
    if not selected:
        print("No servers selected.")
        return None
    
    # Generate configuration
    config = generate_mcp_config(selected, available_servers)
    
    # Save configuration
    save_mcp_config(config, project_path)
    
    # Create .env.example if needed
    create_env_template(config, project_path)
    
    return config


if __name__ == "__main__":
    # For testing
    project_path = Path.cwd()
    interactive_mcp_setup(project_path)